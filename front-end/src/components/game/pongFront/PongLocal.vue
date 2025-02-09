<template>
  <div class="pong-page">
    <Versus v-if="showVersus" @time-up="handleTimeUp" />
    
    <div v-else class="content">
        <div class="player-controls">
        <div class="left-cmd">
          <h2 class="mobile-hide">{{ $t('commands') }}</h2>
          <p class="mobile-hide">{{ $t('move-up') }}<span class="span">W</span></p>
          <p class="mobile-hide">{{ $t('move-down') }} <span class="span">S</span></p>
        </div>
        <div class="right-cmd">
          <h2 class="mobile-hide">{{ $t('commands') }}</h2>
          <p class="mobile-hide">{{ $t('move-up') }}<span class="span">↑</span></p>
          <p class="mobile-hide">{{ $t('move-down') }} <span class="span">↓</span></p>
        </div>
      </div>

      <div class="game-container">
        <PongGame />
      </div>
    </div>
  </div>
</template>

<script>
import PongGame from "@/components/game/pongGame/PongGame.vue";
import Versus from "@/components/game/Versus.vue";

export default {
  name: 'LocalFront',
  components: {
    Versus,
    PongGame,
  },
  data() {
    return {
      showVersus: true,
    };
  },
  methods: {
    handleTimeUp() {
      // Hide the Versus overlay when the time is up
      this.showVersus = false;
    },
  },
};
</script>

<style scoped>
.pong-page {
  color: #fff;
}

.span {
  font-weight: bold;
}

.player-controls {
  display: flex;
}

.left-cmd {
  border-radius: 8px;
  padding: 10px;
  background-color: #11101088;
  width: 30%;
  margin-left: 7%;
}

.right-cmd {
  border-radius: 8px;
  padding: 10px;
  background-color: #11101088;
  width: 30%;
  margin-left: 25%;
}

.content {
  padding: 20px;
  text-align: center;
}

.game-container {
  border-radius: 8px;
  padding: 10px;
  background-color: none;
}

@media screen and (max-width: 810px) {
  .mobile-hide {
    display: none;
  }

  .left-cmd {
    padding: 0;
    background-color: transparent;
  }

  .right-cmd {
    padding: 0;
    background-color: transparent;
  }

  .player-controls {
    padding: 5px;
    background: none;
    border: none;
  }

  .game-container {
    padding: 5px;
    border: none;
  }
}

@media screen and (max-width: 410px) {
  .game-container {
    border: none;
  }
}
</style>
