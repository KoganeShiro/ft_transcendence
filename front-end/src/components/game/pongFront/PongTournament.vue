<template>
  <div class="tournament">
    <component
      :is="currentComponent"
      :tournamentId="tournamentData.tournamentCode"
      :isCreator="tournamentData.isCreator"
      :playerCount="tournamentData.playerCount"
      :playerNames="playerNames"
      :matchData="matchData"
      :winner="winner"
      @tournament-created="handleTournamentCreated"
      @tournament-joined="handleTournamentJoined"
      @players-ready="handlePlayersReady"
      @match-ready="handleMatchReady"
      @match-ended="handleMatchEnded"
      @quit-tournament="handleQuitTournament"
    />


    <!-- Quit confirmation popup -->
    <ConfirmQuitTournament 
      v-if="showQuitConfirm"
      @confirm="handleQuitConfirm" 
      @cancel="handleQuitCancel" 
    />
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import CreateTournament from "@/components/game/tournament/CreateTournament.vue";
import WaitingPlayers from "@/views/game/waiting_players.vue";
import Matchmaking from "@/components/game/tournament/Matchmaking.vue";
import PongGame from "@/components/game/pongGame/PongGame.vue";
import ConfirmQuitTournament from "@/components/game/tournament/ConfirmQuitTournament.vue";

export default {
  name: "TournamentPage",
  components: {
    CreateTournament,
    WaitingPlayers,
    Matchmaking,
    PongGame,
    ConfirmQuitTournament,
  },
  data() {
    return {
      currentComponent: 'CreateTournament',
      tournamentData: {
        tournamentCode: '',
        isCreator: false,
        playerCount: 4
      },
      playerNames: [],
      matchData: [],
      winner: null,
      showQuitConfirm: false
    };
  },
  methods: {
    handleTournamentCreated(data) {
      this.tournamentData = { ...data, isCreator: true };
      this.currentComponent = 'WaitingPlayers';
    },
    handleTournamentJoined(data) {
      this.tournamentData = { ...data, isCreator: false };
      this.currentComponent = 'WaitingPlayers';
    },
    handlePlayersReady(players) {
      this.playerNames = players;
      this.currentComponent = 'Matchmaking';
    },
    handleMatchReady() {
      this.currentComponent = 'PongGame';
    },
    handleMatchEnded(result) {
      this.matchData.push(result);
      if (this.tournamentIsOver()) {
        this.winner = this.determineWinner();
        this.currentComponent = 'Matchmaking'; // To display final results
      } else {
        this.currentComponent = 'Matchmaking'; // For next round
      }
    },
    handleQuitTournament() {
      this.showQuitConfirm = true;
    },
    tournamentIsOver() {
      // Logic to determine if the tournament is over
    },
    determineWinner() {
      // Logic to determine the tournament winner
    }
  },

  setup() {
    const phase = ref('create');
    const tournamentData = ref({});
    const showQuitConfirm = ref(false);
    const pendingNavigation = ref(null);
    let timer = null;

    const currentComponent = computed(() => {
      switch (phase.value) {
        case "create":
          return "CreateTournament";
        case "waiting":
          return "WaitingPlayers";
        case "matchmaking":
          return "Matchmaking";
        case "game":
          return "PongGame";
        default:
          return "CreateTournament";
      }
    });

    const handleTournamentCreated = (data) => {
      console.log("Tournament created:", data);
      tournamentData.value = data;
      startTournament();
    };

    const startTournament = () => {
      phase.value = 'waiting';
      timer = setTimeout(() => {
        phase.value = 'matchmaking';
        timer = setTimeout(() => {
          phase.value = 'game';
          timer = setTimeout(() => {
            phase.value = 'matchmaking';
            timer = setTimeout(() => {
              phase.value = 'game';
              timer = setTimeout(() => {
                phase.value = 'create';
                console.log("Tournament ended");
              }, 15000); // Game 2 duration: 15 seconds
            }, 5000); // Matchmaking 2 duration: 5 seconds
          }, 15000); // Game 1 duration: 15 seconds
        }, 5000); // Matchmaking 1 duration: 5 seconds
      }, 10000); // Waiting players duration: 10 seconds
    };

    const attemptNavigation = (targetRoute) => {
      pendingNavigation.value = targetRoute;
      showQuitConfirm.value = true;
    };

    const handleQuitConfirm = () => {
      if (pendingNavigation.value) {
        // Implement router push here
        console.log("Navigating to:", pendingNavigation.value);
      }
      pendingNavigation.value = null;
      showQuitConfirm.value = false;
    };

    const handleQuitCancel = () => {
      pendingNavigation.value = null;
      showQuitConfirm.value = false;
    };

    onMounted(() => {
      // Any setup code if needed
    });

    onUnmounted(() => {
      if (timer) {
        clearTimeout(timer);
      }
    });

    return {
      phase,
      currentComponent,
      tournamentData,
      showQuitConfirm,
      handleTournamentCreated,
      attemptNavigation,
      handleQuitConfirm,
      handleQuitCancel
    };
  }
};
</script>



<!-- 
<script>
import CreateTournament from "@/components/game/tournament/CreateTournament.vue";
import WaitingPlayers from "@/views/game/waiting_players.vue";
import Matchmaking from "@/components/game/tournament/Matchmaking.vue";
import PongGame from "@/components/game/pongGame/PongGame.vue";
import ConfirmQuitTournament from "@/components/game/tournament/ConfirmQuitTournament.vue";

export default {
  name: "TournamentPage",
  components: {
    CreateTournament,
    WaitingPlayers,
    Matchmaking,
    PongGame,
    ConfirmQuitTournament,
  },
  data() {
    return {
      phase: "create", // phases: 'create', 'waiting', 'matchmaking', 'game'
      tournamentData: {},
      showQuitConfirm: false,
      pendingNavigation: null,
    };
  },
  // setup() {
  //   const socket = ref(null);
  //   const phase = ref('create');

  //   onMounted(() => {
  //     socket.value = new WebSocket('ws://your-backend-url');
      
  //     socket.value.onmessage = (event) => {
  //       const data = JSON.parse(event.data);
  //       handleServerMessage(data);
  //     };
  //   });

  //   onUnmounted(() => {
  //     if (socket.value) {
  //       socket.value.close();
  //     }
  //   });

  //   const handleServerMessage = (data) => {
  //     switch (data.type) {
  //       case 'tournament_created':
  //         phase.value = 'waiting';
  //         break;
  //       case 'players_ready':
  //         phase.value = 'matchmaking';
  //         break;
  //       case 'match_ready':
  //         phase.value = 'game';
  //         break;
  //       case 'match_ended':
  //         phase.value = 'matchmaking';
  //         break;
  //     }
  //   };

  //   return { phase };
  // },
  computed: {
    currentComponent() {
      switch (this.phase) {
        case "create":
          return "CreateTournament";
        case "waiting":
          return "WaitingPlayers";
        case "matchmaking":
          return "Matchmaking";
        case "game":
          return "PongGame";
        default:
          return "CreateTournament";
      }
    },
  },
  methods: {
    handleTournamentCreated(data) {
      console.log("Tournament created:", data);
      this.tournamentData = data;
      this.phase = "waiting";
    },
    handlePlayersReady() {
      console.log("All players are ready");
      this.phase = "matchmaking";
    },
    // When Matchmaking is done (after 5s), transition to the game phase.
    handleMatchReady() {
      console.log("Matchmaking complete. Starting Pong game.");
      this.phase = "game";
    },
    // When the Pong game ends (after 15s or game result), handle the match result.
    handleMatchEnded(result) {
      console.log("Match ended with result:", result);
      // Here you could process the result, update rounds, etc.
      // Then transition back to matchmaking for the next round.
      this.phase = "matchmaking";
    },
    attemptNavigation(targetRoute) {
      this.pendingNavigation = targetRoute;
      this.showQuitConfirm = true;
    },
    handleQuitConfirm() {
      if (this.pendingNavigation) {
        this.$router.push(this.pendingNavigation);
      }
      this.pendingNavigation = null;
      this.showQuitConfirm = false;
    },
    handleQuitCancel() {
      this.pendingNavigation = null;
      this.showQuitConfirm = false;
    },
  },
};
</script> -->

<style scoped>
.tournament {
  text-align: center;
}
</style>