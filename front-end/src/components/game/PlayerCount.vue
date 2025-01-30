<template>
    <div class="player-count-container">
      <button class="circle-btn" @click="toggleMenu">
        {{ playerCount }}
      </button>
  
      <div v-if="showMenu" class="player-menu">
        <button 
          v-for="num in availablePlayers" 
          :key="num" 
          :class="['player-option', { active: playerCount === num }]"
          @click="selectPlayers(num)"
        >
          {{ num }}
        </button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      modelValue: Number,
      minPlayers: {
        type: Number,
        default: 4,
      },
      maxPlayers: {
        type: Number,
        default: 4,
      },
    },
    data() {
      return {
        showMenu: false,
      };
    },
    computed: {
      playerCount: {
        get() {
          return this.modelValue;
        },
        set(value) {
          this.$emit("update:modelValue", value);
        },
      },
      availablePlayers() {
        return Array.from({ length: this.maxPlayers - this.minPlayers + 1 }, (_, i) => i + this.minPlayers);
      },
    },
    methods: {
      toggleMenu() {
        this.showMenu = !this.showMenu;
      },
      selectPlayers(num) {
        this.playerCount = num;
        this.showMenu = false;
      },
    },
  };
  </script>
  
  <style scoped>
  .player-count-container {
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  /* Circular button */
  .circle-btn {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    border: none;
    background: #717477;
    color: white;
    font-size: 18px;
    font-weight: bold;
    cursor: pointer;
    transition: 0.2s;
  }

  
  /* Player selection menu */
  .player-menu {
    position: absolute;
    top: 70px;
    background: #333;
    border-radius: 10px;
    padding: 10px;
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }
  
  .player-option {
    background: #444;
    color: white;
    border: none;
    padding: 8px 12px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 16px;
    transition: 0.2s;
  }
  
  .player-option:hover {
    background: #666;
  }
  
  </style>
  