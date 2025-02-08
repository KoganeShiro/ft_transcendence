<template>
  <div class="matchmaking-container">
    <!-- Matchmaking Phase -->
    <div v-if="phase === 'matchmaking'" class="matchmaking">
      <h1>Tournament Matchmaking</h1>
      
      <div class="round">
        <h2>First Round</h2>
        <div
          v-for="(match, index) in firstRound"
          :key="'first' + index"
          class="match"
        >
          <TextBox :modelValue="match.player1" :modifiable="false" class="field"/>
          <span class="vs">vs</span>
          <TextBox :modelValue="match.player2" :modifiable="false" class="field"/>
          <div class="timer" v-if="!match.completed">{{ match.timeLeft }}</div>
          <div class="status" v-else>Completed</div>
        </div>
      </div>
      
      <div class="round" v-if="secondRound.length > 0">
        <h2>Second Round</h2>
        <div
          v-for="(match, index) in secondRound"
          :key="'second' + index"
          class="match"
        >
          <TextBox :modelValue="match.player1" :modifiable="false" class="field"/>
          <span class="vs">vs</span>
          <TextBox :modelValue="match.player2" :modifiable="false" class="field"/>
          <div class="timer" v-if="!match.completed">{{ match.timeLeft }}</div>
          <div class="status" v-else>Completed</div>
        </div>
      </div>
      
      <div class="winner" v-if="winner">
        <h2>Tournament Winner</h2>
        <TextBox :modelValue="winner" :modifiable="false" class="field"/>
      </div>
    </div>

    <!-- Game Phase -->
    <div v-if="phase === 'game'" class="game-view">
      <!-- PongGame emits "game-ended" when finished -->
      <PongGame @game-ended="handleGameEnded" />
    </div>
  </div>
</template>

<script>
import TextBox from "@/components/atoms/ModifyInformations.vue";
import PongGame from "@/components/game/PongGame.vue";

export default {
  name: "Matchmaking",
  components: {
    TextBox,
    PongGame,
  },
  data() {
    return {
      // Phase can be 'matchmaking' or 'game'
      phase: "matchmaking",
      firstRound: [
        { player1: "Player 1", player2: "Player 3", completed: false, timeLeft: 10 },
        { player1: "Player 2", player2: "Player 4", completed: false, timeLeft: 10 },
      ],
      secondRound: [],
      winner: null,
      timers: [],
    };
  },
  mounted() {
    this.startTimers();
  },
  methods: {
    startTimers() {
      // Start timers for all matches in the first round.
      this.firstRound.forEach((match, index) => {
        this.startMatchTimer(match, "first", index);
      });
    },
    startMatchTimer(match, round, index) {
      const timer = setInterval(() => {
        if (match.timeLeft > 0) {
          match.timeLeft--;
        } else {
          clearInterval(timer);
          this.completeMatch(match, round, index);
        }
      }, 1000);
      this.timers.push(timer);
    },
    completeMatch(match, round, index) {
      match.completed = true;
      // For demonstration, choose a winner randomly for this match.
      const matchWinner = Math.random() < 0.5 ? match.player1 : match.player2;
      
      // In this example, when all matches in the first round are complete,
      // we transition to the game phase.
      if (round === "first" && this.firstRound.every(m => m.completed)) {
        // Transition to game phase
        this.phase = "game";
      }
      // (You could add logic for the second round if needed)
    },
    handleGameEnded(result) {
      // When PongGame ends, log the result and then reset the matchmaking for the next match.
      console.log("Game ended with result:", result);
      // Remove the PongGame by switching phase, then restart matchmaking:
      this.resetMatchmaking();
      // Optionally, you can update rounds here based on the game result.
      this.phase = "matchmaking";
    },
    resetMatchmaking() {
      // Clear any existing timers
      this.timers.forEach(timer => clearInterval(timer));
      this.timers = [];
      // Reset the rounds and winner.
      this.firstRound = [
        { player1: "Player 1", player2: "Player 3", completed: false, timeLeft: 10 },
        { player1: "Player 2", player2: "Player 4", completed: false, timeLeft: 10 },
      ];
      this.secondRound = [];
      this.winner = null;
      // Restart timers for new matchmaking round.
      this.startTimers();
    },
  },
  beforeUnmount() {
    this.timers.forEach(timer => clearInterval(timer));
  },
};
</script>


<style scoped>
.matchmaking-container {
  max-width: 90%;
  margin: 0 auto;
  padding: 20px;
  text-align: center;
}

.round {
  margin-bottom: 30px;
}

.match {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  margin-bottom: 10px;
  gap: 10px;
  padding: 15px;
  border-radius: 8px;
  background: rgba(99, 99, 99, 0.1);
}

.vs {
  font-weight: bold;
  font-size: 1.2em;
  color: var(--text-color);
}

.status {
  font-weight: bold;
  padding: 5px;
  border-radius: 4px;
}

.timer {
  font-weight: bold;
  font-size: 1rem;
}

.field {
  margin-bottom: 30px;
}

.winner {
  font-size: 1.5em;
  font-weight: bold;
  color: gold;
}

/* Game view styling */
.game-view {
  margin-top: 20px;
}
@media (max-width: 800px) {
  .matchmaking-container {
    margin-left: 0;
  }
  .match {
    flex-direction: column;
    text-align: center;
  }
  .vs {
    margin: 5px 0;
  }
}
</style>
