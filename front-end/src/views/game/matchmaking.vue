<template>
  <div class="matchmaking-container">
    <section v-if="phase === 'matchmaking'" class="matchmaking">
      <h1>Tournament Matchmaking</h1>
      <p>Game will start in {{ matchmakingCountdown }} seconds...</p>
      
      <!-- Transition group for first round -->
      <div class="round">
        <h2>First Round</h2>
        <transition-group name="match-transition" tag="div">
          <MatchItem
            v-for="(match, index) in firstRound"
            :key="'first-' + index"
            :match="match"
          />
        </transition-group>
      </div>
      
      <!-- Second round only if present -->
      <div class="round" v-if="secondRound.length">
        <h2>Second Round</h2>
        <transition-group name="match-transition" tag="div">
          <MatchItem
            v-for="(match, index) in secondRound"
            :key="'second-' + index"
            :match="match"
          />
        </transition-group>
      </div>
      
      <div class="winner" v-if="winner">
        <h2>Tournament Winner</h2>
        <TextBox :modelValue="winner" :modifiable="false" class="field" />
      </div>
    </section>

    <!-- Quit confirmation popup -->
    <ConfirmQuitTournament
      v-if="showQuitConfirm"
      @confirm="quitTournament"
      @cancel="showQuitConfirm = false"
    />
  </div>
</template>

<script>
import TextBox from "@/components/atoms/ModifyInformations.vue";
import ConfirmQuitTournament from "@/components/game/tournament/ConfirmQuitTournament.vue";
import MatchItem from "@/components/game/tournament/Matchmaking.vue";
export default {
  name: "Matchmaking",
  components: {
    TextBox,
    ConfirmQuitTournament,
    MatchItem
  },
  data() {
    return {
      phase: "matchmaking",
      firstRound: [
        { player1: "Player 1", player2: "Player 3", completed: false, timeLeft: 10 },
        { player1: "Player 2", player2: "Player 4", completed: false, timeLeft: 10 }
      ],
      secondRound: [],
      winner: null,
      timers: [],
      showQuitConfirm: false,
      matchmakingCountdown: 3,
      matchmakingTimer: null
    };
  },
  mounted() {
    this.startTimers();
    this.startMatchmakingCountdown();
  },
  methods: {
    startMatchmakingCountdown() {
      this.matchmakingTimer = setInterval(() => {
        if (this.matchmakingCountdown > 0) {
          this.matchmakingCountdown--;
        } else {
          clearInterval(this.matchmakingTimer);
          this.$emit("match-ready");
        }
      }, 1000);
    },
    startTimers() {
      // Start individual match timers
      this.firstRound.forEach((match, index) => {
        this.startMatchTimer(match, index);
      });
    },
    startMatchTimer(match, index) {
      const timer = setInterval(() => {
        if (match.timeLeft > 0) {
          match.timeLeft--;
        } else {
          clearInterval(timer);
          this.completeMatch(match, index);
        }
      }, 1000);
      this.timers.push(timer);
    },
    completeMatch(match, index) {
      match.completed = true;
      // Optionally determine a winner here, e.g. randomly
      const matchWinner = Math.random() < 0.5 ? match.player1 : match.player2;
      // You might update rounds or propagate events here
    },
    quitTournament() {
      this.$router.push("/game-choice");
      this.showQuitConfirm = false;
    }
  },
  beforeUnmount() {
    this.timers.forEach(timer => clearInterval(timer));
    if (this.matchmakingTimer) clearInterval(this.matchmakingTimer);
  }
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
.winner {
  font-size: 1.5em;
  font-weight: bold;
  color: gold;
}
/* Transition styles */
.match-transition-enter-active,
.match-transition-leave-active {
  transition: all 0.5s ease;
}
.match-transition-enter-from,
.match-transition-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
/* Responsive adjustments */
@media (max-width: 800px) {
  .matchmaking-container {
    padding: 10px;
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
