<template>
  <div class="pong-page">
    <MatchPopup v-if="showPopup" @match-selected="handleMatchSelection" />
    
    <div v-else class="content">
      <Versus v-if="showVersus" @time-up="handleVersusTimeUp" />
      <div v-else>
        <div class="player-controls">
          <h2 class="mobile-hide">Commands</h2>
          <p class="mobile-hide">Move Up: <span class="span">W</span></p>
          <p class="mobile-hide">Move Down: <span class="span">S</span></p>
        </div>
        <div class="game-container">
          <PongGame />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import PongGame from "@/components/game/PongGame.vue";
import Versus from "@/components/game/Versus.vue";
import MatchPopup from "@/components/game/pongFront/PrivateMatch.vue";

export default {
  name: 'SoloFront',
  components: {
    PongGame,
    Versus,
    MatchPopup,
  },
  data() {
    return {
      showPopup: true,
      showVersus: false,
      // Optionally store the selected match action and code
      matchAction: null,
      matchCode: null,
    };
  },
  methods: {
    handleMatchSelection({ action, code }) {
      // Hide the popup and proceed with the selected action.
      this.showPopup = false;
      this.matchAction = action;
      this.matchCode = code;
      
      // For example, if the user chose "create", we might show the versus overlay first.
      if (action === "create") {
        this.showVersus = true;
      } else if (action === "join") {
        // Handle join logic here; you might also show Versus before the game.
        this.showVersus = true;
      }
    },
    handleVersusTimeUp() {
      // When the Versus component finishes, hide it and show the game.
      this.showVersus = false;
    },
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
}
.span {
  font-weight: bold;
}
</style>
