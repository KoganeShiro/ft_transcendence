<template>
    <div class="add-friend">
      <div class="add-friend-form">
        <input
          type="text"
          v-model="newFriend"
          :placeholder="$t('addFriend')"
          @keyup.enter="addFriend"
          class="add-friend-input"
        />
        <ButtonAtom @click="addFriend" class="add-friend-btn">{{ $t("add") }}</ButtonAtom>
      </div>
    </div>
  </template>
  
  <script>
  import ButtonAtom from "@/components/atoms/Button.vue";
  import { useLanguage } from '@/components/useLanguage.js';

  export default {
    components: {
      ButtonAtom,
    },
    setup() {
    const { changeLanguage } = useLanguage()
    return {
      changeLanguage
    }
  },
    name: "AddFriend",
    props: {
      friends: {
        type: Array,
        required: true,
      },
    },
    data() {
      return {
        newFriend: "",
      };
    },
    methods: {
      addFriend() {
        if (this.newFriend.trim()) {
          // Emit the new friend to the parent component
          this.$emit("add-friend", { name: this.newFriend.trim() });
          this.newFriend = "";
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .add-friend-form {
    display: flex;
    align-items: center;
  }
  
  .add-friend-input {
    flex: 1;
    padding: 10px;
    border-radius: 5px;
    border: 1px solid #555;
    margin-right: 10px;
    background-color: #333;
    color: white;
  }
  
  .add-friend-btn {
    padding: 10px 20px;
    background-color: #4caf50;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  .add-friend-btn:hover {
    background-color: #3e8e41;
  }
  </style>
  