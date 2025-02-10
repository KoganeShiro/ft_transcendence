// import { ref } from 'vue';

// export default function usePongGame(pongCanvas) {
//   const gameState = ref({
//     ball_x: 0.5,
//     ball_y: 0.5,
//     ball_velocity_x: 0.01,
//     ball_velocity_y: 0,
//     player1_y: 0.5,
//     player2_y: 0.5,
//     score1: 0,
//     score2: 0,
//     gameLoop: null,
//   });

//   const ballSpeedFactor = ref(30);
//   const initialBallSpeed = 30;
//   const maxBallSpeed = 100;

//   const keysPressed = ref({
//     up_left: false,
//     down_left: false,
//     up_right: false,
//     down_right: false
//   });

//   const handleKeyDown = (event) => {
//     if (event.key === 'ArrowUp') keysPressed.value.up_right = true;
//     if (event.key === 'ArrowDown') keysPressed.value.down_right = true;
//     if (event.key === 'w' || event.key === 'W') keysPressed.value.up_left = true;
//     if (event.key === 's' || event.key === 'S') keysPressed.value.down_left = true;
//   };

//   const handleKeyUp = (event) => {
//     if (event.key === 'ArrowUp') keysPressed.value.up_right = false;
//     if (event.key === 'ArrowDown') keysPressed.value.down_right = false;
//     if (event.key === 'w' || event.key === 'W') keysPressed.value.up_left = false;
//     if (event.key === 's' || event.key === 'S') keysPressed.value.down_left = false;
//   };

//   const startGameLoop = () => {
//     let previousTime = performance.now();
//     const loop = (currentTime) => {
//       const deltaTime = (currentTime - previousTime) / 1000;
//       previousTime = currentTime;
//       updateGame(deltaTime);
//       updateCanvas();
//       gameState.value.gameLoop = requestAnimationFrame(loop);
//     };
//     gameState.value.gameLoop = requestAnimationFrame(loop);
//   };

//   const updateGame = (deltaTime) => {
//     const paddleSpeed = 0.01;
//     if (keysPressed.value.up_left) gameState.value.player1_y = Math.max(gameState.value.player1_y - paddleSpeed, 0);
//     if (keysPressed.value.down_left) gameState.value.player1_y = Math.min(gameState.value.player1_y + paddleSpeed, 1);
//     if (keysPressed.value.up_right) gameState.value.player2_y = Math.max(gameState.value.player2_y - paddleSpeed, 0);
//     if (keysPressed.value.down_right) gameState.value.player2_y = Math.min(gameState.value.player2_y + paddleSpeed, 1);

//     gameState.value.ball_x += gameState.value.ball_velocity_x * deltaTime * ballSpeedFactor.value;
//     gameState.value.ball_y += gameState.value.ball_velocity_y * deltaTime * ballSpeedFactor.value;

//     if (gameState.value.ball_y <= 0 || gameState.value.ball_y >= 1) {
//       gameState.value.ball_velocity_y *= -1;
//     }

//     checkPaddleCollision();
//     checkScore();
//   };

//   const checkPaddleCollision = () => {
//     if (gameState.value.ball_x <= 0.05 &&
//         gameState.value.player1_y - 0.1 <= gameState.value.ball_y && gameState.value.ball_y <= gameState.value.player1_y + 0.1) {
//       gameState.value.ball_velocity_x *= -1;
//       gameState.value.ball_velocity_y = (gameState.value.ball_y - gameState.value.player1_y) * 0.1;
//       ballSpeedFactor.value = Math.min(maxBallSpeed, ballSpeedFactor.value + 5);
//     }
//     if (gameState.value.ball_x >= 0.95 &&
//         gameState.value.player2_y - 0.1 <= gameState.value.ball_y && gameState.value.ball_y <= gameState.value.player2_y + 0.1) {
//       gameState.value.ball_velocity_x *= -1;
//       gameState.value.ball_velocity_y = (gameState.value.ball_y - gameState.value.player2_y) * 0.1;
//       ballSpeedFactor.value = Math.min(maxBallSpeed, ballSpeedFactor.value + 5);
//     }
//   };

//   const checkScore = () => {
//     if (gameState.value.ball_x <= 0) {
//       gameState.value.score2++;
//       resetBall(1);
//     }
//     if (gameState.value.ball_x >= 1) {
//       gameState.value.score1++;
//       resetBall(-1);
//     }
//   };

//   const resetBall = (direction) => {
//     gameState.value.ball_x = 0.5;
//     gameState.value.ball_y = 0.5;
//     gameState.value.player1_y = 0.5;
//     gameState.value.player2_y = 0.5;
//     gameState.value.ball_velocity_x = 0.01 * direction;
//     gameState.value.ball_velocity_y = 0;
//     ballSpeedFactor.value = initialBallSpeed;
//   };

//   const updateCanvas = () => {
//     const canvas = pongCanvas.value;
//     const ctx = canvas.getContext('2d');
//     ctx.clearRect(0, 0, canvas.width, canvas.height);
//     ctx.fillStyle = 'white';

//     ctx.beginPath();
//     ctx.arc(gameState.value.ball_x * canvas.width, gameState.value.ball_y * canvas.height, 7, 0, Math.PI * 2);
//     ctx.fill();

//     ctx.fillRect(20, gameState.value.player1_y * canvas.height - 30, 10, 60);
//     ctx.fillRect(canvas.width - 30, gameState.value.player2_y * canvas.height - 30, 10, 60);

//     ctx.font = '30px Arial';
//     ctx.fillText(gameState.value.score1, canvas.width / 4, 30);
//     ctx.fillText(gameState.value.score2, 3 * canvas.width / 4, 30);
//   };

//   return {
//     gameState,
//     keysPressed,
//     startGameLoop,
//     handleKeyDown,
//     handleKeyUp,
//     updateCanvas,
//   };
// }
import { ref } from 'vue';

export default function usePongGame(pongCanvas) {
  const gameState = ref({
    ball_x: 0.5,
    ball_y: 0.5,
    ball_velocity_x: 0.01,
    ball_velocity_y: 0,
    player1_y: 0.5,
    player2_y: 0.5,
    score1: 0,
    score2: 0,
    gameLoop: null,
  });

  const ballSpeedFactor = ref(30);
  const initialBallSpeed = 30;
  const maxBallSpeed = 100;

  const keysPressed = ref({
    up_left: false,
    down_left: false,
    up_right: false,
    down_right: false
  });

  const handleKeyDown = (event) => {
    if (event.key === 'ArrowUp') keysPressed.value.up_right = true;
    if (event.key === 'ArrowDown') keysPressed.value.down_right = true;
    if (event.key === 'w' || event.key === 'W') keysPressed.value.up_left = true;
    if (event.key === 's' || event.key === 'S') keysPressed.value.down_left = true;
  };

  const handleKeyUp = (event) => {
    if (event.key === 'ArrowUp') keysPressed.value.up_right = false;
    if (event.key === 'ArrowDown') keysPressed.value.down_right = false;
    if (event.key === 'w' || event.key === 'W') keysPressed.value.up_left = false;
    if (event.key === 's' || event.key === 'S') keysPressed.value.down_left = false;
  };

  const handleTouchStart = (event) => {
    const touch = event.touches[0];
    const canvas = pongCanvas.value;
    const rect = canvas.getBoundingClientRect();
    const y = (touch.clientY - rect.top) / canvas.height;

    if (touch.clientX < rect.width / 2) { // Left side
      if (y < gameState.value.player1_y) {
        keysPressed.value.up_left = true;
      } else {
        keysPressed.value.down_left = true;
      }
    } else { // Right side
      if (y < gameState.value.player2_y) {
        keysPressed.value.up_right = true;
      } else {
        keysPressed.value.down_right = true;
      }
    }
  };

  const handleTouchEnd = () => {
    keysPressed.value.up_left = false;
    keysPressed.value.down_left = false;
    keysPressed.value.up_right = false;
    keysPressed.value.down_right = false;
  };

  const startGameLoop = () => {
    let previousTime = performance.now();
    const loop = (currentTime) => {
      const deltaTime = (currentTime - previousTime) / 1000;
      previousTime = currentTime;
      updateGame(deltaTime);
      updateCanvas();
      gameState.value.gameLoop = requestAnimationFrame(loop);
    };
    gameState.value.gameLoop = requestAnimationFrame(loop);
  };

  const updateGame = (deltaTime) => {
    const paddleSpeed = 0.01;
    if (keysPressed.value.up_left) gameState.value.player1_y = Math.max(gameState.value.player1_y - paddleSpeed, 0);
    if (keysPressed.value.down_left) gameState.value.player1_y = Math.min(gameState.value.player1_y + paddleSpeed, 1);
    if (keysPressed.value.up_right) gameState.value.player2_y = Math.max(gameState.value.player2_y - paddleSpeed, 0);
    if (keysPressed.value.down_right) gameState.value.player2_y = Math.min(gameState.value.player2_y + paddleSpeed, 1);

    gameState.value.ball_x += gameState.value.ball_velocity_x * deltaTime * ballSpeedFactor.value;
    gameState.value.ball_y += gameState.value.ball_velocity_y * deltaTime * ballSpeedFactor.value;

    if (gameState.value.ball_y <= 0 || gameState.value.ball_y >= 1) {
      gameState.value.ball_velocity_y *= -1;
    }

    checkPaddleCollision();
    checkScore();
  };

  const checkPaddleCollision = () => {
    if (gameState.value.ball_x <= 0.05 &&
        gameState.value.player1_y - 0.1 <= gameState.value.ball_y && gameState.value.ball_y <= gameState.value.player1_y + 0.1) {
      gameState.value.ball_velocity_x *= -1;
      gameState.value.ball_velocity_y = (gameState.value.ball_y - gameState.value.player1_y) * 0.1;
      ballSpeedFactor.value = Math.min(maxBallSpeed, ballSpeedFactor.value + 5);
    }
    if (gameState.value.ball_x >= 0.95 &&
        gameState.value.player2_y - 0.1 <= gameState.value.ball_y && gameState.value.ball_y <= gameState.value.player2_y + 0.1) {
      gameState.value.ball_velocity_x *= -1;
      gameState.value.ball_velocity_y = (gameState.value.ball_y - gameState.value.player2_y) * 0.1;
      ballSpeedFactor.value = Math.min(maxBallSpeed, ballSpeedFactor.value + 5);
    }
  };

  const checkScore = () => {
    if (gameState.value.ball_x <= 0) {
      gameState.value.score2++;
      resetBall(1);
    }
    if (gameState.value.ball_x >= 1) {
      gameState.value.score1++;
      resetBall(-1);
    }
  };

  const resetBall = (direction) => {
    gameState.value.ball_x = 0.5;
    gameState.value.ball_y = 0.5;
    gameState.value.player1_y = 0.5;
    gameState.value.player2_y = 0.5;
    gameState.value.ball_velocity_x = 0.01 * direction;
    gameState.value.ball_velocity_y = 0;
    ballSpeedFactor.value = initialBallSpeed;
  };

  const updateCanvas = () => {
    const canvas = pongCanvas.value;
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = 'white';

    ctx.beginPath();
    ctx.arc(gameState.value.ball_x * canvas.width, gameState.value.ball_y * canvas.height, 7, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillRect(20, gameState.value.player1_y * canvas.height - 30, 10, 60);
    ctx.fillRect(canvas.width - 30, gameState.value.player2_y * canvas.height - 30, 10, 60);

    ctx.font = '30px Arial';
    ctx.fillText(gameState.value.score1, canvas.width / 4, 30);
    ctx.fillText(gameState.value.score2, 3 * canvas.width / 4, 30);
  };

  return {
    gameState,
    keysPressed,
    startGameLoop,
    handleKeyDown,
    handleKeyUp,
    handleTouchStart,
    handleTouchEnd,
    updateCanvas,
  };
}