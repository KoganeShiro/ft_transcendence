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
      canvasWidth: 896,
      canvasHeight: 496,
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
      ballSpeedFactor: 20,
      initialBallSpeed: 20,
      maxBallSpeed: 70,
      // Desktop key flags remain for non‑mobile mode.
      keysPressed: {
        up_left: false,
        down_left: false,
        up_right: false,
        down_right: false,
      },
      paddleWidth: 10,
      paddleHeight: 60,
      paddleHalfWidthMobile: 30,
      paddleHeightMobile: 10,
      ballRadius: 7,
      ballDirection: { x: 0.01, y: 0 },
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
      // Remove keyboard listeners (not needed for touch)
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
      window.removeEventListener("keydown", this.handleKeyDown);
      window.removeEventListener("keyup", this.handleKeyUp);
      this.$refs.pongCanvas.addEventListener(
        "touchmove",
        this.handleTouchMove,
        { passive: false }
      );
    } else {
      // Desktop mode
      window.addEventListener("keydown", this.handleKeyDown);
      window.addEventListener("keyup", this.handleKeyUp);
    }
    this.startGameLoop();
  },

  methods: {
    // Existing keyboard events for desktop remain unchanged.
    handleKeyDown(event) {
      // console.log("Key down:", event.key);
      if (event.key === "ArrowUp") this.keysPressed.up_right = true;
      if (event.key === "ArrowDown") this.keysPressed.down_right = true;
      if (event.key === "w" || event.key === "W") this.keysPressed.up_left = true;
      if (event.key === "s" || event.key === "S") this.keysPressed.down_left = true;
    },
    handleKeyUp(event) {
      // console.log("Key up:", event.key);
      if (event.key === "ArrowUp") this.keysPressed.up_right = false;
      if (event.key === "ArrowDown") this.keysPressed.down_right = false;
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
        const paddleSpeed = 0.005;
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
          this.gameState.ball_velocity_x += 5;
        }
      }
      this.checkPaddleCollision();
      this.checkScore();
    },
    checkPaddleCollision() {
      const ballRadius = 7; // Rayon de la balle
      const ballRect = {
        x: this.gameState.ball_x * this.canvasWidth - ballRadius,
        y: this.gameState.ball_y * this.canvasHeight - ballRadius,
        width: ballRadius * 2,
        height: ballRadius * 2,
      };

      if (!this.isMobile && !this.isTablette) {
        // Desktop Collision
        const paddle1Rect = {
          x: 20,
          y: this.gameState.player1_y * this.canvasHeight - this.paddleHeight / 2,
          width: this.paddleWidth,
          height: this.paddleHeight,
        };

        const paddle2Rect = {
          x: this.canvasWidth - 30,
          y: this.gameState.player2_y * this.canvasHeight - this.paddleHeight / 2,
          width: this.paddleWidth,
          height: this.paddleHeight,
        };

        if (this.detectCollision(ballRect, paddle1Rect) && this.gameState.ball_velocity_x < 0) {
          this.handleBallCollision(ballRect, paddle1Rect);
        }

        if (this.detectCollision(ballRect, paddle2Rect) && this.gameState.ball_velocity_x > 0) {
          this.handleBallCollision(ballRect, paddle2Rect);
        }
      } else {
        // Mobile Collision
        const paddle1Rect = {
          x: this.player1_x * this.canvasWidth - this.paddleHalfWidthMobile,
          y: this.canvasHeight - 30 - this.paddleHeightMobile, // Position du paddle en bas
          width: this.paddleHalfWidthMobile * 2,
          height: this.paddleHeightMobile,
        };

        const opponentRect = {
          x: this.canvasWidth * 0.5 - this.paddleHalfWidthMobile,
          y: 20, // Position du paddle en haut
          width: this.paddleHalfWidthMobile * 2,
          height: this.paddleHeightMobile,
        };

        if (this.detectCollision(ballRect, paddle1Rect) && this.gameState.ball_velocity_y > 0) {
            this.handleBallCollision(ballRect, paddle1Rect, 'y');
        }

        if (this.detectCollision(ballRect, opponentRect) && this.gameState.ball_velocity_y < 0) {
            this.handleBallCollision(ballRect, opponentRect, 'y');
        }
      }
    },

    detectCollision(rect1, rect2) {
      return (
        rect1.x < rect2.x + rect2.width &&
        rect1.x + rect1.width > rect2.x &&
        rect1.y < rect2.y + rect2.height &&
        rect1.y + rect1.height > rect2.y
      );
    },

    handleBallCollision(ballRect, paddleRect, axis = 'x') {
      if (axis === 'x') {
        this.gameState.ball_velocity_x *= -1;
        this.gameState.ball_velocity_y = (ballRect.y + ballRect.height / 2 - (paddleRect.y + paddleRect.height / 2)) * 0.1 / this.canvasHeight;
      } else if (axis === 'y') {
        this.gameState.ball_velocity_y *= -1;
        this.gameState.ball_velocity_x = (ballRect.x + ballRect.width / 2 - (paddleRect.x + paddleRect.width / 2)) * 0.1 / this.canvasWidth;
      }
      this.ballSpeedFactor = Math.min(this.maxBallSpeed, this.ballSpeedFactor + 5);
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
        ctx.fillRect(20, this.gameState.player1_y * canvas.height - this.paddleHeight / 2, this.paddleWidth, this.paddleHeight);
        ctx.fillRect(canvas.width - 30, this.gameState.player2_y * canvas.height - this.paddleHeight / 2, this.paddleWidth, this.paddleHeight);
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
        winner = this.gameState.score1 > this.gameState.score2 ? "Player" : "Opponent";
      } else {
        winner = this.gameState.score1 > this.gameState.score2 ? "Opponent" : "Player";
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
  background-color: black;
}

</style>