<template>
  <div class="pong-page">
     <Versus
      v-if="showVersus"
      :player2="opponentPlayer"
      @time-up="handleTimeUp"
      class="versus-overlay"
    />
    
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
        <PongLocal @gameEnded="handleGameEnded" />
        <WinnerPopup v-if="showWinner" :winnerName="winnerName" :winnerImage="winnerImage" />
        <LoserPopup v-if="showLoser" :loserName="loserName" :loserImage="loserImage" />
      </div>
    </div>
  </div>
</template>

<script>
import Versus from "@/components/game/Versus.vue";
import PongLocal from "@/components/game/pongGame/PongLocal.vue";
import WinnerPopup from "@/views/game/winner.vue";
import LoserPopup from "@/views/game/loser.vue";
import API from '@/api.js';

export default {
  name: 'LocalFront',
  components: {
    Versus,
    PongLocal,
    WinnerPopup,
    LoserPopup,
  },
  data() {
    return {
      showVersus: true,
      showWinner: false,
      showLoser: false,
      winnerName: '',
      winnerImage: '',
      loserName: '',
      loserImage: '',
      requestSent: false,
      opponentPlayer: {
        pseudo: "Guest",
        imageUrl: "",
      },
    };
  },
  
  methods: {
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
          if (winner === "Player 1") {
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