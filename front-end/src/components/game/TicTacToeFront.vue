<template>
  <div class="pong-page">
    <MatchPopup v-if="showPopup" @match-selected="handleMatchSelection" />
    <Versus v-else-if="showVersus" @time-up="handleTimeUp" />
    
    <div v-else class="content">
      <div class="game-container">
        <TicTacToeGame :mode="mode" :useImages="false" />
      </div>
    </div>
  </div>
</template>

<script>
import { computed } from "vue";
import { useRoute } from "vue-router";
import TicTacToeGame from "@/components/game/TicTacToeGame.vue";
import Versus from "@/components/game/Versus.vue";
import MatchPopup from "@/components/game/pongFront/PrivateMatch.vue";

export default {
  name: 'LocalFront',
  components: {
    Versus,
    TicTacToeGame,
    MatchPopup,
  },
  setup() {
    const route = useRoute();
    const mode = computed(() => route.params.mode);

    return { mode };
  },
  data() {
    return {
      showPopup: this.mode === 'withFriend',
      showVersus: this.mode !== 'withFriend',
      matchAction: '',
      matchCode: '',
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