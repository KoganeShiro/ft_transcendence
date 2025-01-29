<template>
    <div class="pong-game">
      <canvas ref="pongCanvas"></canvas>
    </div>
  </template>
  
  <script>
  import { onMounted, ref, onBeforeUnmount } from "vue";
  
  export default {
    props: {
      mode: String, // "local", "solo", "remote"
    },
    setup(props) {
      const pongCanvas = ref(null);
      let animationFrameId = null;
  
      const handleResize = () => {
        const canvas = pongCanvas.value;
        if (!canvas) return;
        const isMobile = window.innerWidth <= 768;
  
        if (isMobile) {
          // Portrait mode for mobile
          canvas.width = window.innerWidth * 0.95;
          canvas.height = window.innerHeight * 0.7;
        } else {
          // Landscape mode for desktop
          canvas.width = 800;
          canvas.height = 400;
        }
        initGame();
      };
  
      const initGame = () => {
        const canvas = pongCanvas.value;
        if (!canvas) return;
        const ctx = canvas.getContext("2d");
        const isMobile = window.innerWidth <= 768;
  
        // Game settings based on device type
        const settings = isMobile ? {
          // Mobile (Portrait) settings
          paddleWidth: canvas.width * 0.15,
          paddleHeight: canvas.width * 0.02,
          paddleOffset: canvas.height * 0.05,
          ballSize: canvas.width * 0.02,
          ballSpeedX: canvas.width * 0.005,
          ballSpeedY: canvas.width * 0.007
        } : {
          // Desktop (Landscape) settings
          paddleWidth: 10,
          paddleHeight: 80,
          paddleOffset: 20,
          ballSize: 8,
          ballSpeedX: 5,
          ballSpeedY: 3
        };
  
        let paddle1Pos = isMobile ? 
          { x: canvas.width / 2 - settings.paddleWidth / 2, y: settings.paddleOffset } : 
          { x: settings.paddleOffset, y: canvas.height / 2 - settings.paddleHeight / 2 };
        
        let paddle2Pos = isMobile ? 
          { x: canvas.width / 2 - settings.paddleWidth / 2, y: canvas.height - settings.paddleOffset - settings.paddleHeight } : 
          { x: canvas.width - settings.paddleOffset - settings.paddleWidth, y: canvas.height / 2 - settings.paddleHeight / 2 };
  
        let ballX = canvas.width / 2;
        let ballY = canvas.height / 2;
        let ballSpeedX = settings.ballSpeedX;
        let ballSpeedY = settings.ballSpeedY;
        let paddle1Speed = 0;
        let paddle2Speed = 0;
  
        const touchHandler = (event) => {
          event.preventDefault();
          //touch and click not the same ??
          const touch = event.touches[0];
          const rect = canvas.getBoundingClientRect();
          
          if (isMobile) {
            // Mobile touch controls (top/bottom paddles)
            const touchX = touch.clientX - rect.left;
            if (props.mode === "local") {
              if (touch.clientY < window.innerHeight / 2) {
                paddle1Pos.x = touchX - settings.paddleWidth / 2;
              } else {
                paddle2Pos.x = touchX - settings.paddleWidth / 2;
              }
            } else {
              paddle1Pos.x = touchX - settings.paddleWidth / 2;
            }
          }
        };
  
        const keyDown = (event) => {
          if (!isMobile && props.mode === "local") {
            if (event.key === "w") paddle1Speed = -5;
            if (event.key === "s") paddle1Speed = 5;
            if (event.key === "ArrowUp") paddle2Speed = -5;
            if (event.key === "ArrowDown") paddle2Speed = 5;
          }
        };
  
        const keyUp = (event) => {
          if (!isMobile && props.mode === "local") {
            if (event.key === "w" || event.key === "s") paddle1Speed = 0;
            if (event.key === "ArrowUp" || event.key === "ArrowDown") paddle2Speed = 0;
          }
        };
  
        if (isMobile) {
          canvas.addEventListener("touchmove", touchHandler);
          canvas.addEventListener("touchstart", touchHandler);
        } else {
          window.addEventListener("keydown", keyDown);
          window.addEventListener("keyup", keyUp);
        }
  
        const updateGame = () => {
          ctx.fillStyle = "black";
          ctx.fillRect(0, 0, canvas.width, canvas.height);
  
          // Draw paddles
          ctx.fillStyle = "white";
          if (isMobile) {
            // Draw paddles horizontally for mobile
            ctx.fillRect(paddle1Pos.x, paddle1Pos.y, settings.paddleWidth, settings.paddleHeight);
            ctx.fillRect(paddle2Pos.x, paddle2Pos.y, settings.paddleWidth, settings.paddleHeight);
          } else {
            // Draw paddles vertically for desktop
            ctx.fillRect(paddle1Pos.x, paddle1Pos.y, settings.paddleWidth, settings.paddleHeight);
            ctx.fillRect(paddle2Pos.x, paddle2Pos.y, settings.paddleWidth, settings.paddleHeight);
          }
  
          // Update paddle positions
          if (isMobile) {
            // Keep paddles within horizontal bounds
            paddle1Pos.x = Math.max(0, Math.min(canvas.width - settings.paddleWidth, paddle1Pos.x));
            paddle2Pos.x = Math.max(0, Math.min(canvas.width - settings.paddleWidth, paddle2Pos.x));
          } else {
            // Update vertical paddle positions for desktop
            paddle1Pos.y += paddle1Speed;
            paddle2Pos.y += paddle2Speed;
            // Keep paddles within vertical bounds
            paddle1Pos.y = Math.max(0, Math.min(canvas.height - settings.paddleHeight, paddle1Pos.y));
            paddle2Pos.y = Math.max(0, Math.min(canvas.height - settings.paddleHeight, paddle2Pos.y));
          }
  
          // Ball movement
          ballX += ballSpeedX;
          ballY += ballSpeedY;
  
          // Ball collisions
          if (isMobile) {
            // Mobile collisions (top/bottom paddles)
            if (ballX <= 0 || ballX >= canvas.width) {
              ballSpeedX *= -1;
            }
  
            // Paddle collisions
            if ((ballY <= paddle1Pos.y + settings.paddleHeight && 
                 ballX >= paddle1Pos.x && 
                 ballX <= paddle1Pos.x + settings.paddleWidth) ||
                (ballY >= paddle2Pos.y && 
                 ballX >= paddle2Pos.x && 
                 ballX <= paddle2Pos.x + settings.paddleWidth)) {
              ballSpeedY *= -1;
            }
  
            // Reset ball if out of bounds
            if (ballY <= 0 || ballY >= canvas.height) {
              ballX = canvas.width / 2;
              ballY = canvas.height / 2;
            }
          } else {
            // Desktop collisions (left/right paddles)
            if (ballY <= 0 || ballY >= canvas.height) {
              ballSpeedY *= -1;
            }
  
            // Paddle collisions
            if ((ballX <= paddle1Pos.x + settings.paddleWidth && 
                 ballY >= paddle1Pos.y && 
                 ballY <= paddle1Pos.y + settings.paddleHeight) ||
                (ballX >= paddle2Pos.x && 
                 ballY >= paddle2Pos.y && 
                 ballY <= paddle2Pos.y + settings.paddleHeight)) {
              ballSpeedX *= -1;
            }
  
            // Reset ball if out of bounds
            if (ballX <= 0 || ballX >= canvas.width) {
              ballX = canvas.width / 2;
              ballY = canvas.height / 2;
            }
          }
  
          // Draw ball
          ctx.beginPath();
          ctx.arc(ballX, ballY, settings.ballSize, 0, Math.PI * 2);
          ctx.fill();
  
          // AI for solo mode
          if (props.mode === "solo") {
            if (isMobile) {
              paddle2Pos.x += (ballX - (paddle2Pos.x + settings.paddleWidth / 2)) * 0.05;
            } else {
              paddle2Pos.y += (ballY - (paddle2Pos.y + settings.paddleHeight / 2)) * 0.05;
            }
          }
  
          animationFrameId = requestAnimationFrame(updateGame);
        };
  
        updateGame();
      };
  
      onMounted(() => {
        handleResize();
        window.addEventListener("resize", handleResize);
      });
  
      onBeforeUnmount(() => {
        window.removeEventListener("resize", handleResize);
        if (animationFrameId) {
          cancelAnimationFrame(animationFrameId);
        }
      });
  
      return { pongCanvas };
    },
  };
  </script>
  
  <style scoped>
  .pong-game {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100%;
    margin-top: 20px;
  }
  
  canvas {
    background: black;
    border: 2px solid white;
    max-width: 100%;
    max-height: 100%;
  }
  
  @media screen and (max-width: 768px) {
    .pong-game {
      margin-top: 0;
    }
    
    canvas {
      border: 1px solid white;
    }
  }
  </style>