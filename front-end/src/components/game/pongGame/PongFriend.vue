<template>
  <div class="pong-game-wrapper">
    <!-- Popup to create or join a room -->
    <div v-if="showPopup" class="modal-overlay">
      <Card class="modal-card">
        <h2 class="modal-title">{{ $t('game-withfriend') }}</h2>
        <p class="modal-text">{{ $t('join-create-match') }}</p>

        <div class="button-group">
          <Button class="btn" variant="secondary" @click="handleCreate">
            {{ $t('create-game') }}
          </Button>
        </div>

        <!-- Display generated code when creating a private room -->
        <div v-if="isCreatingPrivateRoom && privateRoomCode" class="created-match-code">
          <p>{{ $t('match-id') }}</p>
          <div class="code-display">
            <input
              :value="privateRoomCode"
              type="text"
              readonly
              class="generated-code-input"
            />
            <button class="copy-btn" :class="{ copied: isCopied }" @click="copyToClipboard">
              {{ $t('copy') }}
            </button>
          </div>
        </div>

        <!-- Input for joining a room -->
        <div class="form-group">
          <input
            v-model="joinCode"
            type="text"
            placeholder="Enter match code"
            class="match-code-input"
          />
          <Button class="btn" variant="primary" @click="joinPrivateRoom">
            {{ $t('join-game') }}
          </Button>
        </div>
      </Card>
    </div>

    <!-- Once popup is dismissed -->
    <div v-else class="content">
      <!-- Versus screen displayed after match-ready -->
      <Versus
        v-if="showVersus"
        :player1="localPlayer"
        :player2="opponentPlayer"
      />

      <!-- Main game UI -->
      <div v-else>
        <div class="player-controls">
          <h2 class="mobile-hide">{{ $t('commands') }}</h2>
          <p class="mobile-hide">
            {{ $t('move-up') }}<span class="span">w</span>
          </p>
          <p class="mobile-hide">
            {{ $t('move-down') }}<span class="span">s</span>
          </p>
        </div>
        <div class="username">
        <p class="player-left">{{ localPlayer.pseudo }}</p>
        <p class="player-right">{{ opponentPlayer.pseudo }}</p>
      </div>
        <canvas
          ref="pongCanvas"
          class="canvas"
          :width="896"
          :height="496"
        ></canvas>
        <WinnerPopup v-if="showWinner" :winnerName="winnerName" :winnerImage="winnerImage" />
        <LoserPopup v-if="showLoser" :loserName="loserName" :loserImage="loserImage" />
      </div>
    </div>
  </div>
</template>

<script>
import Versus from "@/components/game/Versus.vue";
import Card from "@/components/atoms/Card.vue";
import Button from "@/components/atoms/Button.vue";
import API from '@/api.js';
import WinnerPopup from "@/views/game/winner.vue";
import LoserPopup from "@/views/game/loser.vue";

export default {
  name: "PongFriend",
  components: { Versus, Card, Button, WinnerPopup, LoserPopup },
  data() {
    return {
      // UI states for the room creation/join popup
      isCreatingRoom: false,
      showPopup: true,
      isCreatingPrivateRoom: false,
      isJoiningPrivateRoom: false,
      privateRoomCode: null,
      joinCode: "",
      isCopied: false,
      // Game states
      gameSocket: null,
      gameStarted: false,
      gameState: {
        ball_x: 0.5,
        ball_y: 0.5,
        score1: 0,
        score2: 0,
        player1_y: 0.5,
        player2_y: 0.5,
      },
      playerRole: null,
      gameOverMessage: null,
      winner: null,
      keysPressed: {
        up: false,
        down: false,
      },
      frameCount: 0,
      lastFrameTime: 0,
      fps: 0,
      currentGameMode: null,
      // Match/versus states
      showVersus: false,
      localPlayer: {
        pseudo: "Player1",
        imageUrl: "",
      },
      opponentPlayer: {
        pseudo: "Opponent",
        imageUrl: "",
      },
      // Winner/Loser popup states
      showWinner: false,
      showLoser: false,
      winnerName: "",
      winnerImage: "",
      loserName: "",
      loserImage: "",
      requestSent: false,
    };
  },
  methods: {
    handleCreate() {
      if (this.isCreatingRoom) return; // Prevent multiple clicks
      this.isCreatingRoom = true;
      this.showCreatePrivateRoom();
      this.createPrivateRoom();
    },
    showCreatePrivateRoom() {
      this.isCreatingPrivateRoom = true;
      this.isJoiningPrivateRoom = false;
      this.privateRoomCode = null;
      this.joinCode = "";
    },
    createPrivateRoom() {
      this.privateRoomCode = "Generating...";
      console.log("Creating private room...");
      this.startGameMode("create_private");
    },
    joinPrivateRoom(event) {
      if (event && event.preventDefault) event.preventDefault();
      if (this.joinCode && this.joinCode.trim() !== "") {
        this.showJoinPrivateRoom();
        this.startGameMode("join_private");
      } else {
        alert("Veuillez entrer un code de room privée.");
      }
    },
    // Set UI state for joining a room
    showJoinPrivateRoom() {
      this.isJoiningPrivateRoom = true;
      this.isCreatingPrivateRoom = false;
      this.privateRoomCode = "";
    },
    // Start game mode and connect via WebSocket
    startGameMode(mode) {
      this.currentGameMode = mode;
      this.connectToGame(mode);
    },
    connectToGame(gameMode) {
      if (this.gameSocket) return;
      
      const localGameMode = gameMode;
      const roomName = "default_room";
      this.gameSocket = new WebSocket(`wss://${window.location.host}/ws/friendPong/${roomName}/`);
      this.gameSocket.onopen = () => {
        API.get("/api/profile/").then((response) => {
          const username = response.data.username;
          this.localPlayer.pseudo = username;
          let initMessagePayload = {
            type: "init", // Initialization message
            info: {
              game: localGameMode, // "create_private" or "join_private"
              playerName: username,
            },
          };
          if (gameMode === "join_private") {
            initMessagePayload.info.join_code = this.joinCode;
          }
          this.gameSocket.send(JSON.stringify(initMessagePayload));
        });
      };


      this.gameSocket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        const messageType = data.type;

        if (messageType === "game_update" && this.gameStarted) {
          this.gameState = data.game_state;
          this.updateCanvas();
        } else if (messageType === "players_ready") {
          this.gameStarted = true;
          this.handleMatchReady(data);
        } else if (messageType === "role_assignment") {
          this.playerRole = data.role;
          console.log("Assigned role:", this.playerRole);
        } else if (messageType === "game_over") {
          this.updateCanvas();
          this.gameStarted = false;
          this.gameOverMessage = data.message;
          this.winner = data.winner;
          console.log("End of the game, winner:", data.winner);
          this.handleGameEnded(data.winner);
        } else if (messageType === "private_room_code") {
          this.privateRoomCode = data.code;
        }
      };

      this.gameSocket.onclose = () => {
        this.gameSocket = null;
        this.gameStarted = false; // Stop game on disconnect
      };
    },
    handleMatchReady(payload) {
      if (this.playerRole === "player2") {
        this.opponentPlayer.pseudo = payload.player1;
      } else {
        this.opponentPlayer.pseudo = payload.player2;
      }
      console.log("Opponent:", this.opponentPlayer.pseudo);
      this.showPopup = false;
      this.showVersus = true;
      console.log("Match ready. Starting game...");
      setTimeout(() => {
        this.showVersus = false;
        this.animationLoop();
      }, 3000);
    },
    sendPlayerMoves() {
      if (!this.gameSocket || this.gameSocket.readyState !== WebSocket.OPEN) return;
      const moves = {
        up: this.keysPressed.up,
        down: this.keysPressed.down,
      };
      const message = {
        type: "moves",
        player: this.playerRole,
        moves: moves,
      };
      this.gameSocket.send(JSON.stringify(message));
    },
    updateCanvas() {
      const canvas = this.$refs.pongCanvas;
      if (!canvas) return;
      const ctx = canvas.getContext("2d");
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.fillStyle = "white";

      const ballRadius = Math.min(canvas.width, canvas.height) * 0.015;
      const paddleMarginHorizontal = canvas.width * 0.03;
      const paddleWidth = canvas.width * 0.013;
      const paddleHeight = canvas.height * 0.1;
      const scoreFontSize = Math.min(canvas.width, canvas.height) * 0.04;
      const scoreMarginTop = scoreFontSize + 10;

      // Draw the ball
      ctx.beginPath();
      ctx.arc(
        this.gameState.ball_x * canvas.width,
        this.gameState.ball_y * canvas.height,
        ballRadius,
        0,
        Math.PI * 2
      );
      ctx.fill();

      // Draw the paddles
      ctx.fillRect(
        paddleMarginHorizontal,
        this.gameState.player1_y * canvas.height - paddleHeight / 2,
        paddleWidth,
        paddleHeight
      );
      ctx.fillRect(
        canvas.width - paddleMarginHorizontal - 2 * paddleWidth,
        this.gameState.player2_y * canvas.height - paddleHeight / 2,
        paddleWidth,
        paddleHeight
      );

      // Draw scores
      ctx.font = `${scoreFontSize}px Arial`;
      ctx.fillText(this.gameState.score1, canvas.width / 4, scoreMarginTop);
      ctx.fillText(this.gameState.score2, (3 * canvas.width) / 4, scoreMarginTop);
    },
    animationLoop() {
      if (!this.gameStarted) {
        return;
      }
      this.updateCanvas();
      this.frameCount++;
      const currentTime = performance.now();
      const deltaTime = currentTime - this.lastFrameTime;
      if (deltaTime >= 1000) {
        this.fps = this.frameCount;
        this.frameCount = 0;
        this.lastFrameTime = currentTime;
      }
      requestAnimationFrame(this.animationLoop);
    },
    handleKeyDown(event) {
      if (!this.playerRole) return;
      if (event.key === "w") {
        this.keysPressed.up = true;
      }
      if (event.key === "s") {
        this.keysPressed.down = true;
      }
      this.sendPlayerMoves();
    },
    handleKeyUp(event) {
      if (!this.playerRole) return;
      if (event.key === "w") {
        this.keysPressed.up = false;
      }
      if (event.key === "s") {
        this.keysPressed.down = false;
      }
      this.sendPlayerMoves();
    },
    copyToClipboard() {
      const el = document.createElement("textarea");
      el.value = this.privateRoomCode;
      document.body.appendChild(el);
      el.select();
      document.execCommand("copy");
      document.body.removeChild(el);

      this.isCopied = true;
      setTimeout(() => {
        this.isCopied = false;
      }, 1000);
    },
    async handleGameEnded(winner) {
    if (this.requestSent) return;
    this.requestSent = true;
    try {
      console.log("Game ended. Winner:", winner);
      // Always fetch both profiles.
      const localResponse = await API.get("/api/profile/");
      const opponentResponse = await API.get(`/api/profile/${this.opponentPlayer.pseudo}`);

      if (winner === "player1") {
        // Player1 is declared winner.
        if (this.playerRole === "player1") {
          // Local is player1 and wins.
          this.winnerName = localResponse.data.username;
          this.winnerImage = localResponse.data.cover_photo;
          this.loserName = opponentResponse.data.username;
          this.loserImage = opponentResponse.data.cover_photo;
          this.showWinner = true;
          this.showLoser = false;
        } else {
          // Local is player2 and loses.
          this.winnerName = opponentResponse.data.username; // player1's data (opponent)
          this.winnerImage = opponentResponse.data.cover_photo;
          this.loserName = localResponse.data.username;
          this.loserImage = localResponse.data.cover_photo;
          this.showWinner = false;
          this.showLoser = true;
        }
      } else if (winner === "player2") {
        // Player2 is declared winner.
        if (this.playerRole === "player2") {
          // Local is player2 and wins.
          this.winnerName = localResponse.data.username;
          this.winnerImage = localResponse.data.cover_photo;
          this.loserName = opponentResponse.data.username;
          this.loserImage = opponentResponse.data.cover_photo;
          this.showWinner = true;
          this.showLoser = false;
        } else {
          // Local is player1 and loses.
          this.winnerName = opponentResponse.data.username; // player2's data (opponent)
          this.winnerImage = opponentResponse.data.cover_photo;
          this.loserName = localResponse.data.username;
          this.loserImage = localResponse.data.cover_photo;
          this.showWinner = false;
          this.showLoser = true;
        }
      } else {
        console.error("Unknown winner:", winner);
      }
    } catch (error) {
      console.error("Error fetching user data:", error);
    }
  },

  },
  mounted() {
    window.addEventListener("keydown", this.handleKeyDown);
    window.addEventListener("keyup", this.handleKeyUp);
    // Optionally, start the animation loop if needed
    this.animationLoop();
  },
  beforeUnmount() {
    window.removeEventListener("keydown", this.handleKeyDown);
    window.removeEventListener("keyup", this.handleKeyUp);
    if (this.gameSocket) {
      this.gameSocket.close();
    }
  },
};
</script>



<style scoped>
.pong-game-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.canvas {
  border: 2px solid var(--background-color);
  border-radius: 8px;
}

.pong-page {
  color: #fff;
  position: relative;
}
.content {
  /* padding: 20px; */
  text-align: center;
}
.player-controls {
  margin: 10px auto;
  width: 30%;
  background-color: rgba(17, 16, 16, 0.53);
  border-radius: 8px;
  padding: 5px;
}

.username {
  display: flex;
  justify-content: space-between;
}

.player-left, .player-right {
  font-weight: bold;
  background-color: rgba(17, 16, 16, 0.53);
  border-radius: 8px;
  padding: 0px;
}

.player-left {
  margin-left: 50px;
}
.player-right {
  margin-right: 50px;
}

.game-container {
  margin-top: 20px;
  border-radius: 8px;
  /* padding: 10px; */
}
.span {
  font-weight: bold;
}

@media screen and (max-width: 810px) {
  .mobile-hide {
    display: none;
  }
  .player-controls {
    width: 100%;
    padding: 5px;
    background: none;
    border: none;
  }
  .game-container {
    padding: 5px;
    border: none;
  }
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.397);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10000;
}
.modal-card {
  width: 90%;
  max-width: 400px;
  padding: 20px;
  border-radius: 10px;
  color: #fff;
  text-align: center;
}
.modal-title {
  font-size: 1.8rem;
  margin-bottom: 10px;
}
.modal-text {
  font-size: 1rem;
  margin-bottom: 20px;
}
.button-group {
  display: flex;
  justify-content: space-around;
  margin-bottom: 20px;
}
.form-group {
  margin-bottom: 20px;
}
.match-code-input {
  width: 100%;
  padding: 10px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-sizing: border-box;
  margin: 15px 0 13px;
}
.btn {
  padding: 10px;
  margin-top: 15px;
}
.created-match-code {
  margin: 15px 0;
  padding: 10px;
  background-color: var(--background-light);
  border-radius: 8px;
}
.code-display {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}
.generated-code-input {
  flex: 1;
  padding: 8px;
  border: 1px solid #cccccc94;
  border-radius: 4px;
  background-color: var(--card-color);
  color: white;
}
.copy-btn {
  padding: 8px 15px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.copy-btn:hover {
  background-color: #45a049;
}
.copy-btn.copied {
  animation: copied-animation 0.5s ease-in-out;
}
@keyframes copied-animation {
  0% { background-color: #4CAF50; }
  50% { background-color: #45a049; transform: scale(0.95); }
  100% { background-color: #4CAF50; }
}
@media (max-width: 768px) {
  .modal-card {
    height: 65%;
    width: 78%;
  }
}

</style>