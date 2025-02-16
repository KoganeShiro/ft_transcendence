
  <template>
	<div class="pong-page">
	  <div class="game-container">
		<PongRemote 
		  @players-update="updatePlayers" 
		  @opponent-found="handleOpponentFound"
		  @game-over="handleGameOver" />
		<WinnerPopup 
		  v-if="showWinner" 
		  :winnerName="winnerName" 
		  :winnerImage="winnerImage" />
		<LoserPopup 
		  v-if="showLoser" 
		  :loserName="loserName" 
		  :loserImage="loserImage" />
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
			this.showLoser = false;
		} else if (gameOverData.type === 'loss') {
			this.loserName = gameOverData.loserName;
			this.loserImage = gameOverData.loserImage;
			this.showWinner = false;
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