<template>
  <div class="chat-container">
    <!-- Chat Header -->
    <div class="chat-header">
      <router-link :to="`/other_profile/${friend.name}`" class="friend-profile">
        <div class="avatar-image">
          <img :src="friend.avatar" alt="Avatar" class="friend-avatar" />
        </div>
        <h2>{{ friend.name }}</h2>
      </router-link>
      <button class="close-btn" @click="closeChat">X</button>
    </div>

    <!-- Chat Messages -->
    <div class="chat-messages">
      <div
        v-for="(message, index) in messages"
        :key="index"
        :class="['chat-message', message.sender === 'me' ? 'sent' : 'received']"
      >
        <p>{{ message.text }}</p>
        <span class="timestamp">{{ message.timestamp }}</span>
      </div>
    </div>

    <!-- Chat Input -->
    <div class="chat-input">
      <input
        type="text"
        v-model="newMessage"
        placeholder="Type a message..."
        @keyup.enter="sendMessage"
      />
      <button @click="sendMessage">{{ $t("send") }}</button>
    </div>
  </div>
</template>

<script>
import Avatar from "@/assets/profile.png";
import API from "@/api.js"

export default {
  name: "ChatComponent",
  props: {
    friend: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      messages: [
        // Prototype messages. In a real app, you might fetch these from your backend.
        { text: "Hi there!", sender: "friend", timestamp: "10:00 AM" },
        { text: "Hello!", sender: "me", timestamp: "10:01 AM" },
      ],
      newMessage: "",
    };
  },
  mounted() {
    // PROTOTYPE: Call your backend to load the conversation with this friend.
    // Example using Axios:
    // axios.get(`/api/chat/${this.friend.id}`)
    //   .then(response => {
    //     this.messages = response.data;
    //   })
    //   .catch(error => console.error("Error loading chat:", error));
    this.getAvatar();
  },
  methods: {
    getAvatar() {
      API.get(`/api/profile/${this.friend.name}`)
      .then(response => {
        if (response.data && response.data.cover_photo) {
          this.friend.avatar = response.data.cover_photo;
        } else {
          this.friend.avatar = Avatar;
        }
      })
      .catch(error => {
        console.error("Error fetching friend's cover photo:", error);
      });
    },
    sendMessage() {
      if (!this.newMessage.trim()) return;

      // should call the backend to send the message
      const message = {
        text: this.newMessage,
        sender: "me",
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      this.messages.push(message);

      //api/friends/send_message/
      /*
        {"receiver" : "moi"
        "message" : "hey, want to play pong together ?"}
      */

      // PROTOTYPE: Here you would call your backend to send the message.
      // axios.post(`/api/chat/${this.friend.id}`, { message: this.newMessage })
      //   .then(response => {
      //     // Optionally update your messages list with the response
      //   })
      //   .catch(error => console.error("Error sending message:", error));

      // Clear the input field
      this.newMessage = "";
    },
    closeChat() {
      // Emit an event to the parent to close the chat component
      this.$emit("close-chat");
    },
  },
};
</script>

<style scoped>
.chat-container {
  position: fixed;
  right: 20px;
  top: 50%;
  transform: translateY(-50%);
  width: 600px;
  max-height: 500px;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  background: var(--chat-header-bg, #f1f1f1);
}

/* Chat header styling */
.chat-header {
  background: var(--chat-header-bg, #f1f1f1);
  padding: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-radius: 8px 8px 0 0;
}

.friend-profile {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: inherit;
}

.avatar-image {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  overflow: hidden;
  margin-right: 10px;
}

.avatar-image img {
  width: 90%;
  height: 90%;
  object-fit: cover;
}

.friend-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 15px;
}

.chat-header h2 {
  margin: 0;
  font-size: 18px;
}

/* Close button styling */
.close-btn {
  background: none;
  border: none;
  font-size: 16px;
  cursor: pointer;
  color: var(--icon-color, #333);
  font-weight: bold;
}

/* Chat messages styling */
.chat-messages {
  flex: 1;
  padding: 10px;
  overflow-y: auto;
  background: var(--chat-messages-bg, #fafafa);
}

.chat-message {
  margin-bottom: 10px;
  max-width: 70%;
  padding: 3px;
  border-radius: 13px;
  font-size: 18px;
}

.chat-message.sent {
  background-color: var(--msg-send, #daf1da);
  align-self: flex-end;
  margin-left: 55px;
}

.chat-message.received {
  background-color: var(--msg-receive, #e0e0e0);
  align-self: flex-start;
}

.timestamp {
  display: block;
  font-size: 13px;
  color: var(--text-color);
  margin-top: 2px;
  text-align: right;
  margin-right: 5px;
}

/* Chat input styling */
.chat-input {
  display: flex;
}

.chat-input input {
  flex: 1;
  padding: 10px;
  border: none;
  outline: none;
  border-radius: 0 0 0 8px;
}

.chat-input button {
  padding: 0 15px;
  border: none;
  background: var(--chat-send-bg, #007bff);
  color: var(--text-color, #fff);
  font-weight: bold;
  border-radius: 0 0 8px 0;
  cursor: pointer;
}

/* Responsive adjustments */
@media (max-width: 750px) {
  .chat-container {
    right: 5%;
    width: 65%;
    top: 55%;
    transform: translateY(-50%);
    max-height: 400px;
  }
}
</style>