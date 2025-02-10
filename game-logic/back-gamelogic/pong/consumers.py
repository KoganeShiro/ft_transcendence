import json
import asyncio
import time
import random
from channels.generic.websocket import AsyncWebsocketConsumer
import uuid  

active_games = {}
class PongConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_id = str(uuid.uuid4())  # Générer un ID unique pour chaque partie
        self.room_group_name = f"pong_{self.game_id}"  # Créer un groupe unique pour chaque partie
        self.game_loop_task = None  
        self.game_speed = 0.04  
        self.initial_ball_velocity_x = 0.01 * random.choice([-1, 1])
        self.initial_ball_velocity_y = 0  
        self.ball_speed_factor = 30  
        self.paddle_speed = 0.01  
        self.max_paddle_speed = 0.05  
        self.acceleration_rate = 0.002  
        self.deceleration_rate = 0.002  
        self.paddle_acceleration_left = 0
        self.paddle_acceleration_right = 0
        self.player1_socket = None  
        self.player2_socket = None 
        self.score_tab = [[0, 0]] #tableau pour suivre la progression des scores
        self.ready_event = asyncio.Event()  # Ajout d'un événement pour attendre 2 joueurs

        #definition des stats 
        self.game_statistic = {
            "rank": 0,
            "won_under5": 0,
            "lost_under5": 0,
            "won_under10": 0,
            "lost_under10": 0,
            "won_upper10": 0,
            "lost_upper10": 0,

        }
        
        # Définition de l'état du jeu ici
        self.game_state = {
            "ball_x": 0.5,
            "ball_y": 0.5,
            "ball_velocity_x": self.initial_ball_velocity_x,
            "ball_velocity_y": self.initial_ball_velocity_y,
            "player1_y": 0.5,
            "player2_y": 0.5,
            "score1": 0,
            "score2": 0,
        }

    async def connect(self):
        """ Gérer la connexion des joueurs et l'affectation aux parties """
        await self.accept()
        # print(game)
            # Vérifier s'il existe une partie en attente d'un deuxième joueur
        for game_id, game in active_games.items():
            if game["player1_socket"] and not game["player2_socket"]:
                self.game_id = game_id  # On récupère bien le game_id existant
                self.room_group_name = f"pong_{self.game_id}"
                active_games[self.game_id]["player2_socket"] = self.channel_name
                self.player2_socket = self.channel_name

                # print(f"👤 Joueur 2 rejoint la room {self.room_group_name}")

                # Ajouter le joueur au groupe et démarrer la partie
                await self.channel_layer.group_add(self.room_group_name, self.channel_name)
                # print(f"✅ group_add - Consumer {self.channel_name} AJOUTÉ au groupe {self.room_group_name}") # LOG CONFIRMATION GROUP_ADD JOUEUR 2
                await self.send(text_data=json.dumps({
                    'type': 'role_assignment', # Type de message optionnel, mais bonne pratique
                    'role': 'player2',
                }))
                # print(f"WebSocket CONNECT - Joueur {self.channel_name} rejoint le groupe {self.room_group_name}") # LOG ESSENTIEL - CONFIRMATION AJOUT AU GROUPE
                
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "players_ready",  # Nouveau type de message pour signaler que 2 joueurs sont prêts
                        "message": "Deux joueurs connectés, la partie peut commencer !" # Message optionnel
                    }
                )
                # print(f"📢 group_send 'players_ready' envoyé au groupe {self.room_group_name}") # LOG DE CONFIRMATION DE L'ENVOI DU MESSAGE AU GROUPE

                
                await self.start_game()
                return  # Stop ici pour éviter de recréer une partie

        # Si aucune partie en attente, créer une nouvelle
        self.game_id = str(uuid.uuid4())  # Uniquement si pas de partie existante
        self.room_group_name = f"pong_{self.game_id}"
        active_games[self.game_id] = {
            "player1_socket": self.channel_name,
            "player2_socket": None,
            "game_state": self.game_state,
        }
        self.player1_socket = self.channel_name
        await self.send(text_data=json.dumps({
            'type': 'role_assignment', # Type de message optionnel, mais bonne pratique
            'role': 'player1',
        }))
        # print(f"🆕 Nouvelle partie créée {self.game_id}, en attente du joueur 2")
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        # print(f"✅ group_add - Consumer {self.channel_name} AJOUTÉ au groupe {self.room_group_name}") # LOG CONFIRMATION GROUP_ADD JOUEUR 1

    async def receive(self, text_data):
        """ Gérer les entrées des joueurs indépendamment """
        text_data_json = json.loads(text_data)
        moves = 'null'
        player = 'null'
        
        type_message = text_data_json.get('type') # Récupérer le type de message (optionnel)
    
        # if type_message == "init":
            # print(f"INIT message :{text_data_json}")
        
        if type_message == "moves":
            # print(f"Moves : {text_data}")
            player = text_data_json.get('player')
            moves = text_data_json.get('moves')
        
        # print(f"Message reçu par {self.channel_name}- Groupe: {self.room_group_name} - Message: {text_data_json}")  # Affiche le message reçu

        if self.channel_name == self.player1_socket:
            await self.handle_player_moves(moves, player)
        elif self.channel_name == self.player2_socket:
            await self.handle_player_moves(moves, player)

        # Mettre à jour l'état du jeu avec la référence correcte
        game = active_games.get(self.game_id)
        if game:
            game_state = game.get("game_state")
            if game_state:
                
                # print(f"Envoyer l'état du jeu à tous les joueurs depuis {self.channel_name}")
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        "type": "game_update",
                        "game_state": game_state  # Envoi de l'état du jeu à partir de active_games
                    }
                )

    async def start_game(self):
        """ Démarre la partie lorsque deux joueurs sont connectés """
        # print("🎮 Démarrage du jeu !")
        self.game_loop_task = asyncio.create_task(self.game_loop())

        
    def reset_ball(self, direction): # <--- AJOUT DE LA MÉTHODE reset_ball CÔTÉ SERVEUR
        self.game_state["ball_x"] = 0.5
        self.game_state["ball_y"] = 0.5
        self.game_state["player1_y"] = 0.5
        self.game_state["player2_y"] = 0.5
        self.game_state["ball_velocity_x"] = 0.01 * direction  # IDENTIQUE AU CLIENT (0.01)
        self.game_state["ball_velocity_y"] = 0
        self.ball_speed_factor = self.initial_ball_speed # Utiliser self.initial_ball_speed, défini dans __init__

    # async def game_update(self, event):
    #     """ Envoyer les mises à jour du jeu aux joueurs """
    #     # await self.send(text_data=json.dumps({
    #     #     "game_state": event["game_state"]
    #     # }))
    
    async def handle_player_moves(self, move, player):
        # print(f"DEBUT handle_player_moves - player: {player}, moves: {move}") # LOG DÉBUT
        # print(f"🔵 SERVEUR - DEBUT handle_player_moves - player: {player}, moves: {move}") # LOG DÉBUT
        # print(f"ℹ️ SERVEUR - game_state BEFORE move processing: {self.game_state}") # ADD THIS LOG - GAME STATE BEFORE

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
        # print(f"🔴 SERVEUR - FIN handle_player_moves - game_state AFTER movements de {player}: {self.game_state}") # LOG FIN
        # print(f"FIN handle_player_moves - game_state après mouvements: {self.game_state}") # LOG FIN


    async def game_loop(self):
        # print("DEBUT game_loop") # LOG DÉBUT
        previous_time = time.time()

        while True:
            current_time = time.time()
            delta_time = current_time - previous_time
            previous_time = current_time

            await asyncio.sleep(0.1)

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
                        self.ball_speed_factor = min(80, self.ball_speed_factor + 5)

            elif self.game_state["ball_x"] >= 0.95:
                # print("touch right")
                if self.game_state["ball_velocity_x"] > 0:
                    if (self.game_state["player2_y"] - 0.1 <= self.game_state["ball_y"] <= self.game_state["player2_y"] + 0.1):
                        self.game_state["ball_velocity_x"] *= -1
                        self.game_state["ball_velocity_y"] = (self.game_state["ball_y"] - self.game_state["player2_y"]) * 0.1
                        self.ball_speed_factor = min(80, self.ball_speed_factor + 5)

            # Gestion des scores
            if self.game_state["ball_x"] <= 0:
                self.game_state["score2"] += 1
                self.score_tab.append([self.game_state["score1"], self.game_state["score2"]])
                self.reset_ball(1)
                self.game_state["ball_velocity_x"] = abs(self.game_state["ball_velocity_x"])

            elif self.game_state["ball_x"] >= 1:
                self.game_state["score1"] += 1
                self.reset_ball(-1)
                self.game_state["ball_velocity_x"] = -abs(self.game_state["ball_velocity_x"])

            # print(f"game_loop - game_state avant update_game_state: {self.game_state}") # LOG ÉTAT DU JEU
            await self.update_game_state()
        
        # print("FIN game_loop") # LOG FIN (devrait ne pas être atteint en boucle infinie)


    async def update_game_state(self):
        message = {
                "type": "game_update",
                "game_state": self.game_state
        }
        await self.channel_layer.group_send(
            self.room_group_name,  # Nom du groupe auquel envoyer le message
            message  # Le message à envoyer
        )
        print(f"🟢 Message: {message}") # LOG DE RÉCEPTION CÔTÉ SERVEUR

            

    def calculate_ball_angle(self, ball_y, paddle_y):
            # Calculer l'écart entre la balle et le centre du paddle
        distance_from_center = ball_y - paddle_y

            # Plus l'écart est grand, plus l'angle de rebond sera large
        angle = distance_from_center * 0.1  # Ajuster ce coefficient pour affiner l'angle
        return angle
    
    
    async def players_ready(self, event):
        message = event['message'] # Récupérer le message optionnel
        # print(f"🟢 RECUE du message 'players_ready' par {self.channel_name} - Message: {message}") # LOG DE RÉCEPTION CÔTÉ SERVEUR
        await self.send(text_data=json.dumps({
            "type": "players_ready",
            "message": message
        }))
        
    async def game_update(self, event):
        """ Gérer le message 'game_update' diffusé au groupe """
        game_state = event['game_state'] # Récupérer l'état du jeu du message
        # print(f"🔄 RECUE du message 'game_update' par {self.channel_name} - game_state: {game_state}") # LOG DE RÉCEPTION CÔTÉ SERVEUR
        message = {
                        "type": "game_update",
                        "game_state": game_state
                }
        # ENVOYER le message 'game_update' (avec l'état du jeu) au CLIENT WEBSOCKET CONNECTÉ à CE CONSUMER (en utilisant self.send())
        await self.send(text_data=json.dumps({
            "type": "game_update",
            "game_state": game_state 
        }))
        print(f"🔄 {message}")