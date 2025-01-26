<template>
    <div class="template">
        <HeaderOrganism />
    <div class="page-container">
      <h1>Friends</h1>
      <div class="friends-list">
        <ul>
          <li v-for="(friend, index) in friends" :key="index">
            {{ friend.name }}
            <button @click="removeFriend(index)">Remove</button>
          </li>
        </ul>
      </div>
      <div class="add-friend">
        <input
          type="text"
          v-model="newFriend"
          placeholder="Add a friend"
          @keyup.enter="addFriend"
        />
        <button @click="addFriend">Add</button>
      </div>
    </div>
    <FooterOrganism />
    </div>
  </template>
  
  <script>
    import HeaderOrganism from "@/components/header/navbar.vue";
    import FooterOrganism from "@/components/footer.vue";

  export default {
    components: {
      HeaderOrganism,
      FooterOrganism,
    },
    data() {
      return {
        friends: [
          { name: "Alice" },
          { name: "Bob" },
          { name: "Charlie" },
        ],
        newFriend: "",
      };
    },
    methods: {
      addFriend() {
        if (this.newFriend.trim()) {
          this.friends.push({ name: this.newFriend.trim() });
          this.newFriend = "";
        }
      },
      removeFriend(index) {
        this.friends.splice(index, 1);
      },
    },
  };
  </script>
  
  <style scoped>
  .page-container {
    padding: 20px;
    color: white;
  }
  
  .friends-list ul {
    list-style: none;
    padding: 0;
  }
  
  .friends-list li {
    padding: 10px;
    background-color: #444;
    margin: 10px 0;
    border-radius: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .add-friend {
    margin-top: 20px;
  }
  
  .add-friend input {
    padding: 10px;
    border-radius: 5px;
    border: 1px solid #555;
    margin-right: 10px;
  }
  
  .add-friend button {
    padding: 10px 20px;
    background-color: #4caf50;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  .add-friend button:hover {
    background-color: #3e8e41;
  }
  </style>
  