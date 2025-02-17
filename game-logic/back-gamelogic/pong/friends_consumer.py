import json
import asyncio
import time
import random
from channels.generic.websocket import AsyncWebsocketConsumer
import uuid
import logging

logging.basicConfig(
    level=logging.DEBUG,  # Niveau de log, peut être DEBUG, INFO, etc.
    format='%(asctime)s - %(levelname)s - %(message)s', 
    handlers=[
        logging.StreamHandler()  # Affiche les logs dans la console
    ]
)
logger = logging.getLogger(__name__)


active_games = {}
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

        self.player1_socket = None  
        self.player2_socket = None
        self.score_tab = [[0, 0]] #tableau pour suivre la progression des scores
        self.ready_event = asyncio.Event()  # Ajout d'un événement pour attendre 2 joueurs

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
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"] # Récupérer room_name de l'URL (toujours utile pour identifier la room dans l'URL)
        self.room_group_name = f"pong_{self.room_name}" # Group name initial (peut être re-défini plus tard pour les privées)

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    def update_player_stats(self, player):
        game = active_games.get(self.game_id)
        if game:
            if player == "player1":
                score = game["game_state"]["score1"]
                rally = game["game_state"]["rally_player1"]
                stats = game.get("player1_stats")
                
                # Mise à jour des statistiques en fonction du rally
                if rally < 5:
                    stats["won_under5"] += 1 if score > 0 else 0
                    stats["lost_under5"] += 1 if score == 0 else 0
                elif rally < 10:
                    stats["won_under10"] += 1 if score > 0 else 0
                    stats["lost_under10"] += 1 if score == 0 else 0
                else:
                    stats["won_upper10"] += 1 if score > 0 else 0
                    stats["lost_upper10"] += 1 if score == 0 else 0

        
            elif player == "player2":
                score = game["game_state"]["score2"]
                rally = game["game_state"]["rally_player2"]
                stats = game.get("player2_stats")
                
                # Mise à jour des statistiques en fonction du rally
                if rally < 5:
                    stats["won_under5"] += 1 if score > 0 else 0
                    stats["lost_under5"] += 1 if score == 0 else 0
                elif rally < 10:
                    stats["won_under10"] += 1 if score > 0 else 0
                    stats["lost_under10"] += 1 if score == 0 else 0
                else:
                    stats["won_upper10"] += 1 if score > 0 else 0
                    stats["lost_upper10"] += 1 if score == 0 else 0

    async def disconnect(self, close_code):
        """ Gérer la déconnexion des joueurs """
        game = active_games.get(self.room_group_name)

        if game:
            if game["game_state"] is None:
                if self.channel_name == game["player1_socket"]:
                    logger.info(f"Le créateur {game['player1_name']} s'est déconnecté avant le début du match. La partie est annulée.")
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
                    logger.info(f"Le joueur {game['player2_name']} s'est déconnecté avant le début du match. La partie est annulée.")
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
                    logger.info(f"Le joueur {game['player1_name']} s'est déconnecté en cours de jeu. Le joueur 2 gagne.")
                    game["game_state"]["score2"] = 5
                    game["game_state"]["disconnect1"] = True
                    winner = "player2"
                    await self.end_game(winner)
                elif self.channel_name == game["player2_socket"]:
                    logger.info(f"Le joueur {game['player2_name']} s'est déconnecté en cours de jeu. Le joueur 1 gagne.")
                    game["game_state"]["score1"] = 5
                    game["game_state"]["disconnect2"] = True
                    winner = "player1"
                    await self.end_game(winner)

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

        elif not game["player2_socket"]: # Second joueur rejoignant la room privée
            game["player2_socket"] = self.channel_name
            self.player2_socket = self.channel_name
            game["player2_name"] = self.name
            role = 'player2'
            
            self.game_state = game["game_state"]
            # logger.info(self.name)
            # self.player2_name = self.name

            player1_name = game["player1_name"]  # Now these will have values
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

        else: # Room privée pleine (peu probable dans un scénario de jeu entre amis, mais à gérer)
            # print(f"Room privée {self.room_group_name} est pleine (cas improbable).")
            await self.close() # Fermer la connexion car room pleine

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

        """ Gérer les mouvements des joueurs de manière asynchrone """
        if player == "player1":
            # print(f"Player1 BEFORE {self.game_state}")
            if move.get("up", False):
                self.game_state["player1_y"] = max(self.game_state["player1_y"] - self.paddle_speed, 0)
            elif move.get("down", False):
                self.game_state["player1_y"] = min(self.game_state["player1_y"] + self.paddle_speed, 1)
            # print(f"Player1 AFTER {self.game_state}")


        elif player == "player2":
            # print(f"Player2 BEFORE {self.game_state}")
            if move.get("up", False):
                self.game_state["player2_y"] = max(self.game_state["player2_y"] - self.paddle_speed, 0)
            elif move.get("down", False):
                self.game_state["player2_y"] = min(self.game_state["player2_y"] + self.paddle_speed, 1)
            # print(f"Player2 AFTER {self.game_state}")


    async def game_loop(self):
        previous_time = time.time()
        game_state = active_games.get(self.game_id)


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

            # # Gestion des collisions avec les paddles
            # if self.game_state["ball_x"] <= 0.05:
            #     # print("touch left")
            #     if self.game_state["ball_velocity_x"] < 0:
            #         if (self.game_state["player1_y"] - 0.1 <= self.game_state["ball_y"] <= self.game_state["player1_y"] + 0.1):
            #             self.game_state["ball_velocity_x"] *= -1
            #             self.game_state["ball_velocity_y"] = (self.game_state["ball_y"] - self.game_state["player1_y"]) * 0.1
            #             self.ball_speed_factor = min(80, self.ball_speed_factor + 5)

            # elif self.game_state["ball_x"] >= 0.95:
            #     # print("touch right")
            #     if self.game_state["ball_velocity_x"] > 0:
            #         if (self.game_state["player2_y"] - 0.1 <= self.game_state["ball_y"] <= self.game_state["player2_y"] + 0.1):
            #             self.game_state["ball_velocity_x"] *= -1
            #             self.game_state["ball_velocity_y"] = (self.game_state["ball_y"] - self.game_state["player2_y"]) * 0.1
            #             self.ball_speed_factor = min(80, self.ball_speed_factor + 5)

            # Gestion des scores
            if self.game_state["ball_x"] <= 0:
                self.game_state["score2"] += 1
                self.score_tab.append([self.game_state["score1"], self.game_state["score2"]])
                self.reset_ball(1)
                game_state["rally"] = 0
                self.game_state["ball_velocity_x"] = -abs(self.game_state["ball_velocity_x"])

                if self.game_state["score2"] >= 5:
                    winner = "player2"
                    await self.end_game(winner) # APPELER LA FONCTION end_game POUR ARRÊTER LE JEU ET ANNONCER LE VAINQUEUR
                    return 

            elif self.game_state["ball_x"] >= 1:
                self.game_state["score1"] += 1
                self.score_tab.append([self.game_state["score1"], self.game_state["score2"]])
                self.reset_ball(-1)
                game_state["rally"] = 0
                self.game_state["ball_velocity_x"] = abs(self.game_state["ball_velocity_x"])

                if self.game_state["score1"] >= 5:
                    winner = "player1"
                    await self.end_game(winner) # APPELER LA FONCTION end_game POUR ARRÊTER LE JEU ET ANNONCER LE VAINQUEUR
                    return 

            await self.update_game_state()
        

    async def end_game(self, winner):
        """ Arrêter la boucle de jeu et annoncer le vainqueur """
        if self.game_loop_task: # Vérifier si la game_loop_task existe et est en cours
            self.game_loop_task.cancel() # Annuler la game_loop_task pour arrêter la boucle de jeu
            try:
                await self.game_loop_task # Attendre que la tâche soit bien annulée (bonne pratique)
            except asyncio.CancelledError:
                pass # Tâche annulée, c'est normal

        # Envoyer un message "game_over" à tous les joueurs du groupe pour annoncer le vainqueur
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "game_over", # Type de message pour indiquer la fin du jeu
                "message": f"{winner} a gagné la partie !", # Message annonçant le vainqueur
                "winner": winner, # Envoyer aussi le nom du vainqueur pour que le front-end puisse l'afficher
            }
        )
        print(f"Partie terminée ! Vainqueur : {winner}")
        

    async def update_game_state(self):
        message = {
                "type": "game_update",
                "game_state": self.game_state
        }
        await self.channel_layer.group_send(
            self.room_group_name,  # Nom du groupe auquel envoyer le message
            message  # Le message à envoyer
        )
        # print(f"🟢 {self.game_state}") # LOG DE RÉCEPTION CÔTÉ SERVEUR


    # def calculate_ball_angle(self, ball_y, paddle_y):
    #         # Calculer l'écart entre la balle et le centre du paddle
    #     distance_from_center = ball_y - paddle_y

    #         # Plus l'écart est grand, plus l'angle de rebond sera large
    #     angle = distance_from_center * 0.1  # Ajuster ce coefficient pour affiner l'angle
    #     return angle
    
    
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
    
    
    async def game_update(self, event):
        """ Gérer le message 'game_update' diffusé au groupe """
        game_state = event['game_state']
        message = {
            "type": "game_update",
            "game_state": game_state
        }
        await self.send(text_data=json.dumps(message))