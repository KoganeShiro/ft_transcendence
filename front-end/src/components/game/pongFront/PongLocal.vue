<template>
	<div class="pong-page">
	  <div class="content">

      <Versus v-if="showVersus" @time-up="handleTimeUp" />

      <div v-else class="content">
            <div class="left-cmd">
                <h2 class="mobile-hide">Commands</h2>
                <p class="mobile-hide">Move Up: <span class="span">W</span></p>
                <p class="mobile-hide">Move Down: <span class="span">S</span></p>
            </div>
            <div class="right-cmd">
                <h2 class="mobile-hide">Commands</h2>
                <p class="mobile-hide">Move Up: <span class="span">↑</span></p>
                <p class="mobile-hide">Move Down: <span class="span">↓</span></p>
            </div>
        </div>
		<div class="game-container">
		  <!-- This component handles the solo game logic -->
		  <!-- <PongLocal /> -->
			<div class="game-container">
				<PongGame />
			</div>
		</div>
	  </div>
</div>
  </template>
  
  <script>
  import PongGame from "@/components/game/PongGame.vue";
  import Versus from "@/components/game/Versus.vue";
  
  export default {
	name: 'SoloFront',
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
		// Hide the Versus overlay when the time is up
		this.showVersus = false;
	  },
	},
  };
  </script>
  
  <style scoped>
  .pong-page {
	color: #fff;
  }
  
  .span {
	font-weight: bold;
  }

  .player-controls {
    /* inline */
    display: flex;
  }

  .left-cmd {
	/* border: 2px solid #444; */
	border-radius: 8px;
	padding: 10px;
	background-color: #11101088;
	width: 30%;
	margin-left: 7%;
  }

  .right-cmd {
	/* border: 2px solid #444; */
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
  }

  @media screen and (max-width: 810px) {
  .mobile-hide {
	display: none;
  }

  .left-cmd {
    padding: 0px;
    background-color: node;
  }

  .right-cmd {
    padding: 0px;
    background-color: node;
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