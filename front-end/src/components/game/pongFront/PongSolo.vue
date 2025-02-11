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
  import PongAI from "@/components/game/pongGame/PongAI.js"; // import our AI module
  
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
		  console.log("PongGame instance available, commands can be used.");
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
	  onOpponentFound() {
		// Hide the Versus overlay to reveal the game content
		this.showVersus = false;
		const pongGameInstance = this.$refs.pongGameComponent;
		if (pongGameInstance) {
		  pongGameInstance.startGameLoop();
		  console.log("onOpponentFound: PongGame instance available, game can start.");
		  // Start the AI opponent:
		  PongAI.start(pongGameInstance);
		  console.log("PongAI.start() called.");
		}
	  },
	  // Optionally, implement handleTimeUp() if needed for other scenarios.
	  handleTimeUp() {
		// Your existing logic
		this.showVersus = false;
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
  