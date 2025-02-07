<template>
	<div class="pong-page">
	  <Versus v-if="showVersus" @time-up="handleTimeUp" />
	  
	  <div v-else class="content">
		<div class="player-controls">
		  <h2 class="mobile-hide">Commands</h2>
		  <p class="mobile-hide">Move Up: <span class="span">W</span></p>
		  <p class="mobile-hide">Move Down: <span class="span">S</span></p>
		</div>
		<div class="game-container">
		  <PongGame />
		</div>
	  </div>
	</div>
  </template>
  
  <script>
  import PongGame from "@/components/game/PongGame.vue";
  import Versus from "@/components/game/Versus.vue";
  
  export default {
	name: 'RemoteFront',
	components: {
	  Versus,
	  PongGame,
	},
	data() {
	  return {
		showVersus: true,
	  };
	},
	methods: {
	  handleTimeUp() {
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
	background-color: rgba(17, 16, 16, 0.53);
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
  