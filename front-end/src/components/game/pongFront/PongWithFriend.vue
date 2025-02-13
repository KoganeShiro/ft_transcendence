<template>
  <div class="pong-page">
    <!-- Listen for "match-ready" from PrivateMatch -->
    <MatchPopup v-if="showPopup" @match-ready="handleMatchReady" />
    <div v-else class="content">
      <!-- make sure that the versus component show the oponnent username -->
      <Versus v-if="showVersus" @time-up="handleVersusTimeUp" />
      <div v-else>
        <!-- The game doesn't start... -->
        <PongGame :gameMode="gameMode" :joinCode="matchCode" />
      </div>
    </div>
  </div>
</template>

<script>
import PongGame from "@/components/game/pongGame/PongFriend.vue";
import Versus from "@/components/game/Versus.vue";
import MatchPopup from "@/components/game/pongFront/PrivateMatch.vue";

export default {
  name: "PongWithFriend",
  components: { PongGame, Versus, MatchPopup },
  data() {
    return {
      showPopup: true,
      showVersus: false,
      gameMode: null,
      matchCode: null,
    };
  },
  methods: {
    handleMatchReady({ code, mode }) {
      // Hide the popup and start the versus overlay for both players
      this.showPopup = false;
      this.gameMode = mode;
      this.matchCode = code;
      this.showVersus = true;
    },
    handleVersusTimeUp() {
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
