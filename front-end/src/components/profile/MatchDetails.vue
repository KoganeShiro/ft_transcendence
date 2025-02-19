<template>
  <div class="match-details">
    <div class="summary" @click="toggleDetails">
      {{ summaryText }}
      <span class="chevron">{{ isOpen ? '▼' : '▶' }}</span>
    </div>
    <transition name="slide">
      <div v-if="isOpen" class="details">
        <div class="detail-item">
          <span class="label">{{ $t("winner") }}:</span>
          {{ this.match.winner }}
        </div>
        <div class="detail-item">
          <span class="label">{{ $t("loser") }}:</span>
          {{ this.match.loser }}
        </div>
        <div v-if="localGameType === 'pong'">
          <div class="detail-item">
            <span class="label">{{ $t("your_score") }}:</span>
            {{ this.match.my_score }}
          </div>
          <div class="detail-item">
            <span class="label">{{ $t("opponent_score") }}:</span>
            {{ this.match.opponent_score }}
          </div>
        </div>
        <div v-if="localGameType === 'ttt'">
          <div class="detail-item">
            <span class="label">{{ $t("your_nb_move") }}:</span>
            {{ this.match.my_turn }}
          </div>
          <div class="detail-item">
            <span class="label">{{ $t("opponent_nb_move") }}:</span>
            {{ this.match.opponent_turn }}
          </div>
        </div>
        <div class="detail-item" v-if="localGameType === 'pong'">
          <span class="label">{{ $t("your_rank_begin") }}:</span>
          {{ this.match.rank_player1_begin }}
        </div>
        <div class="detail-item" v-if="localGameType === 'pong'">
          <span class="label">{{ $t("opponent_rank_begin") }}:</span>
          {{ this.match.rank_player2_begin }}
        </div>
        <div class="detail-item" v-if="localGameType === 'pong'">
          <span class="label">{{ $t("your_rank_change") }}:</span>
          {{ this.match.rank_player1_change }}
        </div>
        <div class="detail-item" v-if="localGameType === 'pong'">
          <span class="label">{{ $t("opponent_rank_change") }}:</span>
          {{ this.match.rank_player2_change }}
        </div>
        <div class="detail-item">
          <span class="label">{{ $t("timestamp") }}:</span>
          {{ formattedTimestamp || 'N/A' }}
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import { format } from 'date-fns';

export default {
  props: {
    match: {
      type: Object,
      required: true,
    },
    gameType: {
      type: String,
      required: true,
    },
    history: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      isOpen: false,
      gameDetails: {},
      localGameType: this.gameType === 'Tic Tac Toe' ? 'ttt' : this.gameType.toLowerCase(),
    };
  },
  computed: {
    summaryText() {
      let result = this.match.winner;
      if (this.match.won === false) {
        // console.log("match.won: ", this.match.won);
        result = "loose";
      }
      else {
        result = "win";
      }      
      if (this.match.player1 === this.match.opponent) {
        let tmpPlayer = this.match.player1;
        this.match.player1 = this.match.player2;
        this.match.player2 = tmpPlayer;

        let tmpRankBegin = this.match.rank_player1_begin;
        this.match.rank_player1_begin = this.match.rank_player2_begin;
        this.match.rank_player2_begin = tmpRankBegin;

        // console.log("tmpRankBegin p1: ", this.match.rank_player1_begin);
        // console.log("tmpRankBegin p2: ", this.match.rank_player2_begin);

        let tmpRankChange = this.match.rank_player1_change;
        this.match.rank_player1_change = this.match.rank_player2_change;
        this.match.rank_player2_change = tmpRankChange;

        // console.log("tmpRankChange p1: ", this.match.rank_player1_change);
        // console.log("tmpRankChange p2: ", this.match.rank_player2_change);

    }
      // console.log("my score: ", this.match.my_score);
      // console.log("opponent score: ", this.match.opponent_score);
      // console.log("winner: ", this.match.winner);
        return `${this.match.player1} vs ${this.match.player2}: ${result}`;
    },
    formattedTimestamp() {
            return this.gameDetails.timestamp ? format(new Date(this.gameDetails.timestamp), 'PP HH:mm') : 'N/A';
    },
  },
  methods: {
    async toggleDetails() {
      if (!this.isOpen) {
        try {
          const response = await fetch(`/api/games/${this.localGameType}/${this.match.id}`);
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          this.gameDetails = await response.json();
          // console.log('Game details:', this.gameDetails);
        } catch (error) {
          // console.error('Error fetching game details:', error);
          this.gameDetails = {
            winner: 'N/A',
            loser: 'N/A',
            player1_score: 'N/A',
            player2_score: 'N/A',
            player1_turn: 'N/A',
            player2_turn: 'N/A',
            rank_player1_begin: 'N/A',
            rank_player2_begin: 'N/A',
            rank_player1_change: 'N/A',
            rank_player2_change: 'N/A',
            timestamp: 'N/A',
          };
        }
      }
      this.isOpen = !this.isOpen;
    },
  },
};
</script>

  
  <style scoped>
  .match-details {
    cursor: pointer;
    margin: 10px 0;
  }
  
  .summary {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px;
    background-color: var(--text-box-color);
    border-radius: 8px;
  }
  
  .chevron {
    margin-left: 10px;
  }
  
  .details {
    padding: 10px;
    background-color: var(--background-dark);
    border-radius: 0 0 8px 8px;
  }
  
  .detail-item {
    margin: 5px 0;
    display: flex;
    justify-content: space-between;
  }
  
  .label {
    font-weight: bold;
    margin-right: 10px;
  }
  
  .slide-enter-active, .slide-leave-active {
    transition: all 0.3s ease;
  }
  
  .slide-enter-from, .slide-leave-to {
    opacity: 0;
    transform: translateY(-10px);
  }
  </style>
  