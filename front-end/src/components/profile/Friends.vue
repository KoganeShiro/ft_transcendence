<template>
  <div class="page-container">
    <h1>{{ $t("friends") }}</h1>
    <!-- Loading indicator (if you decide to use one) -->
    <!-- <div v-if="isLoading">Loading...</div> -->

    <div class="friends-list">
      <ul>
        <li v-for="(friend, index) in friends" :key="friend.id">
          <div class="friend-info" @click="openChat(friend)">
            <!-- Online/Offline status dot -->
            <span
              class="status-dot"
              :class="{ online: friend.online, offline: !friend.online }"
            ></span>
            <span class="friend-name">{{ friend.name }}</span>
          </div>
          <!-- Remove Friend Button -->
          <ButtonAtom
            variant="attention"
            @click="removeFriend(index)"
            class="remove-btn"
          >
            {{ $t("block") }}
          </ButtonAtom>
        </li>
      </ul>
    </div>

    <div class="add-friend">
      <AddFriend :friends="friends" @add-friend="addFriend" />
    </div>

    <!-- Prototype: Chat component is conditionally rendered when a friend is selected -->
    <ChatComponent
      v-if="activeChatFriend"
      :friend="activeChatFriend"
      @close-chat="activeChatFriend = null"
    />
  </div>
</template>

<script>
import AddFriend from "@/components/profile/AddFriend.vue";
import ButtonAtom from "@/components/atoms/Button.vue";
import ChatComponent from "@/components/profile/Chat.vue";
export default {
  components: {
    AddFriend,
    ButtonAtom,
    ChatComponent,
  },
  data() {
    return {
      // Prototype list with hardcoded friends. In a real app, you'll call the backend
      // to fetch this list and update these objects accordingly.
      friends: [
        { id: 1, name: "Alice", online: true },
        { id: 2, name: "Bob", online: false },
        { id: 3, name: "Charlie", online: true },
      ],
      // isLoading: false, // Uncomment if you decide to handle a loading state
      activeChatFriend: null, // Stores the selected friend for chat
    };
  },
  mounted() {
    // PROTOTYPE: Here is where you would call the backend to get the list of friends.
    // Example using Axios:
    // this.isLoading = true;
    // axios.get('/api/friends')
    //   .then(response => {
    //     // Assume response.data is an array of friends with { id, name, online } fields
    //     this.friends = response.data;
    //   })
    //   .catch(error => console.error('Error fetching friends:', error))
    //   .finally(() => { this.isLoading = false; });
  },
  methods: {
    addFriend(newFriend) {
      // PROTOTYPE: In a real app, call the backend to add the friend and then update the list.
      // axios.post('/api/friends', newFriend)
      //   .then(response => {
      //     // Assume response.data is the newly added friend
      //     this.friends.push(response.data);
      //   })
      //   .catch(error => console.error('Error adding friend:', error));
      this.friends.push({
        id: Date.now(), // Prototype unique id
        name: newFriend.name,
        online: false, // Default status
      });
    },
    removeFriend(index) {
      // PROTOTYPE: In a real app, call the backend to remove the friend before updating the list.
      // axios.delete(`/api/friends/${this.friends[index].id}`)
      //   .then(() => {
      //     this.friends.splice(index, 1);
      //   })
      //   .catch(error => console.error('Error removing friend:', error));
      this.friends.splice(index, 1);
    },
    openChat(friend) {
      // Open the chat component with the selected friend
      this.activeChatFriend = friend;
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
}
</style>
