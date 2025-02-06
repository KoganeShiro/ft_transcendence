<template>
    <div class="modal-overlay" @click.self="closePopup">
      <div class="modal">
        <h1>{{ $t("loss") }}</h1>
        <!-- Loser's avatar and name -->
        <AvatarAtom 
          :pseudo="loserName" 
          :imageUrl="loserImage" 
          :showPseudo="true" 
          pseudoPosition="bottom" 
        />
        <router-link class="return-link" to="/profile">{{ $t("profile") }}</router-link>
      </div>
    </div>
  </template>
  
  <script>
  import AvatarAtom from "@/components/atoms/Avatar.vue";
  
  export default {
    name: "LoserPopup",
    components: {
      AvatarAtom,
    },
    data() {
      return {
        loserName: "Try Again", // Replace with dynamic data if needed
        loserImage: "",         // URL for the loser's image; if empty, AvatarAtom uses its default
      };
    },
    methods: {
      closePopup() {
        // Navigate to the home page or close the modal by other means
        this.$router.push("/");
        // Alternatively, emit an event: this.$emit('close');
      },
    },
  };
  </script>
  
  <style scoped>
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 2000;
  }
  
  .modal {
    background: var(--card-color);
    padding: 20px;
    border-radius: 8px;
    position: relative;
    text-align: center;
    width: 90%;
    max-width: 400px;
  }
  
  .close-btn {
    position: absolute;
    top: 10px;
    right: 10px;
    background: none;
    border: none;
    font-size: 24px;
    line-height: 1;
    cursor: pointer;
  }
  
  .return-link {
    display: inline-block;
    margin-top: 20px;
    padding: 10px 20px;
    background-color: #007bff;
    color: #fff;
    text-decoration: none;
    border-radius: 5px;
  }
  
  .return-link:hover {
    opacity: 0.9;
  }
  </style>
  