import json
import random
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    tab = []  # Liste des messages, avec les ids des utilisateurs

    async def connect(self):
        self.room_name = 'chat_room'
        self.room_group_name = f'chat_{self.room_name}'

        # Générer un identifiant unique pour l'utilisateur
        self.user_id = f'user{random.randint(1, 1000)}'  # Exemple d'ID comme 'user1', 'user2', etc.

        # Rejoindre la salle de chat
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Accepter la connexion WebSocket
        await self.accept()

        # Envoyer l'historique des messages avec les ids d'utilisateur
        await self.send(text_data=json.dumps({
            'historic': [{'user': msg['user'], 'message': msg['message']} for msg in ChatConsumer.tab]
        }))

    async def disconnect(self, close_code):
        # Quitter la salle de chat
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Ajouter le message avec l'identifiant utilisateur
        ChatConsumer.tab.append({'user': self.user_id, 'message': message})

        # Envoyer le message à la salle de chat
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'user': self.user_id,
                'message': message
            }
        )

    async def chat_message(self, event):
        # Récupérer le message et l'utilisateur
        user = event['user']
        message = event['message']

        # Envoyer le message au WebSocket
        await self.send(text_data=json.dumps({
            'user': user,
            'message': message
        }))
