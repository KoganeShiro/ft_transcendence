// PongAI.js

// Helper: Predict ball Y position after t seconds, given current position and vertical velocity.
// It simulates elastic bounces off the top (1) and bottom (0) edges.
function predictBallY(currentY, velocityY, ballSpeedFactor, t) {
  let timeLeft = t;
  let pos = currentY;
  // Convert velocity to normalized units per second.
  let v = velocityY * ballSpeedFactor;
  while (timeLeft > 0) {
    if (v > 0) {
      const timeToTop = (1 - pos) / v;
      if (timeToTop > timeLeft) {
        pos += v * timeLeft;
        timeLeft = 0;
      } else {
        pos = 1;
        v = -v;
        timeLeft -= timeToTop;
      }
    } else if (v < 0) {
      const timeToBottom = pos / (-v);
      if (timeToBottom > timeLeft) {
        pos += v * timeLeft;
        timeLeft = 0;
      } else {
        pos = 0;
        v = -v;
        timeLeft -= timeToBottom;
      }
    } else {
      break; // velocity is zero.
    }
  }
  return Math.max(0, Math.min(1, pos));
}

export default {
  start(pongGameInstance) {
    // Save the game instance reference.
    this.gameInstance = pongGameInstance;
    // Clear any existing intervals.
    if (this.decisionInterval) clearInterval(this.decisionInterval);
    if (this.movementInterval) clearInterval(this.movementInterval);

    // Initialize state variables.
    this.currentDirection = "none"; // "up", "down", or "none"
    // Our snapshot prediction of the ball’s target Y position.
    this.predictedTargetY = 0.5; // default to center

    const tolerance = 0.03;    // Minimum error needed to trigger movement.
    const predictionTime = 1;    // Predict 1 second into the future.

    // Decision interval: take one snapshot every 1000ms.
    // At that moment, if the ball is moving toward the AI (ball_velocity_x > 0),
    // compute the predicted ball Y position over the next 1 second.
    this.decisionInterval = setInterval(() => {
      if (!this.gameInstance || !this.gameInstance.gameState) return;
      const state = this.gameInstance.gameState;
      if (state.ball_velocity_x > 0) {
        this.predictedTargetY = predictBallY(
          state.ball_y,
          state.ball_velocity_y,
          this.gameInstance.ballSpeedFactor,
          predictionTime
        );
      } else {
        // When the ball is moving away, target center.
        this.predictedTargetY = 0.5;
      }
    }, 1000);

    // Movement interval: update paddle movement continuously (~60 FPS).
    // Using the predicted target from the snapshot, calculate the current error and
    // simulate the corresponding key events.
    this.movementInterval = setInterval(() => {
      const state = this.gameInstance.gameState;
      const paddleY = state.player2_y;
      const error = this.predictedTargetY - paddleY;
      let desired = "none";
      if (error > tolerance) {
        desired = "down";
      } else if (error < -tolerance) {
        desired = "up";
      } else {
        desired = "none";
      }
      if (desired !== this.currentDirection) {
        // Release previously held key.
        if (this.currentDirection === "up") {
          window.dispatchEvent(new KeyboardEvent("keyup", { key: "ArrowUp", bubbles: true }));
        } else if (this.currentDirection === "down") {
          window.dispatchEvent(new KeyboardEvent("keyup", { key: "ArrowDown", bubbles: true }));
        }
        // Press the new key if needed.
        if (desired === "up") {
          window.dispatchEvent(new KeyboardEvent("keydown", { key: "ArrowUp", bubbles: true }));
        } else if (desired === "down") {
          window.dispatchEvent(new KeyboardEvent("keydown", { key: "ArrowDown", bubbles: true }));
        }
        this.currentDirection = desired;
      }
      // Otherwise, maintain current key press.
    }, 16); // roughly 60 updates per second
  },
  stop() {
    if (this.decisionInterval) {
      clearInterval(this.decisionInterval);
      this.decisionInterval = null;
    }
    if (this.movementInterval) {
      clearInterval(this.movementInterval);
      this.movementInterval = null;
    }
    // Release any key that is still pressed.
    if (this.currentDirection === "up") {
      window.dispatchEvent(new KeyboardEvent("keyup", { key: "ArrowUp", bubbles: true }));
    } else if (this.currentDirection === "down") {
      window.dispatchEvent(new KeyboardEvent("keyup", { key: "ArrowDown", bubbles: true }));
    }
    this.currentDirection = "none";
  }
};
