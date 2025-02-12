<template>
  <div class="ttt-page">
    <MatchPopup v-if="showPopup" @match-selected="handleMatchSelection" />
    <Versus v-else-if="showVersus" @time-up="handleTimeUp" />
    
    <div v-else class="content">
      <div class="game-container">
        <!-- Pass the mode down to the game component -->
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
    console.log("LocalFront: mode computed value =", mode.value);
    return { mode };
  },
  data() {
    return {
      showPopup: false,
      showVersus: true,
      matchAction: '',
      matchCode: '',
    };
  },
  methods: {
    handleMatchSelection({ action, code }) {
      this.showPopup = false;
      this.matchAction = action;
      this.matchCode = code;
      if (action === "create" || action === "join") {
        this.showVersus = true;
      }
    },
    handleTimeUp() {
      this.showVersus = false;
    },
  },
};
</script>
  

<style scoped>
.ttt-page {
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