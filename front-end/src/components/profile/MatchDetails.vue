<!-- Make conditions -->
<template>
    <div class="match-details">
      <div class="summary" @click="toggleDetails">
        {{ summaryText }}
        <span class="chevron">{{ isOpen ? '▼' : '▶' }}</span>
      </div>
      <transition name="slide">
        <div v-if="isOpen" class="details">
          <div class="detail-item">
            <span class="label">{{ $t("game") }} id</span>
            {{ match.id }}
          </div>
          <!-- <div class="detail-item">
            <span class="label">Mode :</span>
            {{ match.mode }}
          </div> -->
          <div class="detail-item">
            <span class="label"> {{ $t("tournament") }} :</span>
            {{ match.tournamentRank }}
          </div>
          <div class="detail-item">
            <span class="label">{{ $t("score") }} : </span>
            {{ match.score }}
          </div>
          <div class="detail-item">
            <span class="label">{{ $t("opponent-name") }} :</span>
            {{ match.opponentName }}
          </div>
          <div class="detail-item">
            <span class="label">{{ $t("opponent-rank") }} :</span>
            {{ match.opponentRank }}
          </div>
          <div class="detail-item">
            <span class="label">{{ $t("your-rank") }} :</span>
            {{ match.yourRank }}
          </div>
        </div>
      </transition>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      match: {
        type: Object,
        required: true
      }
    },
    data() {
      return {
        isOpen: false
      };
    },
    computed: {
      summaryText() {
        return `vs ${this.match.opponent}: ${this.match.won ? 'Win' : 'Loss'}`;
      }
    },
    methods: {
      toggleDetails() {
        this.isOpen = !this.isOpen;
      }
    }
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
  