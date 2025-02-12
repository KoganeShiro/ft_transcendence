<template>
  <div class="stats-container">
    <h1>{{$t("stats")}}</h1>
    <div v-if="loading">{{$t("loading")}}</div>
    <div v-else>
      <div v-for="(gameStats, gameType) in stats.stats" :key="gameType">
        <GameStatsCard :gameType="gameType" :stats="gameStats" />
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
      stats: {},
      loading: false,
    }
  },
  async mounted() {
    if (this.loading) return;
    this.loading = true;
  
    try {
      const response = await API.get('/api/stats/');
      this.stats = response.data;
      //console.log('Stats:', this.stats);
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