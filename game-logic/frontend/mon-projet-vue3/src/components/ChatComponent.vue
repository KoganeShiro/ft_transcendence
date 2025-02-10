<template>
  <div class="chat-container">
    <!-- Affichage des messages avec l'ID utilisateur -->
    <div v-for="(message, index) in messages" :key="index" class="message">
      <strong>{{ message.user }}:</strong> {{ message.message }}
    </div>
    <!-- Champ de texte pour envoyer un message -->
    <input v-model="message" @keyup.enter="sendMessage" placeholder="Écris un message..." class="message-input">
  </div>
</template>

<script>
export default {
  data() {
    return {
      socket: null,
      message: '',
      messages: [],
    };
  },
  mounted() {
    // Connexion au WebSocket
    this.socket = new WebSocket('ws://localhost:8000/ws/chat/');

    this.socket.onmessage = (event) => {
      const data = JSON.parse(event.data);

      // Mise à jour des messages avec l'utilisateur et le message
      if (data.historic) {
        this.messages = data.historic;  // Historique des messages
      }

      if (data.user && data.message) {
        // Ajouter chaque nouveau message reçu avec l'identifiant de l'utilisateur
        this.messages.push({ user: data.user, message: data.message });
      }
    };

    this.socket.onopen = () => {
      console.log('WebSocket connecté');
    };

    this.socket.onerror = (error) => {
      console.log('WebSocket erreur:', error);
    };

    this.socket.onclose = () => {
      console.log('WebSocket déconnecté');
    };
  },
  methods: {
    sendMessage() {
      if (this.message && this.socket.readyState === WebSocket.OPEN) {
        // Envoi du message avec l'utilisateur
        this.socket.send(JSON.stringify({ message: this.message }));
        this.message = '';  // Réinitialisation du champ de message
      } else {
        console.log("WebSocket n'est pas ouvert ou la connexion est fermée.");
      }
    },
  },
};
</script>

<style scoped>
.chat-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f4f4f4;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.message {
  margin-bottom: 10px;
  padding: 8px;
  background-color: #fff;
  border-radius: 5px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
}

.message-input {
  width: 100%;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ddd;
  margin-top: 20px;
  font-size: 16px;
}
</style>
