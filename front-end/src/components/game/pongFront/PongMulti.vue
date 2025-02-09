<template>
	<div class="pong-page">
	  <div class="content">
		<!-- <Versus /> -->
		<div class="player-controls">
		  <h2 class="mobile-hide">Commands</h2>
		  <h2 class="mobile-hide">{{ $t('commands') }}</h2>
          <p class="mobile-hide">{{ $t('move-up') }}<span class="span">W</span></p>
          <p class="mobile-hide">{{ $t('move-down') }} <span class="span">S</span></p>
		</div>
		<div class="game-container">
		  <!-- This component handles the solo game logic -->
		  <!-- <PongFourPlayer /> -->
			<div class="game-container">
				<h1>4 Player Mode</h1>
			</div>
		</div>
	  </div>
</div>
  </template>
  
  <script>
  import HeaderOrganism from '@/components/header/navbar.vue';
  import FooterOrganism from '@/components/footer.vue';
  // import PongFourPlayer from '@/components/game/pongGame/PongFourPlayer.vue'; 
  import PongGame from "@/components/game/pongGame/PongGame.vue";
  import Versus from "@/components/game/Versus.vue";

  
  export default {
	name: 'SoloFront',
	components: {
	  HeaderOrganism,
	  FooterOrganism,
	  Versus,
	  PongGame,
	  // PongFourPlayer,
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
	/* border: 2px solid #444; */
	border-radius: 8px;
	padding: 10px;
	background-color: #11101088;
	width: 30%;
	margin-left: 20%;
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