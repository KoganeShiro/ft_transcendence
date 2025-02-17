import json
import asyncio
import time
import random
from channels.generic.websocket import AsyncWebsocketConsumer
import uuid  
import logging
import requests
import os

API_KEY = os.environ.get('API_KEY')

logging.basicConfig(
    level=logging.INFO,  # Niveau de log, peut être DEBUG, INFO, etc.
    format='%(asctime)s - %(levelname)s - %(message)s', 
    handlers=[
        logging.StreamHandler()  # Affiche les logs dans la console
    ]
)
logger = logging.getLogger(__name__)

active_games = {}
class PongConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.game_id = str(uuid.uuid4())  # Générer un ID unique pour chaque partie
        self.room_group_name = "" #f"pong_{self.game_id}"  # Créer un groupe unique pour chaque partie
        self.game_loop_task = None  
        self.initial_ball_speed = 10
        self.initial_ball_velocity_x = 0.01 * random.choice([-1, 1])
        self.initial_ball_velocity_y = 0  
        self.ball_speed_factor = 10  
        self.paddle_speed = 0.01  
        self.player1_socket = None  
        self.player2_socket = None 
        self.score_tab = [[0, 0]] 
        self.ready_event = asyncio.Event()
        self.player1_name = None
        self.player2_name = None
        self.name = None
        self.rally = 0

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
        """ Gérer la connexion des joueurs et l'affectation aux parties """
        await self.accept()
            # Vérifier s'il existe une partie en attente d'un deuxième joueur
        for game_id, game in active_games.items():
            if game["player1_socket"] and not game["player2_socket"]:
                self.game_id = game_id  # On récupère bien le game_id existant
                self.room_group_name = f"pong_{self.game_id}"
                active_games[self.game_id]["player2_socket"] = self.channel_name
                self.game_state = game.get("game_state")
                self.player2_socket = self.channel_name

                # Ajouter le joueur au groupe et démarrer la partie
                await self.channel_layer.group_add(self.room_group_name, self.channel_name)
                await self.send(text_data=json.dumps({
                    'type': 'role_assignment', # Type de message optionnel, mais bonne pratique
                    'role': 'player2',
                }))
                
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "players_ready",  # Nouveau type de message pour signaler que 2 joueurs sont prêts
                        "message": "Deux joueurs connectés, la partie peut commencer !" # Message optionnel
                    }
                )
                
                await self.start_game()
                return  # Stop ici pour éviter de recréer une partie

        # Si aucune partie en attente, créer une nouvelle
        self.game_id = str(uuid.uuid4())  # Uniquement si pas de partie existante
        self.room_group_name = f"pong_{self.game_id}"
        initial_game_state = { # Définir l'état initial du jeu **ICI** (dans connect(), pour les nouvelles parties)
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
        active_games[self.game_id] = {
            "player1_socket": self.channel_name,
            "player2_socket": None,
            "player1_name": None,
            "player2_name": None,
            "game_state": initial_game_state,
            "player1_stats": self.game_statistic.copy(),
            "player2_stats": self.game_statistic.copy(),
        }
        game = active_games.get(self.game_id) # Récupérer le jeu de active_games (maintenant qu'il est créé)
        if game: # Vérification (toujours bonne pratique)
            self.game_state = game.get("game_state") # **INITIALISER CORRECTEMENT self.game_state EN RÉCUPÉRANT LA VERSION DE active_games !**
        self.player1_socket = self.channel_name
        await self.send(text_data=json.dumps({
            'type': 'role_assignment', # Type de message optionnel, mais bonne pratique
            'role': 'player1',
        }))
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)


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
        game = active_games.get(self.game_id)

        if game:
            # Si la partie n'a pas encore commencé
            if game["player2_socket"] is None:  # Si aucun joueur 2 n'est connecté
                if self.channel_name == game["player1_socket"]:
                    # Si le créateur (player 1) se déconnecte avant de commencer
                    logger.info(f"Le créateur {game['player1_name']} s'est déconnecté avant le début du match. La partie est annulée.")
                    del active_games[self.game_id]  # Supprimer la partie
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            "type": "game_over",
                            "message": "Le créateur a quitté avant le début de la partie. La partie est annulée.",
                            "winner": None,
                        }
                    )
                # Si le joueur 2 se déconnecte avant que la partie commence
                elif self.channel_name == game["player2_socket"]:
                    logger.info(f"Le joueur {game['player2_name']} s'est déconnecté avant le début du match. La partie est annulée.")
                    del active_games[self.game_id]  # Supprimer la partie
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            "type": "game_over",
                            "message": "Le joueur 2 a quitté avant le début de la partie. La partie est annulée.",
                            "winner": None,
                        }
                    )
            else:
                # Si la partie a déjà commencé
                if self.channel_name == game["player1_socket"]:
                    logger.info(f"Le joueur {game['player1_name']} s'est déconnecté en cours de jeu. Le joueur 2 gagne.")
                    game["game_state"]["score2"] = 5  # Donne la victoire au joueur 2
                    game["game_state"]["disconnect1"] = True  # Marque la déconnexion de player1
                    winner = "player2"
                    await self.end_game(winner)  # Terminer la partie et annoncer le gagnant
                elif self.channel_name == game["player2_socket"]:
                    logger.info(f"Le joueur {game['player2_name']} s'est déconnecté en cours de jeu. Le joueur 1 gagne.")
                    game["game_state"]["score1"] = 5  # Donne la victoire au joueur 1
                    game["game_state"]["disconnect2"] = True  # Marque la déconnexion de player2
                    winner = "player1"
                    await self.end_game(winner)  # Terminer la partie et annoncer le gagnant
        else:
            # Si le jeu n'existe pas, fermer simplement la connexion
            await self.close()


    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        type_message = text_data_json.get('type')
        info = text_data_json.get('info')
        
        moves = 'null'
        player = 'null'

        if info:  # Si on reçoit un message avec les infos du joueur (nom)
                self.name = info.get('playerName')
                logger.debug(f"Joueur {self.channel_name} a envoyé son nom : {self.name}")

                game = active_games.get(self.game_id)
                if game:
                    if not game["player1_name"]:
                        game["player1_name"] = self.name
                        self.player1_name = self.name
                    elif not game["player2_name"]:
                        game["player2_name"] = self.name
                        self.player2_name = self.name

                        player1_name = game["player1_name"]
                        player2_name = game["player2_name"]

                        logger.debug(f"Les deux joueurs sont connectés : {player1_name} et {player2_name}")

                        await self.channel_layer.group_send(
                            self.room_group_name,
                            {
                                "type": "players_ready",
                                "message": "Deux joueurs connectés, la partie peut commencer !",
                                "player1": player1_name,
                                "player2": player2_name,
                            }
                        )
                        await self.start_game()
                        
        if type_message == "moves":
            # print(f"Moves : {text_data}")
            player = text_data_json.get('player')
            moves = text_data_json.get('moves')
        
        if self.channel_name == self.player1_socket:
            await self.handle_player_moves(moves, player)
        elif self.channel_name == self.player2_socket:
            await self.handle_player_moves(moves, player)

        # Mettre à jour l'état du jeu avec la référence correcte
        game = active_games.get(self.game_id)
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

            await asyncio.sleep(0.02)

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

            # Gestion des collisions avec les paddles
            if self.game_state["ball_x"] <= 0.05:
                # print("touch left")
                if self.game_state["ball_velocity_x"] < 0:
                    if (self.game_state["player1_y"] - 0.1 <= self.game_state["ball_y"] <= self.game_state["player1_y"] + 0.1):
                        self.game_state["ball_velocity_x"] *= -1
                        self.game_state["ball_velocity_y"] = (self.game_state["ball_y"] - self.game_state["player1_y"]) * 0.1
                        self.ball_speed_factor = min(60, self.ball_speed_factor + 5)
                        self.game_state["rally"] += 1

            elif self.game_state["ball_x"] >= 0.95:
                # print("touch right")
                if self.game_state["ball_velocity_x"] > 0:
                    if (self.game_state["player2_y"] - 0.1 <= self.game_state["ball_y"] <= self.game_state["player2_y"] + 0.1):
                        self.game_state["ball_velocity_x"] *= -1
                        self.game_state["ball_velocity_y"] = (self.game_state["ball_y"] - self.game_state["player2_y"]) * 0.1
                        self.ball_speed_factor = min(60, self.ball_speed_factor + 5)
                        self.game_state["rally"] += 1

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
        self.send_to_database()
        # print(f"Partie terminée ! Vainqueur : {winner}")
        

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


    def calculate_ball_angle(self, ball_y, paddle_y):
            # Calculer l'écart entre la balle et le centre du paddle
        distance_from_center = ball_y - paddle_y

            # Plus l'écart est grand, plus l'angle de rebond sera large
        angle = distance_from_center * 0.1  # Ajuster ce coefficient pour affiner l'angle
        return angle
    
    
    async def players_ready(self, event):
        message = event.get('message')
        player1 = event.get('player1')
        player2 = event.get('player2')
        await self.send(text_data=json.dumps({
            "type": "players_ready",
            "message": message,
            "player1": player1,
            "player2": player2, 
        }))
    
    
    async def game_over(self, event): # <--- AJOUTEZ CETTE FONCTION DE GESTION (HANDLER) POUR game_over
        """ Gérer le message 'game_over' diffusé au groupe """
        game_over_message = event['message'] # Récupérer le message de fin de partie de l'event
        winner = event['winner'] # Récupérer le nom du vainqueur de l'event

        message = {
            "type": "game_over",
            "message": game_over_message, # Renvoyer le message de fin de partie au front-end
            "winner": winner # Renvoyer le nom du vainqueur au front-end
        }
        # ENVOYER le message 'game_over' (avec le message et le vainqueur) au CLIENT WEBSOCKET CONNECTÉ à CE CONSUMER (en utilisant self.send())
        await self.send(text_data=json.dumps(message))
    
    
    async def game_update(self, event):
        """ Gérer le message 'game_update' diffusé au groupe """
        game_state = event['game_state'] # Récupérer l'état du jeu du message
        message = {
            "type": "game_update",
            "game_state": game_state
        }
        # ENVOYER le message 'game_update' (avec l'état du jeu) au CLIENT WEBSOCKET CONNECTÉ à CE CONSUMER (en utilisant self.send())
        await self.send(text_data=json.dumps(message))
        
    def send_to_database(self):
        game = active_games.get(self.game_id)
        game_state = game.get("game_state")

        player1 = game.get('player1_name')
        player2 = game.get('player2_name')
        score1 = game_state.get("score1")
        score2 = game_state.get("score2")
        logger.info(f"SCORE : {score1} / {score2}")
        url = "http://back-end:8000/api/games/pong/"  #
        # url2 = "http://back-end:8000/api/profile/gkubina/" #
        url3 = "http://back-end:8000/api/stats_increment/gkubina/" #

        url_user1 = f"http://back-end:8000/api/profile/{player1}/"
        url_user2 = f"http://back-end:8000/api/profile/{player2}/"
        url_update_user1 = "http://back-end:8000/api/stats_increment/{player1}/"
        url_update_user2 = "http://back-end:8000/api/stats_increment/{player2}/"
        
        headers = {
            "X-API-KEY": API_KEY
        }
        response1 = requests.get(url_user1, headers=headers)
        response2 = requests.get(url_user2, headers=headers)
        data1 = None
        data2 = None
        if response1.status_code == 200:
            data1 = response1.json()
            logger.info(f"DATA of {player1}: {data1}")
        if response2.status_code == 200:
            data2 = response2.json()
            logger.info(f"DATA of {player2}: {data2}")

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
            logger.info(f"s:{S}")
            E_A = 1 / (1 + 10 ** ((R_B - R_A) / 400))
            R_A_prime = R_A + K * (S - E_A)
            return (R_A_prime)
        
        # Classements initiaux
        R_joueur_1 = 1500
        R_joueur_2 = 1600

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
        
        K = 0
        if (5 - diff == 5):
            K = 40
        elif (5 - diff == 4):
            K = 35
        elif (5 - diff == 3):
            K = 30
        elif (5 - diff == 3):
            K = 20
        elif (5 - diff == 3):
            K = 10

        # Le joueur 1 gagne
        R_joueur_1_prime = calculer_elo(R_joueur_1, R_joueur_2, K, S_joueur_1)

        # Le joueur 2 perd
        S_joueur_2 = 0
        R_joueur_2_prime = calculer_elo(R_joueur_2, R_joueur_1, K, S_joueur_2)

        logger.info(f"Nouveau classement du joueur 1 : {player1} {R_joueur_1_prime}")
        logger.info(f"Nouveau classement du joueur 2 : {player2} {R_joueur_2_prime}")


        # # response = requests.get(url, headers=headers)
        # logger.info("Return: ", response.status_code , response.json())

        
        # game_data = {
        #         "player1_score": score1,
        #         "player2_score": score2,
        #     #  "rank_player1_begin": 10,
        #     #  "rank_player2_begin": 10,
        #         "rank_player1_change": -10,
        #         "rank_player2_change": 10,
        #         "type": "solo",
        #         "player1": data1.get("id"),
        #         "player2": data2.get("id"),
        #         "winner": 3,
        #         "loser": 2
        #     }

        # def prog_data():
        #     return {
        #         "stat_pong_solo_rank": -10,
        #         "stat_pong_solo_progress": -10
        #     }




        # gamedata = game_data()
        # gamedata["player1"] = response.json().get('id')
        # print (gamedata)

        # response = requests.post(url, headers=headers, json=gamedata)


        # # response = requests.get(url, headers=headers)

        # if response.status_code >= 200:
        #     print("Return: ", response.status_code , response.json())

        # response = requests.patch(url3, headers=headers, json=prog_data())


        # # response = requests.get(url, headers=headers)

        # if response.status_code >= 200:
        #     print("Return: ", response.status_code , response.json())


