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

    <div class="player-controls left" v-else-if="mode === 'multiplayer'">
      <h2 class="mobile-hide">Player 1</h2>
      <p class="mobile-hide">Move Up: <span>W</span></p>
      <p class="mobile-hide">Move Down: <span>S</span></p>
      <!-- MultiPong -->
    </div>

    <div class="tournament" v-else-if="mode === 'tournament'">
      <CreateTournament />
    </div>

    <div v-if="mode !== 'tournament'" class="game-container">
      <Versus
        v-if="showVersus"
        :player1="player1"
        :player2="player2"
        :duration="5000"
        @time-up="startGame"
      />
      <PongGame v-else :mode="mode" />
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import PongGame from "@/components/game/PongGame.vue";
import CreateTournament from "@/components/game/CreateTournament.vue";
import Versus from "@/components/game/Versus.vue";

export default {
  components: {
    PongGame,
    CreateTournament,
    Versus,
  },
  props: {
    mode: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const showVersus = ref(true);

    const player1 = ref({
      // imageUrl: "path/to/player1/image.png",
      pseudo: "Player1",
    });

    const player2 = ref({
      // imageUrl: "path/to/player2/image.png",
      pseudo: "Player2",
    });

    const startGame = () => {
      showVersus.value = false;
    };

    return {
      showVersus,
      player1,
      player2,
      startGame,
    };
  },
};
</script>


<style scoped>
.pong-container {
  color: var(--text-color);
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