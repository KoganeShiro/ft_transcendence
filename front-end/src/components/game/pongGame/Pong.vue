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
      <canvas ref="pongCanvas" class="canvas" width="500" height="900"></canvas>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, onBeforeUnmount } from 'vue';
  import usePongGame from './usePongGame.js';
  
  const pongCanvas = ref(null);
  const { gameState, keysPressed, startGameLoop, handleKeyDown, handleKeyUp, handleTouchStart, handleTouchEnd, updateCanvas } = usePongGame(pongCanvas);
  
  onMounted(() => {
    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('keyup', handleKeyUp);
    pongCanvas.value.addEventListener('touchstart', handleTouchStart);
    pongCanvas.value.addEventListener('touchend', handleTouchEnd);
    startGameLoop();
  });
  
  onBeforeUnmount(() => {
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
  }
  
  .canvas {
    background-color: black;
  }
  </style>