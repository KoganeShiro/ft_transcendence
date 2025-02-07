<template>
  <div class="tournament">
    <!-- Dynamic component renders the current phase's component -->
    <component
      :is="currentComponent"
      @tournament-created="handleTournamentCreated"
      @players-ready="handlePlayersReady"
      @match-ready="handleMatchReady"
      @match-ended="handleMatchEnded"
    />
  </div>
</template>

<script>
import CreateTournament from "@/components/game/CreateTournament.vue";
import WaitingPlayers from "@/views/game/waiting_players.vue";
import Matchmaking from "@/components/game/Matchmaking.vue";
import PongGame from "@/components/game/PongGame.vue";

export default {
  name: "TournamentPage",
  components: {
    CreateTournament,
    WaitingPlayers,
    Matchmaking,
    PongGame,
  },
  data() {
    return {
      phase: "create", // phases: 'create', 'waiting', 'matchmaking', 'game'
      tournamentData: {}, // Optionally store data from creation
    };
  },
  computed: {
    currentComponent() {
      // Map the current phase to a component name.
      // Note: make sure these component names match the ones you imported.
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
    handleMatchReady() {
      console.log("Matchmaking complete. Starting game.");
      this.phase = "game";
    },
    handleMatchEnded(result) {
      console.log("Match ended with result:", result);
      // You can then show a result/winner page or reset to a new tournament.
      // For demonstration, we'll reset the phase.
      this.phase = "create";
    },
  },
};
</script>

<style scoped>
.tournament {
  text-align: center;
}
</style>
