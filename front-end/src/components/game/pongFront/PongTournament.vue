<template>
  <div>
    <WaitingPlayers 
      v-if="currentStep === 'waiting'" 
      :players="players" 
      :isCreator="isCreator" 
      :tournamentId="tournamentId" 
      @startTournament="onStartTournament"
      @updatePlayerNames="onUpdatePlayerNames" 
    />
    <Matchmaking 
      v-if="currentStep === 'matchmaking'" 
      :matches="matches" 
      @matchStart="onMatchStart" 
    />

    <PongGame 
      v-if="currentStep === 'game'" 
      :matches="currentMatches" 
      @gameEnded="onGameEnded" 
    />
    <TournamentWinner 
      v-if="currentStep === 'winner'" 
      :winner="winner" 
      @goBack="onGoBack" 
    />
  </div>
</template>

<script>
import WaitingPlayers from '@/components/game/tournament/WaitingPlayers.vue';
import Matchmaking from '@/components/game/tournament/Matchmaking.vue';
import PongGame from '@/components/game/pongGame/PongLocal.vue';
import TournamentWinner from '@/components/game/tournament/Winner.vue';

export default {
  components: { WaitingPlayers, Matchmaking, PongGame, TournamentWinner },
  data() {
    return {
      currentStep: 'waiting',
      tournamentId: '',
      players: [],
      matches: [],
      isCreator: false,
      winner: '',
      currentMatchIndex: 0,
      matchResults: [],
      currentMatches: [],
      showQuitConfirm: false,
      pendingRoute: null,
      loading: false,
    };
  },
  methods: {
    onStartTournament() {
      this.currentStep = 'matchmaking';
      this.createRandomMatches();
    },
    onUpdatePlayerNames(playerNames) {
      this.players = playerNames.map(name => ({ name }));
      console.log("Updated player names:", this.players);
    },
    shuffleArray(array) {
      for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
      }
    },
    createRandomMatches() {
      if (this.loading) {
        console.log("createRandomMatches is already in progress");
        return;
      }
      console.log("createRandomMatches called");
      this.loading = true;
      this.shuffleArray(this.players);
      this.matches = [
        { id: 1, player1: this.players[0].name, player2: this.players[1].name, completed: false, timeLeft: 5 },
        { id: 2, player1: this.players[2].name, player2: this.players[3].name, completed: false, timeLeft: 5 }
      ];
      console.log(this.players[0].name, 'vs', this.players[1].name);
      console.log(this.players[2].name, 'vs', this.players[3].name);
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
  },
};
</script>