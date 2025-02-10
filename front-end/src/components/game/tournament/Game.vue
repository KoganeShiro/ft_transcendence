<template>
    <div class="pong-page">
      <Versus v-if="showVersus" @time-up="handleTimeUp" />
      
      <div v-else class="content">
        <div class="player-controls">
          <h2 class="mobile-hide">{{ $t('commands') }}</h2>
          <p class="mobile-hide">{{ $t('move-up') }}<span class="span">W</span></p>
          <p class="mobile-hide">{{ $t('move-down') }} <span class="span">S</span></p>
        </div>
        <div class="game-container">
          <PongGameComponent @gameEnded="endGame" />
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import PongGameComponent from "@/components/game/pongGame/PongGame.vue";
  import Versus from "@/components/game/Versus.vue";
  
  export default {
    name: 'RemoteFront',
    components: {
      Versus,
      PongGameComponent,
    },
    data() {
      return {
        showVersus: true,
      };
    },
    methods: {
      handleTimeUp() {
        this.showVersus = false;
      },
      endGame() {
        this.$emit('gameEnded');
      }
    },
  };
  </script>
  
  <style scoped>
  .pong-page {
    color: #fff;
    position: relative;
  }
  .content {
    padding: 20px;
    text-align: center;
  }
  .player-controls {
    margin: 20px auto;
    width: 30%;
    background-color: rgba(17, 16, 16, 0.53);
    border-radius: 8px;
    padding: 10px;
  }
  .game-container {
    margin-top: 20px;
    border-radius: 8px;
    padding: 10px;
    background-color: none;
  }
  
  @media screen and (max-width: 810px) {
    .mobile-hide {
      display: none;
    }
    .player-controls {
      width: 100%;
      padding: 5px;
      background: none;
      border: none;
    }
    .game-container {
      padding: 5px;
      border: none;
    }
  }
  </style>