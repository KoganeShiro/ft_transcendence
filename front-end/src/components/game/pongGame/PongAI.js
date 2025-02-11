// PongAI.js
export default {
  start(pongGameInstance) {
    // Store the instance for later use if needed.
    this.gameInstance = pongGameInstance;
    // Clear any existing interval (if any)
    if (this.interval) {
      clearInterval(this.interval);
    }
    // Start an interval loop (roughly 60 FPS)
    this.interval = setInterval(() => {
      const game = this.gameInstance;
      if (!game || !game.gameState) return;
      const state = game.gameState;
      // Current opponent paddle position (player2_y)
      let opponentY = state.player2_y;
      
      // Only adjust when the ball is moving toward the opponent.
      if (state.ball_velocity_x > 0) {
        // Calculate the error between ball and paddle position.
        const error = state.ball_y - opponentY;
        // Set a base paddle speed and increase it with error magnitude.
        let paddleSpeed = 0.005 + 0.01 * Math.abs(error);
        // Apply a dead zone to prevent jitter.
        if (error > 0.02) {
          state.player2_y = Math.min(opponentY + paddleSpeed, 1);
        } else if (error < -0.02) {
          state.player2_y = Math.max(opponentY - paddleSpeed, 0);
        }
      } else {
        // If the ball is moving away, slowly return to center (0.5).
        const centerError = 0.5 - opponentY;
        const centerSpeed = 0.002; // slower correction speed
        if (centerError > 0.01) {
          state.player2_y = Math.min(opponentY + centerSpeed, 1);
        } else if (centerError < -0.01) {
          state.player2_y = Math.max(opponentY - centerSpeed, 0);
        }
      }
    }, 16); // ~60 updates per second
  },
  stop() {
    if (this.interval) {
      clearInterval(this.interval);
      this.interval = null;
    }
  }
};
