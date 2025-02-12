<template>
  <div class="page-container">
    <h1>{{ $t("history") }}</h1>
    <div v-if="loading">{{ $t("loading") }}</div>
    <div v-else>
      <div v-for="(gameType, index) in gameTypes" :key="index" class="game-section">
        <h2>{{ gameType }}</h2>
        <ul class="history-list">
          <li v-for="match in getMatchesByType(gameType)" :key="match.id">
            <MatchDetails :match="match" />
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import MatchDetails from '@/components/profile/MatchDetails.vue';

export default {
  components: {
    MatchDetails
  },
  data() {
    return {
      history: [],
      loading: true,
      error: null,
      // gameTypes: ['Pong', '4 Players Pong', 'Tic Tac Toe']
      gameTypes: ['Pong', 'Tic Tac Toe']
    };
  },
  methods: {
    async fetchMatchDetails(id, gameType) {
      try {
        const response = await fetch(`/api/games/${gameType.toLowerCase()}/${id}`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
      } catch (error) {
        console.error(`Error fetching match ${id}:`, error);
        return null;
      }
    },
    getMatchesByType(gameType) {
      return this.history.filter(match => match.type === gameType);
    }
  },
  async mounted() {
    try {
      this.loading = true;
      
      // Fetch last 5 Pong games
      let response = await fetch('/api/games/last_five_pong_games');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      let pongGames = await response.json();
      
      // Fetch last 5 Tic Tac Toe games
      response = await fetch('/api/games/last_five_ttt_games');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      let tttGames = await response.json();
      
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


<!-- <script>
import MatchDetails from '@/components/profile/MatchDetails.vue';

export default {
  components: {
    MatchDetails
  },
  data() {
    return {
      history: [
        // Pong matches
        {
          id: 'pong1',
          gameType: 'Pong',
          opponent: 'AI',
          won: true,
          date: '2023-07-20T14:30:00Z',
          score: '10-8',
          opponentRank: 'Beginner',
          yourRank: 'Intermediate'
        },
        {
          id: 'pong2',
          gameType: 'Pong',
          opponent: 'JohnDoe',
          won: false,
          date: '2023-07-19T10:15:00Z',
          score: '7-10',
          opponentRank: 'Expert',
          yourRank: 'Intermediate'
        },
        {
          id: 'pong3',
          gameType: 'Pong',
          opponent: 'AI',
          won: true,
          date: '2023-07-18T18:45:00Z',
          score: '10-5',
          opponentRank: 'Beginner',
          yourRank: 'Intermediate'
        },
        {
          id: 'pong4',
          gameType: 'Pong',
          opponent: 'JaneSmith',
          won: true,
          date: '2023-07-17T20:00:00Z',
          score: '10-9',
          opponentRank: 'Intermediate',
          yourRank: 'Intermediate'
        },
        {
          id: 'pong5',
          gameType: 'Pong',
          opponent: 'AI',
          won: false,
          date: '2023-07-16T15:30:00Z',
          score: '8-10',
          opponentRank: 'Expert',
          yourRank: 'Intermediate'
        },
        // 4 Players Pong matches
        {
          id: '4pong1',
          gameType: '4 Players Pong',
          opponent: 'player 1',
          opponent2: 'player 2',
          opponent3: 'player 3',
          won: true,
          date: '2023-07-15T19:00:00Z',
          score: '10-8-7-6',
          opponentRank: 'Intermediate',
          yourRank: 'Expert'
        },
        {
          id: '4pong2',
          gameType: '4 Players Pong',
          opponent: 'player 1',
          opponent2: 'player 2',
          opponent3: 'player 3',
          won: false,
          date: '2023-07-14T21:15:00Z',
          score: '9-10-8-7',
          opponentRank: 'Expert',
          yourRank: 'Expert'
        },
        {
          id: '4pong3',
          gameType: '4 Players Pong',
          opponent: 'player 1',
          opponent2: 'player 2',
          opponent3: 'player 3',
          won: true,
          date: '2023-07-13T17:30:00Z',
          score: '10-9-8-7',
          opponentRank: 'Beginner',
          yourRank: 'Expert'
        },
        {
          id: '4pong4',
          gameType: '4 Players Pong',
          opponent: 'player 1',
          opponent2: 'player 2',
          opponent3: 'player 3',
          won: false,
          date: '2023-07-12T20:45:00Z',
          score: '8-10-7-6',
          opponentRank: 'Expert',
          yourRank: 'Expert'
        },
        {
          id: '4pong5',
          gameType: '4 Players Pong',
          opponent: 'Team Purple',
          won: true,
          date: '2023-07-11T18:00:00Z',
          score: '10-9-8-7',
          opponentRank: 'Intermediate',
          yourRank: 'Expert'
        },
        // Tic Tac Toe matches
        {
          id: 'ttt1',
          gameType: 'Tic Tac Toe',
          opponent: 'AI',
          won: true,
          date: '2023-07-10T14:00:00Z',
          score: '1-0',
          opponentRank: 'Beginner',
          yourRank: 'Intermediate'
        },
        {
          id: 'ttt2',
          gameType: 'Tic Tac Toe',
          opponent: 'BobJohnson',
          won: false,
          date: '2023-07-09T16:30:00Z',
          score: '0-1',
          opponentRank: 'Expert',
          yourRank: 'Intermediate'
        },
        {
          id: 'ttt3',
          gameType: 'Tic Tac Toe',
          opponent: 'AI',
          won: true,
          date: '2023-07-08T11:45:00Z',
          score: '1-0',
          opponentRank: 'Intermediate',
          yourRank: 'Intermediate'
        },
        {
          id: 'ttt4',
          gameType: 'Tic Tac Toe',
          opponent: 'AliceWilliams',
          won: true,
          date: '2023-07-07T19:15:00Z',
          score: '1-0',
          opponentRank: 'Beginner',
          yourRank: 'Intermediate'
        },
        {
          id: 'ttt5',
          gameType: 'Tic Tac Toe',
          opponent: 'AI',
          won: false,
          date: '2023-07-06T13:00:00Z',
          score: '0-1',
          opponentRank: 'Expert',
          yourRank: 'Intermediate'
        }
      ],
      loading: false,
      error: null,
      gameTypes: ['Pong', '4 Players Pong', 'Tic Tac Toe']
    };
  },
  methods: {
    getMatchesByType(gameType) {
      return this.history.filter(match => match.gameType === gameType);
    }
  },
  // Remove the mounted hook since we're using hard-coded data
};
</script> -->


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
