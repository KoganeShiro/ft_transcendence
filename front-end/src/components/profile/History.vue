<template>
  <div class="page-container">
    <h1>{{ $t("history") }}</h1>
    <div v-if="loading">{{ $t("loading") }}</div>
    <div v-else>
      <div v-for="(gameType, index) in gameTypes" :key="index" class="game-section">
        <h2>{{ gameType }}</h2>
        <ul class="history-list">
          <li v-for="match in getMatchesByType(gameType)" :key="match.id">
            <MatchDetails :match="match" :gameType="gameType" :history="history" />
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import MatchDetails from './MatchDetails.vue';

export default {
  components: {
    MatchDetails,
  },
  data() {
    return {
      history: [],
      loading: false,
      error: null,
      gameTypes: ['Pong', 'Tic Tac Toe'],
      games: ['pong', 'ttt'],
    };
  },
  methods: {
    getMatchesByType(gameType) {
      return this.history.filter(match => match.gameType === gameType);
    },
  },
  async mounted() {
    this.loading = true;
    try {
      let response = await fetch('/api/games/last_five_pong_games');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      let pongGames = await response.json();
      pongGames = pongGames.map(game => ({ ...game, gameType: 'Pong' }));

      response = await fetch('/api/games/last_five_ttt_games');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      let tttGames = await response.json();
      tttGames = tttGames.map(game => ({ ...game, gameType: 'Tic Tac Toe' }));

      // Combine the games into the history array
      this.history = [...pongGames, ...tttGames];

      this.loading = false;
    } catch (error) {
      console.error('Error fetching match history:', error);
      this.error = error;
      this.loading = false;
    }
  },
};
</script>

<style scoped>
.page-container {
  padding: 20px;
  color: var(--text-color);
  margin-bottom: 50px;
}

.game-section {
  margin-bottom: 30px;
}

.game-section h2 {
  margin-bottom: 15px;
  border-bottom: 1px solid var(--text-color);
  padding-bottom: 5px;
}

.history-list {
  list-style: none;
  padding: 0;
}

.history-list li {
  margin: 10px 0;
}
</style>
