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
    <div class="chat-messages" ref="chatMessages">
      <div
        v-for="(message, index) in sortedMessages"
        :key="message.id || index"
        :class="['chat-message', message.sender === friend.name ? 'received' : 'sent']"
      >
        <p>{{ message.text }}</p>
        <span class="timestamp">{{ formattedTimestamp(message.timestamp) }}</span>
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
import API from "@/api.js";
import { format } from "date-fns";

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
      messages: [],
      newMessage: "",
      pollingInterval: null,
      lastReceivedMessageId: null,
      isActive: true,
      isFetchingMessages: false,
      isGetAvatar: false,
    };
  },
  mounted() {
    this.getAvatar();
    this.fetchMessages();
    this.startPolling();
  },
  beforeDestroy() {
    //this.isActive = false;
    this.stopPolling();
  },
  methods: {
    getAvatar() {
      if (this.isGetAvatar) return;
      this.isGetAvatar = true;

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
          this.friend.avatar = Avatar;
        })
        .finally(() => {
          this.isGetAvatar = false;
        });
    },
    // Fetch the last 15 messages for this friend.
    fetchMessages() {
      if (this.isFetchingMessages) return;
      this.isFetchingMessages = true;
      API.post(`/api/friends/get_last_15_messages/`, { username: this.friend.name })
      .then(response => {
        const newMessages = response.data.map(msg => ({
          id: msg.id,
          sender: msg.sender,
          text: msg.message,
          timestamp: msg.timestamp,
        }));
        // Filter only messages received from the friend
        const receivedMessages = newMessages.filter(msg => msg.sender === this.friend.name);
        const lastReceived = receivedMessages.length ? receivedMessages[receivedMessages.length - 1] : null;

        this.messages = newMessages;

        // If there's a new received message that is different from the stored one, scroll to bottom.
        if (lastReceived && lastReceived.id !== this.lastReceivedMessageId) {
          this.lastReceivedMessageId = lastReceived.id;
          this.scrollToBottom();
        }
      })
      .catch(error => {
        console.error("Error fetching messages:", error);
      })
      .finally(() => {
        this.isFetchingMessages = false;
      });
  },

    // Format ISO timestamp to a readable string.
    formattedTimestamp(ts) {
      return new Date(ts).toLocaleDateString() + ' ' + new Date(ts).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: false });    },
    sendMessage() {
      if (!this.newMessage.trim()) return;
      //block the user at 160 characters
      if (this.newMessage.length > 160) {
        this.newMessage = this.newMessage.slice(0, 160);
      }

      // For messages sent by the current user, set sender as "me".
      const message = {
        text: this.newMessage,
        sender: "me",
        timestamp: new Date().toISOString(),
      };
      this.messages.push(message);

      // Send the message to the backend.
      API.post("/api/friends/send_message/", {
        receiver: this.friend.name,
        message: this.newMessage,
      })
        .then(response => {
          console.log("Message sent successfully:", response.data);
          this.scrollToBottom();
        })
        .catch(error => {
          console.error("Error sending message:", error);
        });

      // Clear the input.
      this.newMessage = "";
    },
    closeChat() {
      this.stopPolling();
      this.$emit("close-chat");
    },
    scrollToBottom() {
      this.$nextTick(() => {
        const chatMessages = this.$refs.chatMessages;
        if (chatMessages) {
          chatMessages.scrollTop = chatMessages.scrollHeight;
        }
      });
    },
    startPolling() {
      this.pollingInterval = setInterval(this.fetchMessages, 5000);
    },
    stopPolling() {
      if (this.pollingInterval) {
        clearInterval(this.pollingInterval);
        this.pollingInterval = null;
      }
    },
  },
  computed: {
    sortedMessages() {
      return this.messages.sort(
        (a, b) => new Date(a.timestamp) - new Date(b.timestamp)
      );
    },
  },
  watch: {
    friend(newFriend, oldFriend) {
      if (newFriend !== oldFriend) {
        this.fetchMessages();
      }
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

.content {
  flex: 1;
}

input[type="text"] {
  margin-top: 10px;
  padding: 5px;
  width: calc(100% - 12px);
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  margin-top: 10px;
  padding: 5px 10px;
  border: none;
  background-color: #007bff;
  color: white;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
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