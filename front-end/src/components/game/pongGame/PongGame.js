export class PongGame {
  constructor(pongCanvas) {
    this.pongCanvas = pongCanvas;
    this.gameState = {
      ball_x: 0.5,
      ball_y: 0.5,
      ball_velocity_x: 0.01,
      ball_velocity_y: 0,
      player1_x: 0.5,
      score1: 0,
      gameLoop: null,
    };
    this.ballSpeedFactor = 30;
    this.initialBallSpeed = 30;
    this.maxBallSpeed = 100;
    this.keysPressed = {
      left: false,
      right: false,
    };
  }

  handleKeyDown = (event) => {
    if (event.key === 'ArrowLeft') this.keysPressed.left = true;
    if (event.key === 'ArrowRight') this.keysPressed.right = true;
  };

  handleKeyUp = (event) => {
    if (event.key === 'ArrowLeft') this.keysPressed.left = false;
    if (event.key === 'ArrowRight') this.keysPressed.right = false;
  };

  handleTouchStart = (event) => {
    const touch = event.touches[0];
    const rect = this.pongCanvas.getBoundingClientRect();
    const x = (touch.clientX - rect.left) / this.pongCanvas.width;

    if (x < this.gameState.player1_x) {
      this.keysPressed.left = true;
    } else {
      this.keysPressed.right = true;
    }
  };

  handleTouchEnd = () => {
    this.keysPressed.left = false;
    this.keysPressed.right = false;
  };

  startGameLoop = () => {
    let previousTime = performance.now();
    const loop = (currentTime) => {
      const deltaTime = (currentTime - previousTime) / 1000;
      previousTime = currentTime;
      this.updateGame(deltaTime);
      this.updateCanvas();
      this.gameState.gameLoop = requestAnimationFrame(loop);
    };
    this.gameState.gameLoop = requestAnimationFrame(loop);
  };

  updateGame = (deltaTime) => {
    const paddleSpeed = 0.01;
    if (this.keysPressed.left) this.gameState.player1_x = Math.max(this.gameState.player1_x - paddleSpeed, 0);
    if (this.keysPressed.right) this.gameState.player1_x = Math.min(this.gameState.player1_x + paddleSpeed, 1);

    this.gameState.ball_x += this.gameState.ball_velocity_x * deltaTime * this.ballSpeedFactor;
    this.gameState.ball_y += this.gameState.ball_velocity_y * deltaTime * this.ballSpeedFactor;

    if (this.gameState.ball_y <= 0 || this.gameState.ball_y >= 1) {
      this.gameState.ball_velocity_y *= -1;
    }

    this.checkPaddleCollision();
    this.checkScore();
  };

  checkPaddleCollision = () => {
    if (this.gameState.ball_y >= 0.95 &&
        this.gameState.player1_x - 0.1 <= this.gameState.ball_x && this.gameState.ball_x <= this.gameState.player1_x + 0.1) {
      this.gameState.ball_velocity_y *= -1;
      this.gameState.ball_velocity_x = (this.gameState.ball_x - this.gameState.player1_x) * 0.1;
      this.ballSpeedFactor = Math.min(this.maxBallSpeed, this.ballSpeedFactor + 5);
    }
  };

  checkScore = () => {
    if (this.gameState.ball_y >= 1) {
      this.gameState.score1++;
      this.resetBall();
    }
  };

  resetBall = () => {
    this.gameState.ball_x = 0.5;
    this.gameState.ball_y = 0.5;
    this.gameState.player1_x = 0.5;
    this.gameState.ball_velocity_x = 0.01;
    this.gameState.ball_velocity_y = 0;
    this.ballSpeedFactor = this.initialBallSpeed;
  };

  updateCanvas = () => {
    const ctx = this.pongCanvas.getContext('2d');
    ctx.clearRect(0, 0, this.pongCanvas.width, this.pongCanvas.height);
    ctx.fillStyle = 'white';

    ctx.beginPath();
    ctx.arc(this.gameState.ball_x * this.pongCanvas.width, this.gameState.ball_y * this.pongCanvas.height, 7, 0, Math.PI * 2);
    ctx.fill();

    ctx.fillRect(this.gameState.player1_x * this.pongCanvas.width - 30, this.pongCanvas.height - 20, 60, 10);

    ctx.font = '30px Arial';
    ctx.fillText(this.gameState.score1, this.pongCanvas.width / 2, 30);
  };
}