<template>
    <div class="template">
      <HeaderOrganism />
      <div class="container">
        <!-- if the player loose, they are kick out of the tournament
         let them a page message to let them know that they
         can view the result in their history when the tournament is
         finish -->
        <div v-if="winner" class="winner-section">
          <h1>🏆 Tournament Winner: {{ winner }} 🏆</h1>
        </div>
  
        <div v-else class="matchmaking-section">
          <MatchmakingComponent
            :firstRound="firstRound"
            :secondRound="secondRound"
            :winner="winner"
          />
  
          <div v-if="countdown > 0" class="countdown">
            <h2>Match starts in {{ countdown }} seconds...</h2>
          </div>
  
          <div v-if="gameStarted && !eliminated">
            <PongGame :mode="'remote'" />
            <h2>Playing Against: {{ currentOpponent }}</h2>
          </div>
  
          <div v-if="gameStarted && eliminated">
            <h2>You've been eliminated! Spectating matches...</h2>
          </div>
        </div>
      </div>
      <FooterOrganism />
    </div>
  </template>
  
  <script>
  import HeaderOrganism from "@/components/header/navbar.vue";
  import FooterOrganism from "@/components/footer.vue";
  import MatchmakingComponent from "@/components/game/Matchmaking.vue";
  import PongGame from "@/components/game/PongGame.vue";
  import { useStore } from 'vuex';
  
  export default {
    components: {
      HeaderOrganism,
      FooterOrganism,
      MatchmakingComponent,
      PongGame,
    },
    setup() {
      const store = useStore();
    },
    data() {
      return {
        firstRound: [
          { player1: "Player 1", player2: "Player 3", completed: false },
          { player1: "Player 2", player2: "Player 4", completed: false },
        ],
        secondRound: [],
        winner: null,
        countdown: 5, // Seconds before the match starts
        gameStarted: false,
        currentOpponent: null,
        eliminated: false,
        userPlayer: "Player 1", // Example, replace with actual logged-in user
      };
    },
    methods: {
      startCountdown() {
        let timer = setInterval(() => {
          if (this.countdown > 0) {
            this.countdown--;
          } else {
            clearInterval(timer);
            this.startGame();
          }
        }, 1000);
      },
      startGame() {
        this.gameStarted = true;
  
        const userMatch = this.firstRound.find(
          (match) =>
            match.player1 === this.userPlayer || match.player2 === this.userPlayer
        );
  
        if (userMatch) {
          this.currentOpponent =
            userMatch.player1 === this.userPlayer
              ? userMatch.player2
              : userMatch.player1;
        } else {
          this.eliminated = true; // Spectate if not playing
        }
  
        setTimeout(() => {
          this.completeMatch();
        }, 100000);
      },
      completeMatch() {
        this.gameStarted = false;
  
        const userMatch = this.firstRound.find(
          (match) =>
            match.player1 === this.userPlayer || match.player2 === this.userPlayer
        );
  
        if (userMatch) {
          const matchWinner =
            Math.random() < 0.5 ? userMatch.player1 : userMatch.player2;
  
          if (matchWinner !== this.userPlayer) {
            this.eliminated = true;
          }
  
          if (this.firstRound.every((match) => match.completed)) {
            this.progressTournament(matchWinner);
          }
        }
      },
      progressTournament(lastWinner) {
        if (this.secondRound.length === 0) {
          this.secondRound = [{ player1: lastWinner, player2: "Random Player", completed: false }];
        } else {
          this.winner = lastWinner;
        }
      },
      restartTournament() {
        this.firstRound = [
          { player1: "Player 1", player2: "Player 3", completed: false },
          { player1: "Player 2", player2: "Player 4", completed: false },
        ];
        this.secondRound = [];
        this.winner = null;
        this.eliminated = false;
        this.countdown = 5;
        this.startCountdown();
      },
    },
    mounted() {
      this.startCountdown();
    },
  };
  </script>
  
  <style scoped>
  .container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
    max-width: 800px;
    margin: 0 auto;
    text-align: center;
  }
  
  .matchmaking-section {
    margin-top: 20px;
  }
  
  .countdown {
    font-size: 24px;
    font-weight: bold;
    color: #ffcc00;
  }
  
  .winner-section {
    text-align: center;
    font-size: 24px;
    font-weight: bold;
    color: gold;
  }
  </style>