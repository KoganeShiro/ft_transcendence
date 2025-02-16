<template>
  <div class="page-container">
    <h1>{{ $t("friends") }}</h1>
    <div v-if="isLoading">Loading...</div>

    <div class="friends-list" v-else>
      <ul>
        <!-- Dynamically display the friends list -->
        <li v-for="(friend, index) in friends" :key="friend.id">
          <div class="friend-info" @click="openChat(friend)">
            <!-- Online/Offline status dot -->
            <span
              class="status-dot"
              :class="{ online: friend.online, offline: !friend.online }"
            ></span>
            <span class="friend-name">{{ friend.name }}</span>
          </div>
          <!-- Block/Unblock and Remove buttons -->
          <div class="btn-group">
            <ButtonAtom
              v-if="!friend.blocked"
              variant="block"
              @click="block(index)"
              class="remove-btn"
            >
              {{ $t("block") }}
            </ButtonAtom>
            <ButtonAtom
              v-else
              variant="unblock"
              @click="unblock(index)"
              class="remove-btn"
            >
              {{ $t("unblock") }}
            </ButtonAtom>
            <ButtonAtom
              variant="attention"
              @click="removeFriend(index)"
              class="remove-btn"
            >
              {{ $t("remove") }}
            </ButtonAtom>
          </div>
        </li>
      </ul>
    </div>

    <!-- Add Friend Component -->
    <div class="add-friend">
      <AddFriend :friends="friends" @add-friend="addFriend" />
    </div>

    <!-- Chat Component -->
    <ChatComponent
      ref="chatComponent"
      v-if="activeChatFriend"
      :friend="activeChatFriend"
      @close-chat="activeChatFriend = null"
      @fetch-messages="fetchMessages"
    />
  </div>
</template>

<script>
import AddFriend from "@/components/profile/AddFriend.vue";
import ButtonAtom from "@/components/atoms/Button.vue";
import ChatComponent from "@/components/profile/Chat.vue";
import API from "@/api.js";
import Avatar from "@/assets/profile.png";

export default {
  components: {
    AddFriend,
    ButtonAtom,
    ChatComponent,
  },
  data() {
    return {
      isLoading: false,
      friends: [],
      activeChatFriend: null,
      fetchFriendsInterval: null,
      isBlocking: false,
      isUnblocking: false,
      isRemoving: false,
    };
  },
  mounted() {
    // Fetch the initial friend list.
    this.fetchFriends();
    this.fetchFriendsInterval = setInterval(this.fetchFriends, 50000);
  },
  beforeDestroy() {
  // Clear the interval when the component is destroyed.
  if (this.fetchFriendsInterval) {
    clearInterval(this.fetchFriendsInterval);
  }
},
  methods: {
    // Helper method to fetch and update the friend list.
    fetchFriends() {
      this.isLoading = true;
      API.get('/api/friends/user_friends/')
        .then(response => {
          // Map the API response to your local friend structure.
          this.friends = response.data.map((friend, index) => ({
            id: index,
            name: friend.username,
            online: friend.online_status,
            blocked: friend.is_blocked,
          }));
        })
        .catch(error => {
          console.error("Error fetching friends:", error);
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    addFriend(newFriend) {
      console.log("Adding friend:", newFriend);
      // POST to /api/friends/add_friend/ with the friend's username.
      API.post('/api/friends/add_friend/', { username: newFriend.name })
        .then(() => {
          console.log("Friend added:", newFriend.name);
          // Refresh the friend list after adding.
          this.fetchFriends();
        })
        .catch(error => {
          console.error("Error adding friend:", error);
        });
    },
    removeFriend(index) {
      if (this.isRemoving) return;
      this.isRemoving = true;

      const friend = this.friends[index];
      API.post('/api/friends/remove_friend/', { username: friend.name })
        .then(() => {
          console.log("Removed friend:", friend.name);
          // Refresh the friend list after removal.
          this.fetchFriends();
        })
        .catch(error => {
          console.error("Error removing friend:", error);
        })
        .finally(() => {
          this.isRemoving = false;
        });
    },
    block(index) {
      if (this.isBlocking) return;
      this.isBlocking = true;

      const friend = this.friends[index];
      API.post('/api/friends/block_user/', { username: friend.name })
        .then(() => {
          console.log("Blocked friend:", friend.name);
          // Refresh the friend list after blocking.
          this.fetchFriends();
        })
        .catch(error => {
          console.error("Error blocking friend:", error);
        })
        .finally(() => {
          this.isBlocking = false;
        });
    },
    unblock(index) {
      if (this.isUnblocking) return;
      this.isUnblocking = true;

      const friend = this.friends[index];
      API.post('/api/friends/unblock_user/', { username: friend.name })
        .then(() => {
          console.log("Unblocked friend:", friend.name);
          // Refresh the friend list after unblocking.
          this.fetchFriends();
        })
        .catch(error => {
          console.error("Error unblocking friend:", error);
        })
        .finally(() => {
          this.isUnblocking = false;
        });
    },
    openChat(friend) {
      this.activeChatFriend = friend;
      this.$nextTick(() => {
        if (this.$refs.chatComponent && this.$refs.chatComponent.getAvatar) {
          this.$refs.chatComponent.getAvatar();
        }
        if (this.$refs.chatComponent && this.$refs.chatComponent.fetchMessages) {
          this.$refs.chatComponent.fetchMessages(friend);
        }
      });
    },
    fetchMessages(friend) {
      if (friend) {
        API.post(`/api/friends/get_last_15_messages/`, { username: friend.name })
          .then(response => {
            friend.messages = response.data.map(msg => ({
              id: msg.id,
              sender: msg.sender,
              text: msg.message,
              timestamp: msg.timestamp,
            }));
          })
          .catch(error => {
            console.error("Error fetching messages:", error);
          });
      }
    },
  },
};
</script>

<style scoped>
.page-container {
  padding: 20px;
  color: var(--text-color);
  margin-bottom: 50px;
}

.friends-list ul {
  list-style: none;
  padding: 0;
}

.friends-list li {
  padding: 10px;
  background-color: var(--text-box-color);
  margin: 10px 0;
  border-radius: 5px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* The friend-info container is clickable.
   We add a hover effect to indicate interactivity. */
.friend-info {
  display: flex;
  align-items: center;
  cursor: pointer;
  flex-grow: 1;
  position: relative;
}

.friend-info:hover {
  transition: transform 0.5s;
  font-weight: bold;

}

/* Friend name styling */
.friend-name {
  margin-left: 10px;
}

/* Online/Offline Status Dot */
.status-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  display: inline-block;
}

.status-dot.online {
  background-color: green;
}

.status-dot.offline {
  background-color: red;
}

.remove-btn {
  color: white;
  border: none;
  border-radius: 5px;
  padding: 5px 10px;
  cursor: pointer;
  margin-right: 7px;
}

@media (max-width: 768px) {
    .btn-group {
      padding: 3px 7px;
      font-size: 15px;
    }
  }

</style>