import json
import asyncio
import time 
from channels.generic.websocket import AsyncWebsocketConsumer
import uuid  # Pour générer un identifiant unique


class PongConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_loop_task = None  # Pour gérer la boucle de jeu
        self.game_speed = 0.04  # Vitesse initiale de mise à jour du jeu
        self.initial_ball_velocity_x = 0.01  # Vitesse initiale horizontale de la balle
        self.initial_ball_velocity_y = 0  # Vitesse initiale verticale de la balle
        self.ball_speed_factor = 30  # Facteur de vitesse de la balle, commence à 30
        self.paddle_speed = 0.01  # Vitesse initiale du paddle
        self.max_paddle_speed = 0.05  # Limite supérieure de la vitesse du paddle
        self.acceleration_rate = 0.002  # Vitesse à laquelle la vitesse du paddle augmente
        self.deceleration_rate = 0.002  # Vitesse à laquelle la vitesse du paddle diminue
        self.paddle_speed_left = self.paddle_speed
        self.paddle_speed_right = self.paddle_speed
        self.paddle_acceleration_left = 0
        self.paddle_acceleration_right = 0

    async def connect(self):
        # Chaque joueur a son propre jeu_id unique
        self.game_id = str(uuid.uuid4())  # Génère un identifiant unique pour chaque jeu
        self.room_name = f"pongroom_{self.game_id}"  # Utiliser game_id pour chaque instance de jeu
        self.room_group_name = f"pong_{self.room_name}"

        # Joindre le groupe du jeu
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

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

        await self.accept()

        # Démarrer la boucle de jeu pour cette instance unique
        self.game_loop_task = asyncio.create_task(self.game_loop())

    async def disconnect(self, close_code):
        # Quitter le groupe du jeu
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        # Annuler la boucle de jeu si elle existe
        if self.game_loop_task:
            self.game_loop_task.cancel()
            await self.game_loop_task  # Attendre que la tâche soit annulée correctement

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        moves = text_data_json.get('moves', {})  # Récupérer toutes les touches pressées

        # Déplacer le joueur 1 (gauche)
        if moves.get("up_left", False):
            self.paddle_acceleration_left = min(self.paddle_acceleration_left + self.acceleration_rate, self.max_paddle_speed)
            self.game_state["player1_y"] = max(self.game_state["player1_y"] - self.paddle_acceleration_left, 0)

        if moves.get("down_left", False):
            self.paddle_acceleration_left = min(self.paddle_acceleration_left + self.acceleration_rate, self.max_paddle_speed)
            self.game_state["player1_y"] = min(self.game_state["player1_y"] + self.paddle_acceleration_left, 1)

        if not (moves.get("up_left", False) or moves.get("down_left", False)):
            self.paddle_acceleration_left = self.paddle_speed

        # Gestion du paddle droit (joueur 2)
        if moves.get("up_right", False):
            self.paddle_acceleration_right = min(self.paddle_acceleration_right + self.acceleration_rate, self.max_paddle_speed)
            self.game_state["player2_y"] = max(self.game_state["player2_y"] - self.paddle_acceleration_right, 0)

        if moves.get("down_right", False):
            self.paddle_acceleration_right = min(self.paddle_acceleration_right + self.acceleration_rate, self.max_paddle_speed)
            self.game_state["player2_y"] = min(self.game_state["player2_y"] + self.paddle_acceleration_right, 1)

        if not (moves.get("up_right", False) or moves.get("down_right", False)):
            self.paddle_acceleration_right = self.paddle_speed

        # Envoyer la mise à jour à tous les joueurs
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "game_update",
                "game_state": self.game_state
            }
        )

    async def game_update(self, event):
        """ Envoie l'état du jeu mis à jour à tous les joueurs. """
        await self.send(text_data=json.dumps({
            "game_state": event["game_state"]
        }))

    async def game_loop(self):
        previous_time = time.time()

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
                self.game_state["ball_y"] = 0  # Assure que la balle ne dépasse pas la limite
                self.game_state["ball_velocity_y"] = -self.game_state["ball_velocity_y"]  # Inverse la direction verticale

            elif self.game_state["ball_y"] >= 1:
                self.game_state["ball_y"] = 1  # Assure que la balle ne dépasse pas la limite
                self.game_state["ball_velocity_y"] = -self.game_state["ball_velocity_y"]  # Inverse la direction verticale

            # Collision avec le paddle gauche (joueur 1)
            if self.game_state["ball_x"] <= 0.05:  # Balle à gauche, avec joueur 1
                if self.game_state["ball_velocity_x"] < 0 and self.game_state["ball_x"] <= 0.05:
                    if self.game_state["player1_y"] - 0.1 <= self.game_state["ball_y"] <= self.game_state["player1_y"] + 0.1:
                        self.game_state["ball_velocity_x"] = -self.game_state["ball_velocity_x"]  # Inverser la direction horizontale
                        
                        # Calculer l'angle de rebond en fonction de la position de la balle sur le paddle
                        self.game_state["ball_velocity_y"] = self.calculate_ball_angle(self.game_state["ball_y"], self.game_state["player1_y"])

                        # Augmenter la vitesse de la balle
                        self.ball_speed_factor = min(80, self.ball_speed_factor + 5)
                        print(f"Facteur de vitesse de la balle après rebond sur paddle gauche: {self.ball_speed_factor}")

            # Collision avec le paddle droit (joueur 2)
            elif self.game_state["ball_x"] >= 0.95:  # Balle à droite, avec joueur 2
                if self.game_state["ball_velocity_x"] > 0 and self.game_state["ball_x"] >= 0.95:
                    if self.game_state["player2_y"] - 0.1 <= self.game_state["ball_y"] <= self.game_state["player2_y"] + 0.1:
                        self.game_state["ball_velocity_x"] = -self.game_state["ball_velocity_x"]  # Inverser la direction horizontale
                        
                        # Calculer l'angle de rebond en fonction de la position de la balle sur le paddle
                        self.game_state["ball_velocity_y"] = self.calculate_ball_angle(self.game_state["ball_y"], self.game_state["player2_y"])

                        # Augmenter la vitesse de la balle
                        self.ball_speed_factor = min(80, self.ball_speed_factor + 5)
                        print(f"Facteur de vitesse de la balle après rebond sur paddle droit: {self.ball_speed_factor}")

            # Gestion des scores
            if self.game_state["ball_x"] <= 0:
                self.game_state["score2"] += 1
                self.game_state["ball_x"] = 0.5  # Réinitialiser la balle
                self.game_state["ball_y"] = 0.5
                self.game_state["ball_velocity_x"] = self.initial_ball_velocity_x  # Réinitialiser la vitesse horizontale
                self.game_state["ball_velocity_y"] = self.initial_ball_velocity_y  # Réinitialiser la vitesse verticale
                self.ball_speed_factor = 30  # Réinitialiser la vitesse du jeu
                self.game_state["player1_y"] = 0.5  # Réinitialiser le paddle gauche
                self.game_state["player2_y"] = 0.5  # Réinitialiser le paddle droit
                self.game_state["ball_velocity_x"] = -abs(self.game_state["ball_velocity_x"])  # La balle part vers le joueur qui a marqué
                print(f"Point marqué! Score1: {self.game_state['score1']} - Score2: {self.game_state['score2']}")
                print(f"Vitesse de la balle réinitialisée : {self.ball_speed_factor}")

            elif self.game_state["ball_x"] >= 1:
                self.game_state["score1"] += 1
                self.game_state["ball_x"] = 0.5  # Réinitialiser la balle
                self.game_state["ball_y"] = 0.5
                self.game_state["ball_velocity_x"] = self.initial_ball_velocity_x  # Réinitialiser la vitesse horizontale
                self.game_state["ball_velocity_y"] = self.initial_ball_velocity_y  # Réinitialiser la vitesse verticale
                self.ball_speed_factor = 30  # Réinitialiser la vitesse du jeu
                self.game_state["player1_y"] = 0.5  # Réinitialiser le paddle gauche
                self.game_state["player2_y"] = 0.5  # Réinitialiser le paddle droit
                self.game_state["ball_velocity_x"] = abs(self.game_state["ball_velocity_x"])  # La balle part vers le joueur qui a marqué
                print(f"Point marqué! Score1: {self.game_state['score1']} - Score2: {self.game_state['score2']}")
                print(f"Vitesse de la balle réinitialisée : {self.ball_speed_factor}")

            # Envoyer l'état du jeu uniquement pour ce client et ce jeu
            await self.update_game_state()

    def calculate_ball_angle(self, ball_y, paddle_y):
        # Calculer l'écart entre la balle et le centre du paddle
        distance_from_center = ball_y - paddle_y

        # Plus l'écart est grand, plus l'angle de rebond sera large
        angle = distance_from_center * 0.1  # Ajuster ce coefficient pour affiner l'angle
        return angle

    async def update_game_state(self):
        # Envoie l'état du jeu uniquement à ce client
        await self.send(text_data=json.dumps({
            'game_state': self.game_state
        }))