import json
import asyncio
import time
import random
from channels.generic.websocket import AsyncWebsocketConsumer
import uuid
import logging
import requests
import os
import threading

API_KEY = os.environ.get('API_KEY')

logging.basicConfig(
    level=logging.DEBUG,  # Niveau de log, peut être DEBUG, INFO, etc.
    format='%(asctime)s - %(levelname)s - %(message)s', 
    handlers=[
        logging.StreamHandler()  # Affiche les logs dans la console
    ]
)
logger = logging.getLogger(__name__)


active_games = {}
game_lock = threading.Lock()
class FriendPongConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.game_id = str(uuid.uuid4())  # Générer un ID unique pour chaque partie
        self.room_group_name = "" #f"pong_{self.game_id}"  # Créer un groupe unique pour chaque partie
        self.game_loop_task = None  
        self.game_speed = 0.04  
        self.initial_ball_speed = 30
        self.initial_ball_velocity_x = 0.01 * random.choice([-1, 1])
        self.initial_ball_velocity_y = 0  
        self.ball_speed_factor = 30  
        self.paddle_speed = 0.01  
        self.max_paddle_speed = 0.05  
        self.acceleration_rate = 0.002  
        self.deceleration_rate = 0.002  
        self.paddle_acceleration_left = 0
        self.paddle_acceleration_right = 0
        self.name = None
        self.gameEnded = False
        self.rally = 0
        self.player1_socket = None  
        self.player2_socket = None
        self.score_tab = [[0, 0]]
        self.ready_event = asyncio.Event() 

        #definition des stats 
        self.game_statistic = {
            "won_under5": 0,
            "lost_under5": 0,
            "won_under10": 0,
            "lost_under10": 0,
            "won_upper10": 0,
            "lost_upper10": 0,
        }
        

    async def connect(self):
        """ Gérer la connexion WebSocket initiale (rooms privées) """
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"] 
        self.room_group_name = f"pong_{self.room_name}" 

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    def update_player_stats(self, winner, loser):
        game = active_games.get(self.room_group_name)
        if game:
            if winner == "player1":
                rally = self.game_state["rally"]
                stats = game.get("player1_stats")
            elif winner == "player2":
                rally = self.game_state["rally"]
                stats = game.get("player2_stats")

            if rally < 5:
                stats["won_under5"] += 1
            elif rally < 10:
                stats["won_under10"] += 1
            else:
                stats["won_upper10"] += 1

            if loser == "player1":
                rally = self.game_state["rally"]
                stats = game.get("player1_stats")
            elif loser == "player2":
                rally = self.game_state["rally"]
                stats = game.get("player2_stats")

            if rally < 5:
                stats["lost_under5"] += 1
            elif rally < 10:
                stats["lost_under10"] += 1
            else:
                stats["lost_upper10"] += 1
        stats1 = game.get("player1_stats")
        stats2 = game.get("player2_stats")
        logger.info(f"Player 1 : {stats1} ; player2 {stats2}")


    async def disconnect(self, close_code):
        """ Gérer la déconnexion des joueurs """
        game = active_games.get(self.room_group_name)

        if game:
            if game["game_state"] is None:
                if self.channel_name == game["player1_socket"]:
                    # logger.info(f"Le créateur {game['player1_name']} s'est déconnecté avant le début du match. La partie est annulée.")
                    del active_games[self.room_group_name]
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            "type": "game_over",
                            "message": "Le créateur a quitté avant le début de la partie. La partie est annulée.",
                            "winner": None,
                        }
                    )
                elif self.channel_name == game["player2_socket"]:
                    # logger.info(f"Le joueur {game['player2_name']} s'est déconnecté avant le début du match. La partie est annulée.")
                    del active_games[self.room_group_name]
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            "type": "game_over",
                            "message": "Le joueur 2 a quitté avant le début de la partie. La partie est annulée.",
                            "winner": None,
                        }
                    )

            else:
                if self.channel_name == game["player1_socket"]:
                    # logger.info(f"Le joueur {game['player1_name']} s'est déconnecté en cours de jeu. Le joueur 2 gagne.")
                    game["game_state"]["score2"] = 5
                    game["game_state"]["disconnect1"] = True
                    winner = "player2"
                    await self.end_game(winner, game["game_state"], game['player1_name'], game['player2_name'])       
                elif self.channel_name == game["player2_socket"]:
                    # logger.info(f"Le joueur {game['player2_name']} s'est déconnecté en cours de jeu. Le joueur 1 gagne.")
                    game["game_state"]["score1"] = 5
                    game["game_state"]["disconnect2"] = True
                    winner = "player1"
                    await self.end_game(winner, game["game_state"], game['player1_name'], game['player2_name'])       

        else:
            await self.close() 

    async def receive(self, text_data):
        """ Gérer les entrées des joueurs indépendamment """
        text_data_json = json.loads(text_data)
        moves = 'null'
        player = 'null'

        type_message = text_data_json.get('type') # Récupérer le type de message (optionnel)

        if type_message == 'init': # **NOUVEAU : Gestion du message "init" à la connexion**
            info = text_data_json.get('info')
            self.name = info.get('playerName')
            game_mode = text_data_json.get('info', {}).get('game') # Récupérer le mode de jeu depuis le JSON
            join_code = text_data_json.get('info', {}).get('join_code') # Récupérer le code de join (si présent)

            if game_mode == 'create_private':
                await self.handle_create_private_room() # Fonction séparée pour la logique de création
            elif join_code:
                await self.handle_join_private_room(join_code) # Fonction séparée pour la logique de join

            else: # Si message "init" mais sans mode clair (ni create_private ni join_code), erreur
                print("**[DEBUG BACKEND - RECEIVE - INIT] Erreur : Message 'init' reçu sans mode privé valide.**")
                await self.close() # Fermer la connexion si init incorrect

        elif type_message == "moves":
            # print(f"Moves : {text_data}")
            player = text_data_json.get('player')
            moves = text_data_json.get('moves')

            if self.channel_name == self.player1_socket:
                await self.handle_player_moves(moves, player)
            elif self.channel_name == self.player2_socket:
                await self.handle_player_moves(moves, player)
        else:
            print(f"**[DEBUG BACKEND - RECEIVE] Type de message inconnu : {type_message}**")

        # Mettre à jour l'état du jeu avec la référence correcte
        game = active_games.get(self.room_group_name)
        if game:
            game_state = game.get("game_state")
            if game_state:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "game_update",
                        "game_state": game_state 
                    },
                )

   
    async def handle_create_private_room(self):
        """ Logique pour créer une room privée (appelée après réception du message 'init' avec mode 'create_private') """
        private_room_code = str(uuid.uuid4())[:8]
        self.room_group_name = f"pong_private_{private_room_code}" # Redéfinir room_group_name avec le code privé
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.send(text_data=json.dumps({
            'type': 'private_room_code',
            'code': private_room_code
        }))
        # print(f"**[DEBUG BACKEND - CONNECT - CREATE ROOM] Room privée créée avec code : {private_room_code}, room_group_name: {self.room_group_name}**")
        await self.initialize_game_room() # Initialiser la room (gestion des joueurs, game state, etc.)


    async def handle_join_private_room(self, join_code):
        """ Logique pour rejoindre une room privée (appelée après réception du message 'init' avec join_code) """
        self.room_group_name = f"pong_private_{join_code}" # Redéfinir room_group_name avec le code privé
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.initialize_game_room()
        
        # print(f"**[DEBUG BACKEND - CONNECT - JOIN ROOM] Client a rejoint room privée avec code : {join_code}, room_group_name: {self.room_group_name}**")


    async def initialize_game_room(self):
        """ Logique d'initialisation d'UNE room (commune à création et join) - Gestion des joueurs et état du jeu """
        if self.room_group_name not in active_games:
            active_games[self.room_group_name] = {
                "player1_name": None,
                "player2_name": None,
                "player1_socket": None,
                "player2_socket": None,
                "game_state": None,
                "player1_stats": {
                    "won_under5": 0,
                    "lost_under5": 0,
                    "won_under10": 0,
                    "lost_under10": 0,
                    "won_upper10": 0,
                    "lost_upper10": 0,
                },
                "player2_stats": {
                    "won_under5": 0,
                    "lost_under5": 0,
                    "won_under10": 0,
                    "lost_under10": 0,
                    "won_upper10": 0,
                    "lost_upper10": 0,
                },
            }

        game = active_games.get(self.room_group_name)
        role = None

        if not game["player1_socket"]: # Premier joueur dans la room privée
            game["player1_socket"] = self.channel_name
            self.player1_socket = self.channel_name
            self.player1_name = self.name
            game["player1_name"] = self.name

            role = 'player1'

            initial_game_state = {
                "ball_x": 0.5,
                "ball_y": 0.5, 
                "ball_velocity_x": self.initial_ball_velocity_x,
                "ball_velocity_y": self.initial_ball_velocity_y,
                "player1_y": 0.5,
                "player2_y": 0.5, 
                "score1": 0, 
                "score2": 0, 
                "disconnect1": False,
                "disconnect2": False,
                "rally": 0,
            }
            game["game_state"] = initial_game_state
            self.game_state = initial_game_state

        elif not game["player2_socket"]: 
            game["player2_socket"] = self.channel_name
            self.player2_socket = self.channel_name
            game["player2_name"] = self.name
            role = 'player2'
            
            self.game_state = game["game_state"]

            player1_name = game["player1_name"] 
            player2_name = game["player2_name"]

            logger.info(f"A L'ENVOIE : {player1_name} : {player2_name}")

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "players_ready",
                    "message": "Deux joueurs connectés, la partie privée peut commencer !",
                    "player1": player1_name,
                    "player2": player2_name,
                }
            )
            await self.start_game()

        else:
            await self.close()

        await self.send(text_data=json.dumps({'type': 'role_assignment', 'role': role}))


    async def start_game(self):
        """ Démarre la partie lorsque deux joueurs sont connectés """
        self.game_loop_task = asyncio.create_task(self.game_loop())


        
    def reset_ball(self, direction):
        self.game_state["ball_x"] = 0.5
        self.game_state["ball_y"] = 0.5
        self.game_state["player1_y"] = 0.5
        self.game_state["player2_y"] = 0.5
        self.game_state["ball_velocity_x"] = 0.01 * direction 
        self.game_state["ball_velocity_y"] = 0
        self.ball_speed_factor = self.initial_ball_speed

 
    async def handle_player_moves(self, move, player):
        logger.info(f"IN THE MOVES {player} : {move}")
        """ Gérer les mouvements des joueurs de manière asynchrone """
        if player == "player1":
            if move.get("up", False):
                self.game_state["player1_y"] = max(self.game_state["player1_y"] - self.paddle_speed, 0)
            elif move.get("down", False):
                self.game_state["player1_y"] = min(self.game_state["player1_y"] + self.paddle_speed, 1)


        elif player == "player2":
            if move.get("up", False):
                self.game_state["player2_y"] = max(self.game_state["player2_y"] - self.paddle_speed, 0)
            elif move.get("down", False):
                self.game_state["player2_y"] = min(self.game_state["player2_y"] + self.paddle_speed, 1)


    async def game_loop(self):
        previous_time = time.time()
        # game_state = active_games.get(self.room_group_name)

        while True:
            current_time = time.time()
            delta_time = current_time - previous_time
            previous_time = current_time

            await asyncio.sleep(0.01)

            # Mettre à jour la position de la balle
            self.game_state["ball_x"] += self.game_state["ball_velocity_x"] * delta_time * self.ball_speed_factor
            self.game_state["ball_y"] += self.game_state["ball_velocity_y"] * delta_time * self.ball_speed_factor

            # Gestion des rebonds de la balle (sur les murs)
            if self.game_state["ball_y"] <= 0:
                self.game_state["ball_y"] = 0
                self.game_state["ball_velocity_y"] = -self.game_state["ball_velocity_y"]

            elif self.game_state["ball_y"] >= 1:
                self.game_state["ball_y"] = 1
                self.game_state["ball_velocity_y"] = -self.game_state["ball_velocity_y"]


             # Détection des collisions avec les paddles (avec AABB)
            ball_rect = {  # Boîte englobante de la balle
                "x": self.game_state["ball_x"] * 900 - 7,  # Ajuster 900 et 7 si nécessaire
                "y": self.game_state["ball_y"] * 500 - 7,  # Ajuster 500 et 7 si nécessaire
                "width": 14,  # Diamètre de la balle
                "height": 14,  # Diamètre de la balle
            }

            paddle1_rect = {  # Boîte englobante du paddle gauche
                "x": 0.05 * 900,  # Marge horizontale
                "y": self.game_state["player1_y"] * 500 - 30,  # Centré verticalement
                "width": 10,  # Largeur du paddle
                "height": 60,  # Hauteur du paddle
            }

            paddle2_rect = {  # Boîte englobante du paddle droit
                "x": 0.95 * 900 - 10,  # Marge horizontale + largeur du paddle
                "y": self.game_state["player2_y"] * 500 - 30,  # Centré verticalement
                "width": 10,  # Largeur du paddle
                "height": 60,  # Hauteur du paddle
            }

            def detect_collision(rect1, rect2):  # Fonction de détection AABB
                return (
                    rect1["x"] < rect2["x"] + rect2["width"] and
                    rect1["x"] + rect1["width"] > rect2["x"] and
                    rect1["y"] < rect2["y"] + rect2["height"] and
                    rect1["y"] + rect1["height"] > rect2["y"]
                )

            if detect_collision(ball_rect, paddle1_rect) and self.game_state["ball_velocity_x"] < 0:
                self.game_state["ball_velocity_x"] *= -1
                self.game_state["ball_velocity_y"] = (self.game_state["ball_y"] - self.game_state["player1_y"]) * 0.1
                self.ball_speed_factor = min(60, self.ball_speed_factor + 5)
                self.game_state["rally"] += 1

            elif detect_collision(ball_rect, paddle2_rect) and self.game_state["ball_velocity_x"] > 0:
                self.game_state["ball_velocity_x"] *= -1
                self.game_state["ball_velocity_y"] = (self.game_state["ball_y"] - self.game_state["player2_y"]) * 0.1
                self.ball_speed_factor = min(60, self.ball_speed_factor + 5)
                self.game_state["rally"] += 1

            # Gestion des scores
            if self.game_state["ball_x"] <= 0:
                self.game_state["score2"] += 1
                self.score_tab.append([self.game_state["score1"], self.game_state["score2"]])
                self.update_player_stats("player2", "player1")
                self.reset_ball(1)
                self.game_state["rally"] = 0
                self.game_state["ball_velocity_x"] = -abs(self.game_state["ball_velocity_x"])

                if self.game_state["score2"] >= 5:
                    game = active_games.get(self.room_group_name)
                    player1_name = game.get("player1_name")
                    player2_name = game.get("player2_name")
                    winner = "player2"
                    await self.end_game(winner, self.game_state, player1_name, player2_name)
                    return 

            elif self.game_state["ball_x"] >= 1:
                self.game_state["score1"] += 1
                self.score_tab.append([self.game_state["score1"], self.game_state["score2"]])
                self.update_player_stats("player1", "player2")
                self.reset_ball(-1)
                self.game_state["rally"] = 0
                self.game_state["ball_velocity_x"] = abs(self.game_state["ball_velocity_x"])

                if self.game_state["score1"] >= 5:
                    game = active_games.get(self.room_group_name)
                    player1_name = game.get("player1_name")
                    player2_name = game.get("player2_name")
                    winner = "player1"
                    await self.end_game(winner, self.game_state, player1_name, player2_name)
                    return 

            await self.update_game_state()
        

    async def end_game(self, winner, game_state, player1_name, player2_name):
        """ Arrêter la boucle de jeu et annoncer le vainqueur """
        logger.info("AVANT")
        if self.game_loop_task: 
            self.game_loop_task.cancel() 
            try:
                await self.game_loop_task 
            except asyncio.CancelledError:
                pass 
        logger.info("APRES")
        # Envoyer un message "game_over" à tous les joueurs du groupe pour annoncer le vainqueur
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "game_over", 
                "message": f"{winner} a gagné la partie !", 
                "winner": winner, 
                "game_state": game_state, 
                "player1_name": player1_name,
                "player2_name": player2_name,
            }
        )
        logger.info("A LA FIN")

        

    async def update_game_state(self):
        message = {
                "type": "game_update",
                "game_state": self.game_state
        }
        await self.channel_layer.group_send(
            self.room_group_name,  # Nom du groupe auquel envoyer le message
            message  # Le message à envoyer
        )
    
    
    async def players_ready(self, event):
        message = event['message']
        player1 = event['player1']
        player2 = event['player2']
        await self.send(text_data=json.dumps({
            "type": "players_ready",
            "message": message,
            "player1": player1,
            "player2": player2
        }))
    
    
    async def game_over(self, event): 
        """ Gérer le message 'game_over' diffusé au groupe """
        game_over_message = event['message'] 
        winner = event['winner'] 

        message = {
            "type": "game_over",
            "message": game_over_message, 
            "winner": winner 
        }
        await self.send(text_data=json.dumps(message))
        self.gameEnded = True
        game_state = event.get("game_state")
        player1_name = event.get("player1_name")
        player2_name = event.get("player2_name")
        if player1_name and player2_name:
            self.send_to_database(game_state, player1_name, player2_name)
        else:
            self.gameEnded = False
    
    
    async def game_update(self, event):
        """ Gérer le message 'game_update' diffusé au groupe """
        game_state = event['game_state']
        message = {
            "type": "game_update",
            "game_state": game_state
        }
        await self.send(text_data=json.dumps(message))

        
    async def game_over(self, event): 
        """ Gérer le message 'game_over' diffusé au groupe """
        game_over_message = event['message'] 
        winner = event['winner'] 

        message = {
            "type": "game_over",
            "message": game_over_message, 
            "winner": winner 
        }
        await self.send(text_data=json.dumps(message))
        self.gameEnded = True
        game_state = event.get("game_state")
        player1_name = event.get("player1_name")
        player2_name = event.get("player2_name")
        if player1_name and player2_name:
            self.send_to_database(game_state, player1_name, player2_name)
        else:
            self.gameEnded = False
    
    
    async def game_update(self, event):
        """ Gérer le message 'game_update' diffusé au groupe """
        game_state = event['game_state'] 
        message = {
            "type": "game_update",
            "game_state": game_state
        }
        await self.send(text_data=json.dumps(message))

        
    def send_to_database(self, game_state, player1_name, player2_name):
        if self.gameEnded is False: # Double sécurité
            return
        
        self.gameEnded = True
        # logger.error(f"---------------------------------------------------------")
        # logger.error(f"GAME = {self.game_id}")
        # logger.error(f"---------------------------------------------------------")
        with game_lock:
            game = active_games.get(self.room_group_name)
            # game_state = game.get("game_state")
            if game is not None:
                player1 = player1_name
                player2 = player2_name
                score1 = game_state.get("score1")
                score2 = game_state.get("score2")
                headers = {
                    "X-API-KEY": API_KEY
                }
                url_user1 = f"http://back-end:8000/api/profile/{player1}/"
                url_user2 = f"http://back-end:8000/api/profile/{player2}/"
                # logger.info(f"SCORE : {score1} / {score2}")
                url = "http://back-end:8000/api/games/pong/"  #
                # url2 = "http://back-end:8000/api/profile/gkubina/" #
                url3 = "http://back-end:8000/api/stats_increment/gkubina/" #

                user1_stats = f"http://back-end:8000/api/stats/{player1}/"
                user2_stats = f"http://back-end:8000/api/stats/{player2}/"
                url_update_user1 = f"http://back-end:8000/api/stats_increment/{player1}/"
                url_update_user2 = f"http://back-end:8000/api/stats_increment/{player2}/"
                
                stats1 = requests.get(user1_stats, headers=headers)
                stats2 = requests.get(user2_stats, headers=headers)
                if stats1.status_code == 200:
                    stats1 = stats1.json()
                    # logger.info(f"DATA of {player1}: {stats1}")
                if stats2.status_code == 200:
                    stats2 = stats2.json()
                    # logger.info(f"DATA of {player2}: {stats2}")
                

                response1 = requests.get(url_user1, headers=headers)
                response2 = requests.get(url_user2, headers=headers)
                data1 = None
                data2 = None
                if response1.status_code == 200:
                    data1 = response1.json()
                    logger.info(f"DATA of {player1}: {data1}")

                    current_rank1 = data1.get('currentRank', 0)
                    logger.info(f"Rank of {player1}: {current_rank1}")

                if response2.status_code == 200:
                    data2 = response2.json()
                    logger.info(f"DATA of {player2}: {data2}")

                    current_rank2 = data2.get('currentRank', 0)
                    logger.info(f"Rank of {player2}: {current_rank2}")

                # {'id': 4, 
                #  'username': 'daleliev',
                #  'cover_photo': '/media/profile_image/daleliev.jpg',
                #  'online': True, 
                #  'last_seen': '2025-02-16T19:05:46.685229+01:00',
                #  'is_active': True, 
                #  'is_42': True,
                #  'theme': 'dark', 
                #  'lang': 'en'}
                
                def calculer_elo(R_A, R_B, K, S):
                    """Calcule le nouveau classement Elo du joueur A.

                    Args:
                        R_A: Classement actuel du joueur A.
                        R_B: Classement actuel du joueur B.
                        K: Facteur K.
                        S: Score de la partie pour le joueur A (1, 0.5 ou 0).

                    Returns:
                        Le nouveau classement Elo du joueur A.
                    """
                    # logger.info(f"s:{S}")
                    E_A = 1 / (1 + 10 ** ((R_B - R_A) / 400))
                    R_A_prime = R_A + K * (S - E_A)
                    return (R_A_prime)
                
                # Classements initiaux
                R_joueur_1 = current_rank1
                R_joueur_2 = current_rank2

                # Facteur K
                diff = 0
                S_joueur_1 = 0
                S_joueur_2 = 0
                if (score1 == 5) :
                    diff = score2
                    S_joueur_1 = 1
                    S_joueur_2 = 0
                else :
                    diff = score1
                    S_joueur_1 = 0
                    S_joueur_2 = 1
                logger.info(f"SCORE1 {score1} SCORE2 {score2}")

                K = 0
                if (5 - diff == 5):
                    K = 40
                elif (5 - diff == 4):
                    K = 35
                elif (5 - diff == 3):
                    K = 30
                elif (5 - diff == 2):
                    K = 20
                elif (5 - diff == 1):
                    K = 10

                R_joueur_1_prime = calculer_elo(R_joueur_1, R_joueur_2, K, S_joueur_1)
                R_joueur_2_prime = calculer_elo(R_joueur_2, R_joueur_1, K, S_joueur_2)
                R_joueur_1_prime = round(R_joueur_1_prime)
                R_joueur_2_prime = round(R_joueur_2_prime)

                if (R_joueur_1_prime < 0):
                    R_joueur_1_prime = 0
                if (R_joueur_2_prime < 0):
                    R_joueur_2_prime = 0
                # logger.info(f"Nouveau classement du joueur 1 : {player1} {R_joueur_1}->{R_joueur_1_prime}")
                # logger.info(f"Nouveau classement du joueur 2 : {player2} {R_joueur_2}->{R_joueur_2_prime}")


                # # response = requests.get(url, headers=headers)
                # logger.info("Return: ", response.status_code , response.json())
                winner = None
                loser = None
                if score1 > score2:
                    winner = data1.get("id")
                    loser = data2.get("id")
                else:
                    winner = data2.get("id")
                    loser = data1.get("id")
                
                game_data = {
                        "player1_score": score1,
                        "player2_score": score2,
                        "rank_player1_change": R_joueur_1_prime - R_joueur_1,
                        "rank_player2_change": R_joueur_2_prime - R_joueur_2,
                        "type": "solo",
                        "player1": data1.get("id"),
                        "player2": data2.get("id"),
                        "winner": winner,
                        "loser": loser,
                }
                response = requests.post(url, headers=headers, json=game_data)
                response = response.json()
                # logger.info(f"game_data : {response}")
                
                
                win1 = 0
                win2 = 0
                loss1 = 0
                loss2 = 0
                if winner == data1.get("id"):
                    win1 = 1
                    loss2 = 1
                else:
                    loss1 = 1
                    win2 = 1

                stats1 = game.get("player1_stats")
                fields1 = {
                    "stat_pong_solo_rank" : R_joueur_1_prime - R_joueur_1, 
                    "stat_pong_solo_progress" : R_joueur_1_prime, 
                    "stat_pong_solo_wins_tot" : win1, 
                    "stat_pong_solo_loss_tot" : loss1, 
                    "stat_pong_solo_tournament_wins" : 0, 
                    "stat_pong_solo_tournament_loss" : 0, 
                    "stat_pong_solo_wins_tot_min5" : stats1["won_under5"], 
                    "stat_pong_solo_loss_tot_min5" : stats1["lost_under5"], 
                    "stat_pong_solo_wins_tot_min10" : stats1["won_under10"], 
                    "stat_pong_solo_loss_tot_min10" : stats1["lost_under10"], 
                    "stat_pong_solo_wins_tot_max10" : stats1["won_upper10"], 
                    "stat_pong_solo_loss_tot_max10" : stats1["lost_upper10"], 
                }
                response1 = requests.patch(url_update_user1, headers=headers, json=fields1)
                response1 = response1.json()
                # logger.info(f"fields1 : {fields1}")
                # logger.info(f"response1 : {response1}")
                
                stats2 = game.get("player2_stats")
                fields2 = {
                    "stat_pong_solo_rank" : R_joueur_2_prime - R_joueur_2, 
                    "stat_pong_solo_progress" : R_joueur_2_prime, 
                    "stat_pong_solo_wins_tot" : win2, 
                    "stat_pong_solo_loss_tot" : loss2, 
                    "stat_pong_solo_tournament_wins" : 0, 
                    "stat_pong_solo_tournament_loss" : 0, 
                    "stat_pong_solo_wins_tot_min5" : stats2["won_under5"], 
                    "stat_pong_solo_loss_tot_min5" : stats2["lost_under5"], 
                    "stat_pong_solo_wins_tot_min10" : stats2["won_under10"], 
                    "stat_pong_solo_loss_tot_min10" : stats2["lost_under10"], 
                    "stat_pong_solo_wins_tot_max10" : stats2["won_upper10"], 
                    "stat_pong_solo_loss_tot_max10" : stats2["lost_upper10"], 
                }
                logger.info(f"fields2 : {fields2}")
                response2 = requests.patch(url_update_user2, headers=headers, json=fields2)
                response2 = response2.json()

                del active_games[self.room_group_name]
            else: 
                return
        self.gameEnded = False
