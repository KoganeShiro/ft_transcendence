<template>
	<div class="pong-page">
	  <!-- Game content (commands and canvas) is hidden while showVersus is true -->
	  <div class="content" v-show="!showVersus">
		<div class="player-controls">
		  <h2 class="mobile-hide">{{ $t('commands') }}</h2>
		  <p class="mobile-hide">
			{{ $t('move-up') }}<span class="span">W</span>
		  </p>
		  <p class="mobile-hide">
			{{ $t('move-down') }} <span class="span">S</span>
		  </p>
		</div>
		<div class="game-container">
		  <!-- PongGame is always mounted so its methods remain available -->
		  <PongGame ref="pongGameComponent" />
		</div>
	  </div>
	  <!-- Versus overlay displayed when showVersus is true -->
	  <Versus v-if="showVersus" @time-up="handleTimeUp" class="versus-overlay" />
	</div>
  </template>
  
  <script>
  import Versus from "@/components/game/Versus.vue";
  import PongGame from "@/components/game/pongGame/PongGame.vue";
  
  export default {
	name: 'SoloFront',
	components: {
	  Versus,
	  PongGame,
	},
	data() {
	  return {
		showVersus: true, // Initially showing the overlay, so commands and canvas are hidden
	  };
	},
	mounted() {
	  // Although the content is hidden via v-show, the PongGame instance is still mounted.
	  this.$nextTick(() => {
		const pongGameInstance = this.$refs.pongGameComponent;
		if (pongGameInstance) {
		  // To move the paddle upward, use handleKeyDown instead of handleKeyUp.
		  pongGameInstance.handleKeyDown({ key: 'w' });
		} else {
		  console.error("PongGame instance is not defined");
		}
	  });
  
	  // Wait for an opponent, then call onOpponentFound:
	  setTimeout(() => {
		console.log("Opponent found, starting game loop.");
		this.onOpponentFound();
	  }, 3000);
	},
	methods: {
	  handleTimeUp() {
		// Hide the Versus overlay when the time is up, revealing the game content
		this.showVersus = false;
		this.$nextTick(() => {
		  const pongGameInstance = this.$refs.pongGameComponent;
		  if (pongGameInstance) {
			// To simulate a key press (e.g., moving the paddle upward), use handleKeyDown.
			pongGameInstance.handleKeyDown({ key: 'w' });
			
			// ********* Place to call your AI logic *********
			// Here you can start your AI match.
			// For example, you could call:
			// this.startAIMatch();
			// or invoke a method on the PongGame component that starts the AI agent:
			// pongGameInstance.startAIAgent();
			// ************************************************
		  }
		});
	  },
	  // Uncomment and implement this method to integrate your AI logic.
	  // startAIMatch() {
	  //   // Your AI logic here.
	  // },
	  onOpponentFound() {
		// Hide the Versus overlay to reveal the game content
		this.showVersus = false;
		const pongGameInstance = this.$refs.pongGameComponent;
		if (pongGameInstance) {
		  pongGameInstance.startGameLoop();
		  console.log("onOpponentFound: PongGame instance available, game can start.");
		}
	  }
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
	background-color: rgba(17, 16, 16, 0.39);
	border-radius: 8px;
	padding: 10px;
  }
  .game-container {
	margin-top: 20px;
	border-radius: 8px;
	padding: 10px;
  }
  
  @media screen and (max-width: 810px) {
	.mobile-hide {
	  display: none;
	}
	.player-controls {
	  width: 100%;
	  margin: 0px;
	  padding: 0px;
	  background: none;
	  border: none;
	}
	.game-container {
	  padding: 0px;
	  border: none;
	  margin: 0px;
	}
	.content {
		padding: 25px;
	}
  }
  </style>
  