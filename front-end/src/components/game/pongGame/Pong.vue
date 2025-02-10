<!-- <template>
    <div id="pongField">
      <canvas ref="pongCanvas" class="canvas" width="900" height="500"></canvas>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, onBeforeUnmount } from 'vue';
  import usePongGame from './usePongGame.js';
  
  const pongCanvas = ref(null);
  const { gameState, keysPressed, startGameLoop, handleKeyDown, handleKeyUp, updateCanvas } = usePongGame(pongCanvas);
  
  onMounted(() => {
    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('keyup', handleKeyUp);
    startGameLoop();
    setTimeout(() => {
      const result = { winner: "Player 1" }; // Replace with actual game logic
      // emit event if needed
    }, 15000);
  });
  
  onBeforeUnmount(() => {
    window.removeEventListener('keydown', handleKeyDown);
    window.removeEventListener('keyup', handleKeyUp);
    cancelAnimationFrame(gameState.value.gameLoop);
  });
  </script> -->
  <template>
    <div id="pongField">
      <canvas ref="pongCanvas" class="canvas" :width="canvasWidth" :height="canvasHeight"></canvas>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, onBeforeUnmount } from 'vue';
  import usePongGame from './usePongGame';
  
  const pongCanvas = ref(null);
  const canvasWidth = ref(900);
  const canvasHeight = ref(500);
  
  const { gameState, keysPressed, startGameLoop, handleKeyDown, handleKeyUp, handleTouchStart, handleTouchEnd, updateCanvas } = usePongGame(pongCanvas);
  
  const updateCanvasSize = () => {
    if (window.innerWidth <= 768) { // Mobile
      canvasWidth.value = window.innerWidth * 0.9;
      canvasHeight.value = window.innerHeight * 0.5;
    } else if (window.innerWidth <= 1024) { // Tablet
      canvasWidth.value = window.innerWidth * 0.8;
      canvasHeight.value = window.innerHeight * 0.6;
    } else { // Desktop
      canvasWidth.value = 900;
      canvasHeight.value = 500;
    }
  };
  
  onMounted(() => {
    updateCanvasSize();
    window.addEventListener('resize', updateCanvasSize);
    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('keyup', handleKeyUp);
    pongCanvas.value.addEventListener('touchstart', handleTouchStart);
    pongCanvas.value.addEventListener('touchend', handleTouchEnd);
    startGameLoop();
    setTimeout(() => {
      const result = { winner: "Player 1" }; // Replace with actual game logic
      // emit event if needed
    }, 15000);
  });
  
  onBeforeUnmount(() => {
    window.removeEventListener('resize', updateCanvasSize);
    window.removeEventListener('keydown', handleKeyDown);
    window.removeEventListener('keyup', handleKeyUp);
    pongCanvas.value.removeEventListener('touchstart', handleTouchStart);
    pongCanvas.value.removeEventListener('touchend', handleTouchEnd);
    cancelAnimationFrame(gameState.value.gameLoop);
  });
  </script>
  
  <style>
  #pongField {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
  }
  
  .canvas {
    background-color: black;
  }
  
  @media (max-width: 768px) {
    .canvas {
      width: 90vw;
      height: 50vh;
    }
  }
  
  @media (max-width: 1024px) {
    .canvas {
      width: 80vw;
      height: 60vh;
    }
  }
  </style>