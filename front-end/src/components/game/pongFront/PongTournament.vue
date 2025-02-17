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
    <Versus 
      v-if="currentStep === 'versus'" 
      :player1="activeMatches[currentMatchIndex]?.player1" 
      :player2="activeMatches[currentMatchIndex]?.player2"
      @time-up="onVersusTimeUp"
    />
    <div class="player-controls" v-if="currentStep === 'game'" >
        <div class="left-cmd">
          <h2 class="mobile-hide">{{ $t('commands') }}</h2>
          <p class="mobile-hide">{{ $t('move-up') }}<span class="span">W</span></p>
          <p class="mobile-hide">{{ $t('move-down') }} <span class="span">S</span></p>
        </div>
        <div class="right-cmd">
          <h2 class="mobile-hide">{{ $t('commands') }}</h2>
          <p class="mobile-hide">{{ $t('move-up') }}<span class="span">↑</span></p>
          <p class="mobile-hide">{{ $t('move-down') }} <span class="span">↓</span></p>
        </div>
      </div>

    <PongGame class="game-container"
      v-if="currentStep === 'game'" 
      :matches="currentMatches" 
      @gameEnded="onGameEnded" 
    />
    <WinnerPopup 
      v-if="currentStep === 'winnerPopup'" 
      :winner="currentMatchWinner" 
      @dismiss="onWinnerPopupDismiss"
    />
    <TournamentWinner 
      v-if="currentStep === 'tournamentWinner'" 
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
import Versus from '@/components/game/tournament/Versus.vue';
import WinnerPopup from "@/components/game/tournament/winnerpopup.vue";

export default {
  components: { WaitingPlayers, Matchmaking, PongGame, TournamentWinner, Versus, WinnerPopup },
  data() {
    return {
      currentStep: 'waiting',
      tournamentId: '',
      players: [],
      matches: [],
      currentMatches: [],  // for round 2 (final match)
      currentRound: 1,
      isCreator: false,
      winner: '',          // final tournament winner
      currentMatchWinner: {}, // intermediate match winner
      currentMatchIndex: 0,
      matchResults: [],
      showQuitConfirm: false,
      pendingRoute: null,
      loading: false,
    };
  },

  computed: {
    // Returns the correct matches array based on the current round.
    activeMatches() {
      return this.currentRound === 1 ? this.matches : this.currentMatches;
    }
  },
  methods: {
    onStartTournament() {
      this.currentStep = 'matchmaking';
      this.createRandomMatches();
    },
    onUpdatePlayerNames(playerNames) {
      // Map each name into an object with a "name" property.
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
        { id: 1, player1: this.players[0], player2: this.players[1], completed: false, timeLeft: 5 },
        { id: 2, player1: this.players[2], player2: this.players[3], completed: false, timeLeft: 5 }
      ];
      console.log(this.players[0].name, 'vs', this.players[1].name);
      console.log(this.players[2].name, 'vs', this.players[3].name);
    },
    onMatchStart() {
      // Use activeMatches for the current round.
      if (this.activeMatches.length > 0 && this.currentMatchIndex < this.activeMatches.length) {
        console.log('Match started:', this.activeMatches[this.currentMatchIndex]);
        console.log('Current round:', this.currentRound);
        console.log(this.activeMatches[this.currentMatchIndex]?.player1);
        console.log(this.activeMatches[this.currentMatchIndex]?.player2);
        this.currentStep = 'versus';
      } else {
        console.error('Invalid activeMatches or currentMatchIndex');
      }
    },
    onVersusTimeUp() {
      this.currentStep = 'game';
    },
    onGameEnded(matchWinner) {
      //weird, the winner isn't goods
      console.log('Match winner:', matchWinner);
      if (matchWinner === 'Opponent') {
        console.log('Opponent');
        matchWinner = this.activeMatches[this.currentMatchIndex].player2.name;
      }
      else {
        matchWinner = this.activeMatches[this.currentMatchIndex].player1.name;
      }
      this.matchResults.push(matchWinner);
      // Store this winner for display in the popup.
      this.currentMatchWinner = { name: matchWinner };
      // Show the winner popup.
      this.currentStep = 'winnerPopup';
    },

    // Called when the winner popup is dismissed (via a button click or timer).
    onWinnerPopupDismiss() {
      if (this.currentRound === 1) {
        // In round 1, there are 2 matches.
        if (this.currentMatchIndex < this.activeMatches.length - 1) {
          // There is another match in round 1.
          this.currentMatchIndex++;
          this.currentStep = 'matchmaking';
        } else {
          // Both round 1 matches are done.
          // Set up the final match using the two winners.
          this.currentMatches = [
            { 
              id: 3, 
              player1: { name: this.matchResults[0] },
              player2: { name: this.matchResults[1] },
              completed: false,
              timeLeft: 5
            }
          ];
          // Switch to round 2.
          this.currentRound = 2;
          this.currentMatchIndex = 0;
          // Go back to matchmaking to start the final match.
          this.currentStep = 'matchmaking';
        }
      } else if (this.currentRound === 2) {
        // In round 2, after the final match, the winner (the third result) is the tournament winner.
        this.winner = this.matchResults[2];
        this.currentStep = 'tournamentWinner';
      }
    },
    onGoBack() {
      this.$router.push('/game-choice');
    }
  },
};
</script>

<style scoped>
.player-controls {
  display: flex;
}

.left-cmd {
  border-radius: 8px;
  padding: 10px;
  background-color: #11101088;
  width: 30%;
  margin-left: 7%;
}

.right-cmd {
  border-radius: 8px;
  padding: 10px;
  background-color: #11101088;
  width: 30%;
  margin-left: 25%;
}

.content {
  padding: 20px;
  text-align: center;
}

.game-container {
  border-radius: 8px;
  padding: 10px;
  background-color: none;
}

@media screen and (max-width: 810px) {
  .mobile-hide {
    display: none;
  }

  .left-cmd {
    padding: 0;
    background-color: transparent;
  }

  .right-cmd {
    padding: 0;
    background-color: transparent;
  }

  .player-controls {
    padding: 5px;
    background: none;
    border: none;
  }

  .game-container {
    padding: 5px;
    border: none;
  }
}

@media screen and (max-width: 410px) {
  .game-container {
    border: none;
  }
}
</style>