<template>
  <div class="matchmaking">
    <h1>Tournament Matchmaking</h1>

    <div class="round">
      <h2>First Round</h2>
      <div v-for="(match, index) in firstRound" :key="'first' + index" class="match">
        <TextBox :modelValue="match.player1" :modifiable="false" class="field"/>
        <span class="vs">vs</span>
        <TextBox :modelValue="match.player2" :modifiable="false" class="field"/>
        <div class="timer" v-if="!match.completed">{{ match.timeLeft }}</div>
        <div class="status" v-else>Completed</div>
      </div>
    </div>

    <div class="round" v-if="secondRound.length > 0">
      <h2>Second Round</h2>
      <div v-for="(match, index) in secondRound" :key="'second' + index" class="match">
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
</template>

<script>
import TextBox from "@/components/atoms/ModifyInformations.vue";

export default {
  components: {
    TextBox,
  },
  data() {
    return {
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
      this.firstRound.forEach((match, index) => {
        this.startMatchTimer(match, 'first', index);
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
      const winner = Math.random() < 0.5 ? match.player1 : match.player2;
      
      if (round === 'first') {
        if (this.firstRound.every(m => m.completed) && this.secondRound.length === 0) {
          this.startSecondRound(winner);
        }
      } else if (round === 'second') {
        this.setWinner(winner);
      }
    },
    startSecondRound(firstWinner) {
      const secondWinner = this.firstRound.find(m => m.player1 !== firstWinner && m.player2 !== firstWinner).player1;
      this.secondRound = [
        { player1: firstWinner, player2: secondWinner, completed: false, timeLeft: 10 }
      ];
      this.startMatchTimer(this.secondRound[0], 'second', 0);
    },
    setWinner(winner) {
      this.winner = winner;
    }
  },
  beforeUnmount() {
    this.timers.forEach(timer => clearInterval(timer));
  }
};
</script>

<style scoped>
.matchmaking {
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
}

.status {
  font-weight: bold;
  padding: 5px;
  border-radius: 4px;
}

.timer {
  display: none;
}

.field {
  margin-bottom: 30px;
}

.winner {
  font-size: 1.5em;
  font-weight: bold;
  color: gold;
}

@media (max-width: 800px) {
  .matchmaking {
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
