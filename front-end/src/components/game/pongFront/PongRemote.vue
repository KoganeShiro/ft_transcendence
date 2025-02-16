<!-- <template>
	<div class="pong-page">
	  <Versus
		v-if="showVersus"
		:player1="localPlayer"
		:player2="opponentPlayer"
		@time-up="handleTimeUp"
	  />
	  
	  <div v-else class="content">
		<div class="player-controls">
		  <h2 class="mobile-hide">{{ $t('commands') }}</h2>
		  <p class="mobile-hide">{{ $t('move-up') }}<span class="span">↑</span></p>
		  <p class="mobile-hide">{{ $t('move-down') }} <span class="span">↓</span></p>
		</div>
		<div class="username">
		  <p class="player-left">{{ localPlayer.pseudo }}</p>
		  <p class="player-right">{{ opponentPlayer.pseudo }}</p>
		</div>
		<div class="game-container">
		  <PongRemote @players-update="updatePlayers" @opponent-found="handleOpponentFound" />
		  <WinnerPopup v-if="showWinner" :winnerName="winnerName" :winnerImage="winnerImage" />
		  <LoserPopup v-if="showLoser" :loserName="loserName" :loserImage="loserImage" />
		</div>
	  </div>
	</div>
  </template> -->

  <template>
	<div class="pong-page">
	  <div class="game-container">
		<PongRemote 
		  @players-update="updatePlayers" 
		  @opponent-found="handleOpponentFound"
		  @game-over="handleGameOver" />
		<WinnerPopup v-if="showWinner" :winnerName="winnerName" :winnerImage="winnerImage" />
		<LoserPopup v-if="showLoser" :loserName="loserName" :loserImage="loserImage" />
	  </div>
	</div>
  </template>
  
  <script>
  import PongRemote from "@/components/game/pongGame/PongRemote.vue";
  import WinnerPopup from "@/views/game/winner.vue";
  import LoserPopup from "@/views/game/loser.vue";
  
  export default {
	name: 'RemoteFront',
	components: { PongRemote, WinnerPopup, LoserPopup },
	data() {
	  return {
		localPlayer: { pseudo: 'Player 1', imageUrl: '' },
		opponentPlayer: { pseudo: 'loading...', imageUrl: '' },
		showWinner: false,
		showLoser: false,
		winnerName: '',
		winnerImage: '',
		loserName: '',
		loserImage: ''
	  };
	},
	methods: {
	  updatePlayers({ localPlayer, opponentPlayer }) {
		console.log("[RemoteFront] updatePlayers:", localPlayer, opponentPlayer);
		this.localPlayer = localPlayer;
		this.opponentPlayer = opponentPlayer;
	  },
	  handleOpponentFound() {
		console.log("[RemoteFront] Opponent found event received.");
	  },
	  handleGameOver(gameOverData) {
		console.log("[RemoteFront] Game over event received:", gameOverData);
		if (gameOverData.type === 'win') {
		  this.winnerName = gameOverData.winnerName;
		  this.winnerImage = gameOverData.winnerImage;
		  this.showWinner = true;
		} else if (gameOverData.type === 'loss') {
		  this.loserName = gameOverData.loserName;
		  this.loserImage = gameOverData.loserImage;
		  this.showLoser = true;
		}
	  },
	},
  };
  </script>
  

  
  <style scoped>
  .pong-page {
	position: relative;
  }

  </style>