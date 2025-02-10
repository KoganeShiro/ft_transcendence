<template>
    <div id="pongField">
      <canvas ref="pongCanvas" class="canvas" width="500" height="900"></canvas>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, onBeforeUnmount } from 'vue';
  import { PongGame } from '@/components/game/pongGame/PongGame.js';
  
  const pongCanvas = ref(null);
  let pongGameInstance;
  
  onMounted(() => {
    pongGameInstance = new PongGame(pongCanvas.value);
    window.addEventListener('keydown', pongGameInstance.handleKeyDown);
    window.addEventListener('keyup', pongGameInstance.handleKeyUp);
    pongCanvas.value.addEventListener('touchstart', pongGameInstance.handleTouchStart);
    pongCanvas.value.addEventListener('touchend', pongGameInstance.handleTouchEnd);
    pongGameInstance.startGameLoop();
  });
  
  onBeforeUnmount(() => {
    window.removeEventListener('keydown', pongGameInstance.handleKeyDown);
    window.removeEventListener('keyup', pongGameInstance.handleKeyUp);
    pongCanvas.value.removeEventListener('touchstart', pongGameInstance.handleTouchStart);
    pongCanvas.value.removeEventListener('touchend', pongGameInstance.handleTouchEnd);
    cancelAnimationFrame(pongGameInstance.gameState.gameLoop);
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