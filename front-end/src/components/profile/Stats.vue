<template>
  <div class="stats-container">
    <h1>{{$t("stats")}}</h1>
    <div v-if="loading">{{$t("loading")}}</div>
    <div v-else>
      <div v-if="stats.stats && stats.stats.Pong">
        <GameStatsCard gameType="Pong" :stats="stats.stats.Pong" />
      </div>
      <div v-if="stats.stats && stats.stats['Tic Tac Toe']">
        <GameStatsCard gameType="Tic Tac Toe" :stats="stats.stats['Tic Tac Toe']" />
      </div>
    </div>
  </div>
</template>

<script>
import GameStatsCard from '@/components/profile/StatsCard.vue'
import API from "@/api.js"

export default {
  components: {
    GameStatsCard,
  },
  data() {
    return {
      stats: {
        stats: {
          Pong: null,
          'Tic Tac Toe': null
        }
      },
      loading: false,
    }
  },
  async mounted() {
    if (this.loading) return;
    this.loading = true;
  
    try {
      const response = await API.get('/api/stats/');
      this.stats = response.data;
      console.log('Stats:', this.stats);
      console.log('Pong stats:', this.stats.stats.Pong);
      console.log('Tic Tac Toe stats:', this.stats.stats['Tic Tac Toe']);
      this.loading = false;
    } catch (error) {
      console.error('Error fetching stats:', error);
      this.loading = false;
    }
  }
}
</script>

<style scoped>
.stats-container {
  padding: 20px;
  color: var(--text-color);
  margin-bottom: 50px;
}
</style>