<template>
  <div>
    <CreateTournament v-if="currentStep === 'create'" @tournamentCreated="onTournamentCreated" @tournamentJoined="onTournamentJoined" />
    <WaitingPlayers v-if="currentStep === 'waiting'" :players="players" :isCreator="isCreator" @startTournament="onStartTournament" />
    <Matchmaking v-if="currentStep === 'matchmaking'" :matches="currentMatches" @matchStart="onMatchStart" />
    <PongGame v-if="currentStep === 'game'" @gameEnded="onGameEnded" />
    <TournamentWinner v-if="currentStep === 'winner'" :winner="winner" @goBack="onGoBack" />
  </div>

  <!-- Quit confirmation popup -->
  <ConfirmQuitTournament 
      v-if="showQuitConfirm"
      @confirm="handleQuitConfirm" 
      @cancel="handleQuitCancel" 
    />
</template>

<script>
import CreateTournament from '@/components/game/tournament/CreateTournament.vue';
import WaitingPlayers from '@/components/game/tournament/WaitingPlayers.vue';
import Matchmaking from '@/components/game/tournament/Matchmaking.vue';
import PongGame from '@/components/game/tournament/Game.vue';
import TournamentWinner from '@/components/game/tournament/Winner.vue'; // Ensure this path is correct
import ConfirmQuitTournament from "@/components/game/tournament/ConfirmQuitTournament.vue";

export default {
  components: { CreateTournament, WaitingPlayers, Matchmaking, PongGame, TournamentWinner, ConfirmQuitTournament },
  props: {
    mode: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      currentStep: 'create', // Ensure this is defined and initialized
      tournamentId: '',
      players: [],
      matches: [],
      isCreator: false,
      winner: '',
      currentMatchIndex: 0,
      matchResults: [],
      currentMatches: []
    };
  },
  methods: {
    onTournamentCreated(id) {
      this.tournamentId = id;
      this.isCreator = true;
      this.currentStep = 'waiting';
      // Add logic to fetch players and update `this.players`
    },
    onTournamentJoined(id) {
      this.tournamentId = id;
      this.currentStep = 'waiting';
      // Add logic to fetch players and update `this.players`
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
      // Determine next match or winner
      const match = this.currentMatches[this.currentMatchIndex];
      match.winner = winner;
      match.completed = true;

      this.matchResults.push(winner);

      // Move to next match
      this.currentMatchIndex++;
      console.log(this.currentMatchIndex);

      if (this.currentMatchIndex === 2) {
        // Create final match
        this.currentMatches = [
          { id: 3, player1: this.matchResults[0], player2: this.matchResults[1], completed: false, timeLeft: 5 }
        ];
        this.currentMatchIndex = 0;
        this.currentStep = 'matchmaking';
      } else if (this.currentMatchIndex === 1 && this.currentMatches.length === 1) {
        // Tournament winner
        this.winner = this.matchResults[0];
        this.currentStep = 'winner';
      } else {
        this.currentStep = 'matchmaking';
      }
    },
    onGoBack() {
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
  }
};
</script>