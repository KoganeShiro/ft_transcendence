<template>
    <div class="pong-container">
      <div class="controls" v-if="mode === 'local'">
        <div class="player-controls left">
          <h2 class="mobile-hide">Player 1</h2>
          <p class="mobile-hide">Move Up: <span>W</span></p>
          <p class="mobile-hide">Move Down: <span>S</span></p>
        </div>
        <div class="player-controls right">
          <h2 class="mobile-hide">Player 2</h2>
          <p class="mobile-hide">Move Up: <span>↑</span></p>
          <p class="mobile-hide">Move Down: <span>↓</span></p>
        </div>
      </div>

      <div class="player-controls left" v-else-if="mode === 'solo'">
        <h2 class="mobile-hide">Player 1</h2>
        <p class="mobile-hide">Move Up: <span>W</span></p>
        <p class="mobile-hide">Move Down: <span>S</span></p>
      </div>

      <div class="player-controls left" v-else-if="mode === 'remote'">
        <h2 class="mobile-hide">Player 1</h2>
        <p class="mobile-hide">Move Up: <span>W</span></p>
        <p class="mobile-hide">Move Down: <span>S</span></p>
      </div>

      <div class="player-controls" v-else-if="mode === 'tournament'">
        <h1 class="mobile-hide">Create tournament (todo)</h1>
      </div>

      <div class="game-container">
        <PongGame :mode="mode" />
      </div>
    </div>
</template>
  
<script>
import PongGame from "@/components/game/PongGame.vue";

export default {
  components: {
    PongGame,
  },
  props: {
    mode: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    console.log("Received mode prop:", props.mode);
  },
};
</script>
  
<style scoped>
.pong-container {
  color: white;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

.controls {
  display: flex;
  justify-content: space-between;
  width: 80%;
  max-width: 900px;
  margin-bottom: 20px;
}

.player-controls {
  flex: 1;
  padding: 15px;
  text-align: center;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.1);
}

.left {
  text-align: left;
}

.right {
  text-align: right;
}

.game-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  max-width: 900px;
}

/* Mobile styles */
@media screen and (max-width: 768px) {
  .mobile-hide {
    display: none;
  }

  .player-controls {
    padding: 5px;
    background: none;
  }

  .controls {
    margin-bottom: 10px;
  }
}
</style>