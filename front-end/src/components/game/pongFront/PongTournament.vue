<template>
  <div>
    <CreateTournament v-if="currentStep === 'create'" @tournamentCreated="onTournamentCreated" @tournamentJoined="onTournamentJoined" />
    <WaitingPlayers v-if="currentStep === 'waiting'" :players="players" :isCreator="isCreator" :tournamentId="tournamentId" @startTournament="onStartTournament" />
    <Matchmaking v-if="currentStep === 'matchmaking'" :matches="currentMatches" @matchStart="onMatchStart" />
    <PongGame v-if="currentStep === 'game'" :matches="currentMatches" @gameEnded="onGameEnded" />
    <TournamentWinner v-if="currentStep === 'winner'" :winner="winner" @goBack="onGoBack" />
    <ConfirmQuitTournament v-if="showQuitConfirm" @confirm="handleQuitConfirm" @cancel="handleQuitCancel" />
  </div>
</template>

<script>
import CreateTournament from '@/components/game/tournament/CreateTournament.vue';
import WaitingPlayers from '@/components/game/tournament/WaitingPlayers.vue';
import Matchmaking from '@/components/game/tournament/Matchmaking.vue';
// import PongGame from '@/components/game/tournament/Game.vue';
import PongGame from '@/components/game/pongGame/PongLocal.vue';
import TournamentWinner from '@/components/game/tournament/Winner.vue';
import ConfirmQuitTournament from "@/components/game/tournament/ConfirmQuitTournament.vue";

export default {
  components: { CreateTournament, WaitingPlayers, Matchmaking, PongGame, TournamentWinner, ConfirmQuitTournament },
  data() {
    return {
      currentStep: 'create',
      tournamentId: '',
      players: [],
      matches: [],
      isCreator: false,
      winner: '',
      currentMatchIndex: 0,
      matchResults: [],
      currentMatches: [],
      showQuitConfirm: false,
      pendingRoute: null, // To store the pending route
    };
  },
  methods: {
    onTournamentCreated({ tournamentId }) {
      this.tournamentId = tournamentId;
      this.isCreator = true;
      this.currentStep = 'waiting';
      this.players = []; // Fetch players and update `this.players` as needed
    },
    onTournamentJoined(tournamentId) {
      this.tournamentId = tournamentId;
      this.currentStep = 'waiting';
      this.players = []; // Fetch players and update `this.players` as needed
    },
    onStartTournament() {
      this.currentStep = 'matchmaking';
      this.createInitialMatches();
    },
    createInitialMatches() {
      // Assuming players are in order: player1, player2, player3, player4
      this.matches = [
        { id: 1, player1: this.players[0], player2: this.players[1], completed: false, timeLeft: 5 },
        { id: 2, player1: this.players[2], player2: this.players[3], completed: false, timeLeft: 5 }
      ];
      this.currentMatches = this.matches.slice(0, 2);
    },
    onMatchStart() {
      this.currentStep = 'game';
    },
    onGameEnded(winner) {
      // Add the winner to the match results
      this.matchResults.push(winner);

      console.log(this.matchResults.length);
      console.log(this.currentMatchIndex);

      // Move to the next match
      this.currentMatchIndex++;

      if (this.matchResults.length === 2) {
        // Create the final match between the winners of the initial matches
        this.currentMatches = [
          { id: 3, player1: this.matchResults[0], player2: this.matchResults[1], completed: false, timeLeft: 5 }
        ];
        this.currentMatchIndex = 0;
        this.currentStep = 'matchmaking';
      } else if (this.matchResults.length === 3) {
        // Determine the tournament winner
        this.winner = this.matchResults[2];
        this.currentStep = 'winner';
      } else {
        // Continue to the next match
        this.currentStep = 'matchmaking';
      }
    },
    onGoBack() {
      this.showQuitConfirm = true;
    },
    handleQuitConfirm() {
      this.showQuitConfirm = false;

      // If there's a pending route, navigate to it
      if (this.pendingRoute) {
        this.$router.push(this.pendingRoute);
        this.pendingRoute = null;
      } else {
        // Reset the tournament state
        this.currentStep = 'create';
        this.tournamentId = '';
        this.players = [];
        this.matches = [];
        this.isCreator = false;
        this.winner = '';
        this.currentMatchIndex = 0;
        this.matchResults = [];
        this.currentMatches = [];
      }
    },
    handleQuitCancel() {
      this.showQuitConfirm = false;
      this.pendingRoute = null; // Clear the pending route
    }
  },
  beforeRouteLeave(to, from, next) {
    if (this.currentStep !== 'create' && this.currentStep !== 'winner') {
      this.showQuitConfirm = true;
      this.pendingRoute = to.path; // Store the pending route
      next(false); // Cancel the navigation
    } else {
      next(); // Allow the navigation
    }
  }
};
</script>
