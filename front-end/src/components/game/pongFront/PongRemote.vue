<template>
	<div class="pong-page">
	  <!-- Show Versus until the time is up -->
	  <Versus
		v-if="showVersus"
		:player1="localPlayer"
		:player2="opponentPlayer"
		@time-up="handleTimeUp"
	  />
	  
	  <!-- Once Versus is gone, show the game -->
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
		  <!-- PongRemote emits the players-update event -->
		  <PongRemote @players-update="updatePlayers" />
		  <WinnerPopup v-if="showWinner" :winnerName="winnerName" :winnerImage="winnerImage" />
		  <LoserPopup v-if="showLoser" :loserName="loserName" :loserImage="loserImage" />
		</div>
	  </div>
	</div>
  </template>
  
  <script>
  import PongRemote from "@/components/game/pongGame/PongRemote.vue";
  import Versus from "@/components/game/Versus.vue";
  import WinnerPopup from "@/views/game/winner.vue";
  import LoserPopup from "@/views/game/loser.vue";
  
  export default {
	name: 'RemoteFront',
	components: {
	  Versus,
	  PongRemote,
	  WinnerPopup,
	  LoserPopup,
	},
	data() {
	  return {
		showVersus: true,
		localPlayer: {
		  pseudo: 'Player 1',
		  imageUrl: '',
		  link: ''
		},
		opponentPlayer: {
		  pseudo: 'loading...',
		  imageUrl: '',
		  link: ''
		},
		// Additional data for popups (if needed)
		showWinner: false,
		showLoser: false,
		winnerName: '',
		winnerImage: '',
		loserName: '',
		loserImage: ''
	  };
	},
	methods: {
	  handleTimeUp() {
		this.showVersus = false;
	  },
	  updatePlayers({ localPlayer, opponentPlayer }) {
		// Update parent's state with the players data emitted by PongRemote
		this.localPlayer = localPlayer;
		this.opponentPlayer = opponentPlayer;
	  },
	},
  };
  </script>
  
  <style scoped>
  .pong-page {
	color: #fff;
	position: relative;
  }
  .content {
	padding: 20px;
	text-align: center;
  }
  .player-controls {
	margin: 20px auto;
	width: 30%;
	background-color: rgba(17, 16, 16, 0.53);
	border-radius: 8px;
	padding: 10px;
  }
  .username {
	display: flex;
	justify-content: space-between;
  }
  .player-left, .player-right {
	font-weight: bold;
	background-color: rgba(17, 16, 16, 0.53);
	border-radius: 8px;
	padding: 10px;
  }
  .player-left {
	margin-left: 50px;
  }
  .player-right {
	margin-right: 50px;
  }
  .game-container {
	margin-top: 20px;
	border-radius: 8px;
	padding: 10px;
	background-color: none;
  }
  @media screen and (max-width: 810px) {
	.mobile-hide {
	  display: none;
	}
	.player-controls {
	  width: 100%;
	  padding: 5px;
	  background: none;
	  border: none;
	}
	.game-container {
	  padding: 5px;
	  border: none;
	}
  }
  </style>
  