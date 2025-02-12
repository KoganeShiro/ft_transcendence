<template>
  <div id="pongField">
    <canvas
      ref="pongCanvas"
      class="canvas"
      :width="canvasWidth"
      :height="canvasHeight"
    ></canvas>
  </div>
</template>

<script>
export default {
  data() {
    return {
      // Flag to switch between desktop and mobile modes.
      isMobile: false,
      isTablette: false,
      // Adjusted canvas dimensions: default for desktop; will be changed for mobile.
      canvasWidth: 900,
      canvasHeight: 500,
      // Core game state (used for ball and score)
      gameState: {
        ball_x: 0.5,
        ball_y: 0.5,
        // For desktop, we use horizontal velocity; for mobile we swap roles.
        ball_velocity_x: 0.01,
        ball_velocity_y: 0.01,
        // Desktop paddles (vertical movement)
        player1_y: 0.5,
        player2_y: 0.5,
        score1: 0,
        score2: 0,
      },
      // New state for mobile: the player paddle’s horizontal position.
      player1_x: 0.5,
      ballSpeedFactor: 30,
      initialBallSpeed: 30,
      maxBallSpeed: 100,
      // Desktop key flags remain for non‑mobile mode.
      keysPressed: {
        up_left: false,
        down_left: false,
        up_right: false,
        down_right: false,
      },
      gameLoop: null,
    };
  },
  mounted() {
    if (window.innerWidth < 480) {
      // Mobile phone: very small width
      this.isMobile = true;
      if (window.innerHeight < 767) {
        // console.log("Very small phone detected.");
        this.canvasWidth = 300;
        this.canvasHeight = 430;
      }
      else {
        this.canvasWidth = 300;
        this.canvasHeight = 550;
      }
      // console.log("window.innerHeight =", window.innerHeight);
      // console.log("Mobile mode: canvasWidth =", this.canvasWidth, "canvasHeight =", this.canvasHeight);
      // // Remove keyboard listeners (not needed for touch)
      window.removeEventListener("keydown", this.handleKeyDown);
      window.removeEventListener("keyup", this.handleKeyUp);
      // Add touch event listener to the canvas
      this.$refs.pongCanvas.addEventListener(
        "touchmove",
        this.handleTouchMove,
        { passive: false }
      );
      // console.log("Touch listener added for mobile.");
    } else if (window.innerWidth < 811) {
      // Tablet (portrait mode but not a very small phone)
      this.isTablette = true;
      this.canvasWidth = 500; // adjust as needed for tablets
      this.canvasHeight = 850;
      // console.log("Tablette mode: canvasWidth =", this.canvasWidth, "canvasHeight =", this.canvasHeight);
      window.removeEventListener("keydown", this.handleKeyDown);
      window.removeEventListener("keyup", this.handleKeyUp);
      this.$refs.pongCanvas.addEventListener(
        "touchmove",
        this.handleTouchMove,
        { passive: false }
      );
      // console.log("Touch listener added for tablette.");
    } else {
      // Desktop mode
      window.addEventListener("keydown", this.handleKeyDown);
      window.addEventListener("keyup", this.handleKeyUp);
      // console.log("Keyboard listeners added for desktop.");
    }
    //this.startGameLoop();
  },

  methods: {
    // Existing keyboard events for desktop remain unchanged.
    handleKeyDown(event) {
      // console.log("Key down:", event.key);
      if (event.key === "ArrowUp");
      if (event.key === "ArrowDown");
      if (event.key === "w" || event.key === "W") this.keysPressed.up_left = true;
      if (event.key === "s" || event.key === "S") this.keysPressed.down_left = true;
    },
    handleKeyUp(event) {
      // console.log("Key up:", event.key);
      if (event.key === "ArrowUp");
      if (event.key === "ArrowDown");
      if (event.key === "w" || event.key === "W") this.keysPressed.up_left = false;
      if (event.key === "s" || event.key === "S") this.keysPressed.down_left = false;
    },
    // Touch event handler for mobile: update player1_x based on touch position.
    handleTouchMove(event) {
      event.preventDefault();
      const touch = event.touches[0];
      const rect = this.$refs.pongCanvas.getBoundingClientRect();
      // Calculate normalized horizontal position (0 to 1)
      const touchX = (touch.clientX - rect.left) / rect.width;
      this.player1_x = touchX;
      // console.log("Touch move: player1_x =", this.player1_x);
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
      // console.log("Game loop started.");
    },
    updateGame(deltaTime) {
      if (!this.isMobile && !this.isTablette) {
        // Desktop: update vertical paddle positions using keys
        const paddleSpeed = 0.01;
        if (this.keysPressed.up_left)
          this.gameState.player1_y = Math.max(this.gameState.player1_y - paddleSpeed, 0);
        if (this.keysPressed.down_left)
          this.gameState.player1_y = Math.min(this.gameState.player1_y + paddleSpeed, 1);
        if (this.keysPressed.up_right)
          this.gameState.player2_y = Math.max(this.gameState.player2_y - paddleSpeed, 0);
        if (this.keysPressed.down_right)
          this.gameState.player2_y = Math.min(this.gameState.player2_y + paddleSpeed, 1);
      }
      // Update ball position (applies to both modes)
      this.gameState.ball_x += this.gameState.ball_velocity_x * deltaTime * this.ballSpeedFactor;
      this.gameState.ball_y += this.gameState.ball_velocity_y * deltaTime * this.ballSpeedFactor;

      if (!this.isMobile && !this.isTablette) {
        // Desktop: bounce ball off top and bottom
        if (this.gameState.ball_y <= 0 || this.gameState.ball_y >= 1) {
          this.gameState.ball_velocity_y *= -1;
        }
      } else {
        // Mobile: bounce ball off left/right sides
        if (this.gameState.ball_x <= 0 || this.gameState.ball_x >= 1) {
          this.gameState.ball_velocity_x *= -1;
        }
      }
      this.checkPaddleCollision();
      this.checkScore();
    },
    checkPaddleCollision() {
      if (!this.isMobile && !this.isTablette) {
        // Desktop collision: paddles on the left and right.
        if (
          this.gameState.ball_x <= 0.05 &&
          this.gameState.player1_y - 0.1 <= this.gameState.ball_y &&
          this.gameState.ball_y <= this.gameState.player1_y + 0.1
        ) {
          this.gameState.ball_velocity_x *= -1;
          this.gameState.ball_velocity_y = (this.gameState.ball_y - this.gameState.player1_y) * 0.1;
          this.ballSpeedFactor = Math.min(this.maxBallSpeed, this.ballSpeedFactor + 5);
          // console.log("Desktop collision: Player 1 hit.");
        }
        if (
          this.gameState.ball_x >= 0.95 &&
          this.gameState.player2_y - 0.1 <= this.gameState.ball_y &&
          this.gameState.ball_y <= this.gameState.player2_y + 0.1
        ) {
          this.gameState.ball_velocity_x *= -1;
          this.gameState.ball_velocity_y = (this.gameState.ball_y - this.gameState.player2_y) * 0.1;
          this.ballSpeedFactor = Math.min(this.maxBallSpeed, this.ballSpeedFactor + 5);
          // console.log("Desktop collision: Player 2 hit.");
        }
      } else {
        // Mobile collision:
        // Assume player's paddle is at the bottom and moves horizontally (using player1_x)
        const paddleHalfWidth = 0.1; // normalized half-width (for a paddle covering 20% of the canvas)
        // Player paddle collision (bottom of the screen)
        if (
          this.gameState.ball_y >= 0.95 &&
          this.gameState.ball_x >= this.player1_x - paddleHalfWidth &&
          this.gameState.ball_x <= this.player1_x + paddleHalfWidth
        ) {
          // Bounce the ball upward
          this.gameState.ball_velocity_y *= -1;
          // Optionally adjust horizontal velocity based on hit position
          this.gameState.ball_velocity_x = (this.gameState.ball_x - this.player1_x) * 0.1;
          this.ballSpeedFactor = Math.min(this.maxBallSpeed, this.ballSpeedFactor + 5);
          // console.log("Mobile collision: Player paddle hit.");
        }
        // Simple opponent paddle at the top (centered horizontally)
        const opponentPaddleX = 0.5;
        if (
          this.gameState.ball_y <= 0.05 &&
          this.gameState.ball_x >= opponentPaddleX - paddleHalfWidth &&
          this.gameState.ball_x <= opponentPaddleX + paddleHalfWidth
        ) {
          // Bounce the ball downward
          this.gameState.ball_velocity_y *= -1;
          this.gameState.ball_velocity_x = (this.gameState.ball_x - opponentPaddleX) * 0.1;
          this.ballSpeedFactor = Math.min(this.maxBallSpeed, this.ballSpeedFactor + 5);
          // console.log("Mobile collision: Opponent paddle hit.");
        }
      }
    },
    checkScore() {
      // Desktop scoring: when ball goes off left or right edges.
      if (!this.isMobile && !this.isTablette) {
        if (this.gameState.ball_x <= 0) {
          this.gameState.score2++;
          this.resetBall(1);
        }
        if (this.gameState.ball_x >= 1) {
          this.gameState.score1++;
          this.resetBall(-1);
        }
      } else {
        // Mobile scoring: when ball goes off the top or bottom.
        if (this.gameState.ball_y >= 1) {
          this.gameState.score2++;
          this.resetBall(-1);
        }
        if (this.gameState.ball_y <= 0) {
          this.gameState.score1++;
          this.resetBall(1);
        }
      }
      
      if (this.gameState.score1 >= 5 || this.gameState.score2 >= 5) {
        this.resetBall(1); 
        this.endGame();
      }
    },

    resetBall(direction) {
      // Reset ball position
      this.gameState.ball_x = 0.5;
      this.gameState.ball_y = 0.5;
      if (!this.isMobile && !this.isTablette) {
        this.gameState.player1_y = 0.5;
        this.gameState.player2_y = 0.5;
      } else {
        // For mobile, reset the player paddle to the center horizontally.
        this.player1_x = 0.5;
      }
      // For desktop, set horizontal ball velocity; for mobile, vertical.
      if (!this.isMobile && !this.isTablette) {
        this.gameState.ball_velocity_x = 0.01 * direction;
        this.gameState.ball_velocity_y = 0;
      } else {
        this.gameState.ball_velocity_y = 0.01 * direction;
        this.gameState.ball_velocity_x = 0;
      }
      this.ballSpeedFactor = this.initialBallSpeed;
      // console.log("Ball reset. Direction:", direction);
    },
    updateCanvas() {
      const canvas = this.$refs.pongCanvas;
      const ctx = canvas.getContext("2d");
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.fillStyle = "white";

      // Draw the ball
      ctx.beginPath();
      ctx.arc(
        this.gameState.ball_x * canvas.width,
        this.gameState.ball_y * canvas.height,
        7,
        0,
        Math.PI * 2
      );
      ctx.fill();

      if (!this.isMobile && !this.isTablette) {
        // Desktop: draw vertical paddles on left and right
        ctx.fillRect(20, this.gameState.player1_y * canvas.height - 30, 10, 60);
        ctx.fillRect(canvas.width - 30, this.gameState.player2_y * canvas.height - 30, 10, 60);
        // Draw scores
        ctx.font = "30px Arial";
        ctx.fillText(this.gameState.score1, canvas.width / 4, 30);
        ctx.fillText(this.gameState.score2, (3 * canvas.width) / 4, 30);
      } else {
        // Mobile: draw horizontal paddles
        const paddleWidth = canvas.width * 0.2;
        const paddleHeight = 10;
        // Player's paddle at bottom
        const player1X = this.player1_x * canvas.width - paddleWidth / 2;
        const player1Y = canvas.height - 30;
        ctx.fillRect(player1X, player1Y, paddleWidth, paddleHeight);
        // Opponent paddle at top (centered)
        const opponentX = canvas.width * 0.5 - paddleWidth / 2;
        const opponentY = 20;
        ctx.fillRect(opponentX, opponentY, paddleWidth, paddleHeight);
        // Draw scores
        ctx.font = "30px Arial";
        ctx.fillText(this.gameState.score1, canvas.width / 4, canvas.height - 30);
        ctx.fillText(this.gameState.score2, canvas.width / 4, 50);
      }
    },
    endGame() {
      let winner = "";
      if (!this.isMobile && !this.isTablette) {
        winner = this.gameState.score1 > this.gameState.score2 ? "Player 1" : "Player 2";
      } else {
        winner = this.gameState.score1 > this.gameState.score2 ? "Player" : "Opponent";
      }
      // console.log("Game ended. Winner:", winner);
      this.$emit("gameEnded", winner);
    },
  },
  beforeUnmount() {
    if (!this.isMobile && !this.isTablette) {
      window.removeEventListener("keydown", this.handleKeyDown);
      window.removeEventListener("keyup", this.handleKeyUp);
    } else {
      this.$refs.pongCanvas.removeEventListener("touchmove", this.handleTouchMove);
    }
    cancelAnimationFrame(this.gameLoop);
    // console.log("Game loop stopped, listeners removed.");
  },
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
