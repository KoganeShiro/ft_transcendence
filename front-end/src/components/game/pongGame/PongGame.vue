<template>
  <div id="pongField">
    <canvas ref="pongCanvas" class="canvas" width="900" height="500"></canvas>
  </div>
</template>

<script>
export default {
  data() {
    return {
      gameState: {
        ball_x: 0.5,
        ball_y: 0.5,
        ball_velocity_x: 0.01,
        ball_velocity_y: 0,
        player1_y: 0.5,
        player2_y: 0.5,
        score1: 0,
        score2: 0,
      },
      ballSpeedFactor: 30,
      initialBallSpeed: 30,
      maxBallSpeed: 100,
      keysPressed: {
        up_left: false,
        down_left: false,
        up_right: false,
        down_right: false
      },
      gameLoop: null,
    };
  },
  mounted() {
    window.addEventListener('keydown', this.handleKeyDown);
    window.addEventListener('keyup', this.handleKeyUp);
    this.startGameLoop();
    
    // Set a timeout to end the game after a certain period
    setTimeout(() => {
      this.endGame();
    }, 15000); // Adjust the duration of the game as needed
  },
  methods: {
    handleKeyDown(event) {
      if (event.key === 'ArrowUp') this.keysPressed.up_right = true;
      if (event.key === 'ArrowDown') this.keysPressed.down_right = true;
      if (event.key === 'w' || event.key === 'W') this.keysPressed.up_left = true;
      if (event.key === 's' || event.key === 'S') this.keysPressed.down_left = true;
    },
    handleKeyUp(event) {
      if (event.key === 'ArrowUp') this.keysPressed.up_right = false;
      if (event.key === 'ArrowDown') this.keysPressed.down_right = false;
      if (event.key === 'w' || event.key === 'W') this.keysPressed.up_left = false;
      if (event.key === 's' || event.key === 'S') this.keysPressed.down_left = false;
    },
    startGameLoop() {
      let previousTime = performance.now();
      const loop = (currentTime) => {
        const deltaTime = (currentTime - previousTime) / 1000;
        previousTime = currentTime;
        this.updateGame(deltaTime);
        this.updateCanvas();
        this.gameLoop = requestAnimationFrame(loop);
      };
      this.gameLoop = requestAnimationFrame(loop);
    },
    updateGame(deltaTime) {
      const paddleSpeed = 0.01;
      if (this.keysPressed.up_left) this.gameState.player1_y = Math.max(this.gameState.player1_y - paddleSpeed, 0);
      if (this.keysPressed.down_left) this.gameState.player1_y = Math.min(this.gameState.player1_y + paddleSpeed, 1);
      if (this.keysPressed.up_right) this.gameState.player2_y = Math.max(this.gameState.player2_y - paddleSpeed, 0);
      if (this.keysPressed.down_right) this.gameState.player2_y = Math.min(this.gameState.player2_y + paddleSpeed, 1);

      this.gameState.ball_x += this.gameState.ball_velocity_x * deltaTime * this.ballSpeedFactor;
      this.gameState.ball_y += this.gameState.ball_velocity_y * deltaTime * this.ballSpeedFactor;

      if (this.gameState.ball_y <= 0 || this.gameState.ball_y >= 1) {
        this.gameState.ball_velocity_y *= -1;
      }

      this.checkPaddleCollision();
      this.checkScore();
    },
    checkPaddleCollision() {
      if (this.gameState.ball_x <= 0.05 &&
          this.gameState.player1_y - 0.1 <= this.gameState.ball_y && this.gameState.ball_y <= this.gameState.player1_y + 0.1) {
        this.gameState.ball_velocity_x *= -1;
        this.gameState.ball_velocity_y = (this.gameState.ball_y - this.gameState.player1_y) * 0.1;
        this.ballSpeedFactor = Math.min(this.maxBallSpeed, this.ballSpeedFactor + 5);
      }
      if (this.gameState.ball_x >= 0.95 &&
          this.gameState.player2_y - 0.1 <= this.gameState.ball_y && this.gameState.ball_y <= this.gameState.player2_y + 0.1) {
        this.gameState.ball_velocity_x *= -1;
        this.gameState.ball_velocity_y = (this.gameState.ball_y - this.gameState.player2_y) * 0.1;
        this.ballSpeedFactor = Math.min(this.maxBallSpeed, this.ballSpeedFactor + 5);
      }
    },
    checkScore() {
      if (this.gameState.ball_x <= 0) {
        this.gameState.score2++;
        this.resetBall(1);
      }
      if (this.gameState.ball_x >= 1) {
        this.gameState.score1++;
        this.resetBall(-1);
      }
    },
    resetBall(direction) {
      this.gameState.ball_x = 0.5;
      this.gameState.ball_y = 0.5;
      this.gameState.player1_y = 0.5;
      this.gameState.player2_y = 0.5;
      this.gameState.ball_velocity_x = 0.01 * direction;
      this.gameState.ball_velocity_y = 0;
      this.ballSpeedFactor = this.initialBallSpeed;
    },
    updateCanvas() {
      const canvas = this.$refs.pongCanvas;
      const ctx = canvas.getContext('2d');
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.fillStyle = 'white';
      
      ctx.beginPath();
      ctx.arc(this.gameState.ball_x * canvas.width, this.gameState.ball_y * canvas.height, 7, 0, Math.PI * 2);
      ctx.fill();
      
      ctx.fillRect(20, this.gameState.player1_y * canvas.height - 30, 10, 60);
      ctx.fillRect(canvas.width - 30, this.gameState.player2_y * canvas.height - 30, 10, 60);
      
      ctx.font = '30px Arial';
      ctx.fillText(this.gameState.score1, canvas.width / 4, 30);
      ctx.fillText(this.gameState.score2, 3 * canvas.width / 4, 30);
    },
    endGame() {
      const winner = this.gameState.score1 > this.gameState.score2 ? "Player 1" : "Player 2";
      this.$emit("gameEnded", winner);
    }
  },
  beforeUnmount() {
    window.removeEventListener('keydown', this.handleKeyDown);
    window.removeEventListener('keyup', this.handleKeyUp);
    cancelAnimationFrame(this.gameLoop);
  }
};
</script>

<style>
#pongField {
  display: flex;
  justify-content: center;
  align-items: center;
}
 .canvas {
  border: 2px solid var(--background-color);
  border-radius: 8px;
}
</style>