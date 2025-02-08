<template>
  <div class="stats-container">
    <h1>Stats</h1>
    <div v-for="(gameStats, gameType) in stats" :key="gameType">
      <GameStatsCard :gameType="gameType" :stats="gameStats" />
    </div>
  </div>
</template>

<script>
import GameStatsCard from '@/components/profile/StatsCard.vue'

export default {
  name: "StatsContainer",
  components: {
    GameStatsCard
  },
  data() {
    return {
      stats: {
        "Pong": {
          currentRank: 1,
          totalMatches: 100,
          tournamentWins: 5,
          wins: 60,
          losses: 40,
          rankProgression: [1000, 1050, 1100, 1075, 1125, 1150, 1200],
          pointsWonUnder5Exchanges: 100,
          pointsWonUnder10Exchanges: 200,
          pointsWonOver10Exchanges: 300,
          pointsLostUnder5Exchanges: 80,
          pointsLostUnder10Exchanges: 150,
          pointsLostOver10Exchanges: 250
        },
        "4 Players Pong": {
          currentRank: 1,
          totalMatches: 50,
          wins: 28,
          losses: 22,
          rankProgression: [800, 850, 900, 875, 925, 950, 1000],
          pointsWonUnder5Exchanges: 50,
          pointsWonUnder10Exchanges: 100,
          pointsWonOver10Exchanges: 150,
          pointsLostUnder5Exchanges: 40,
          pointsLostUnder10Exchanges: 80,
          pointsLostOver10Exchanges: 120
        },
        "Tic Tac Toe": {
          currentRank: 1,
          totalMatches: 200,
          wins: 120,
          losses: 80,
          rankProgression: [1500, 1550, 1600, 1650, 1700, 1750, 1800],
        }
      }
    }
  }
}
</script>

<!-- <script>
import GameStatsCard from '@/components/profile/StatsCard.vue'

export default {
  components: {
    GameStatsCard
  },
  data() {
    return {
      stats: {}
    }
  },
  async mounted() {
    try {
      const response = await fetch('/api/stats')
      this.stats = await response.json()
    } catch (error) {
      console.error('Error fetching stats:', error)
    }
  }
}
</script> -->

<style scoped>
.stats-container {
  padding: 20px;
  color: var(--text-color);
  margin-bottom: 50px;
}
</style>
