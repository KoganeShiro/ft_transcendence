<template>
  <div class="page-container">
    <h1>Friends</h1>
    <div class="friends-list">
      <ul>
        <li v-for="(friend, index) in friends" :key="index">
          {{ friend.name }}
          <!-- <button @click="removeFriend(index)" class="remove-btn">Remove</button> -->
          <ButtonAtom variant="attention" @click="removeFriend(index)" class="remove-btn">Remove</ButtonAtom>
        </li>
      </ul>
    </div>
    <div class="add-friend">
      <AddFriend :friends="friends" @add-friend="addFriend" />
    </div>
  </div>
</template>

<script>
import AddFriend from "@/components/profile/AddFriend.vue";
import ButtonAtom from "@/components/atoms/Button.vue";

export default {
  components: {
    AddFriend,
    ButtonAtom,
  },
  data() {
    return {
      friends: [
        { name: "Alice" },
        { name: "Bob" },
        { name: "Charlie" },
      ],
    };
  },
  methods: {
    addFriend(newFriend) {
      this.friends.push(newFriend);
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
  border-radius: 5px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.remove-btn {
  color: white;
  border: none;
  border-radius: 5px;
  padding: 5px 10px;
  cursor: pointer;
}

</style>
