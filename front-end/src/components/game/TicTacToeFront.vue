<template>
  <div class="ttt-page">
    <!-- <MatchPopup v-if="showPopup" @match-selected="handleMatchSelection" /> -->
    <Versus
      v-if="showVersus"
      :opponentType="opponent_username"
      @time-up="handleTimeUp"
    />
    
    <div v-else class="content">
      <div class="game-container">
        <TicTacToeGame :mode="mode" :useImages="false" @game-ended="handleGameEnded" />
        <WinnerPopup v-if="showWinner" :winnerName="winnerName" :winnerImage="winnerImage" />
        <LoserPopup v-if="showLoser" :loserName="loserName" :loserImage="loserImage" />
      </div>
    </div>
  </div>
</template>

<script>
import { computed } from "vue";
import { useRoute } from "vue-router";
import TicTacToeGame from "@/components/game/TicTacToeGame.vue";
import Versus from "@/components/game/Versus.vue";
// import MatchPopup from "@/components/game/pongFront/PrivateMatch.vue";
import WinnerPopup from "@/views/game/winner.vue";
import LoserPopup from "@/views/game/loser.vue";
import API from '@/api.js';

export default {
  name: 'LocalFront',
  components: {
    Versus,
    TicTacToeGame,
    // MatchPopup,
    WinnerPopup,
    LoserPopup,
  },
  setup() {
    const route = useRoute();
    const mode = computed(() => route.params.mode);
    console.log(mode.value);
    const opponent = computed(() => {
    if (mode.value === "solo") {
          return "AI";
        } else if (mode.value === "local") {
          return "Guest";
        } else {
          return "";
        }
      });
      const opponent_username = opponent.value;
      console.log(opponent_username);
    return { mode, opponent_username };
  },
  data() {
    return {
      showPopup: false,
      showVersus: true,
      matchAction: '',
      matchCode: '',
      showWinner: false,
      showLoser: false,
      winnerName: '',
      winnerImage: '',
      loserName: '',
      loserImage: '',
      requestSent: false,
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
    async handleGameEnded(winner) {
      if (this.requestSent) return;
      this.requestSent = true;
      try {
        const response = await API.get('/api/profile/');
        const { username, cover_photo } = response.data;
        console.log("handleGameEnded: winner =", winner);
        if (winner === "X") {
          this.winnerName = username;
          this.winnerImage = cover_photo;
          this.showWinner = true;
        } else {
          this.loserName = username;
          this.loserImage = cover_photo;
          this.showLoser = true;
        }
      } catch (error) {
        console.error("Error fetching user data:", error);
      }
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