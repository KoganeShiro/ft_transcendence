<template>
  <div class="pong-game-wrapper">
    <!-- Popup is managed internally -->
    <div v-if="showPopup" class="modal-overlay">
      <Card class="modal-card">
        <h2 class="modal-title">{{ $t('game-withfriend') }}</h2>
        <p class="modal-text">{{ $t('join-create-match') }}</p>

        <div class="button-group">
          <Button class="btn" variant="secondary" @click="handleCreate">
            {{ $t('create-game') }}
          </Button>
        </div>

        <!-- Only show the generated code if in create mode and a code exists -->
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
            {{ $t('move-up') }}<span class="span">↑</span>
          </p>
          <p class="mobile-hide">
            {{ $t('move-down') }}<span class="span">↓</span>
          </p>
        </div>
        <canvas
          ref="pongCanvas"
          class="canvas"
          :width="900"
          :height="500"
        ></canvas>
      </div>
    </div>
  </div>
</template>

<script>
import Versus from "@/components/game/Versus.vue";
import Card from "@/components/atoms/Card.vue";
import Button from "@/components/atoms/Button.vue";
import API from '@/api.js';


export default {
  name: "PongFriend",
  components: { Versus, Card, Button },
  data() {
    return {
      isCreatingRoom: false,
      showPopup: true,
      showVersus: false,
      localPlayer: "Player 1",
      opponentPlayer: "Opponent",
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
      lastSentTime: 0,
      winner: null,
      keysPressed: {
        up: false,
        down: false,
      },
      frameCount: 0,
      lastFrameTime: 0,
      fps: 0,
      currentGameMode: null,
      isCreatingPrivateRoom: false,
      isJoiningPrivateRoom: false,
      privateRoomCode: null,
      joinCode: '',
      isCopied: false,
      localPlayer: { name: "Player 1" },
      opponentPlayer: { name: "Opponent" },
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
  this.joinCode = '';
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
  } 
  else {
    alert("Veuillez entrer un code de room privée.");
  }
},
// Set UI state for joining a room
showJoinPrivateRoom() {
  this.isJoiningPrivateRoom = true;
  this.isCreatingPrivateRoom = false;
  // For join, we typically don't display a generated code
  this.privateRoomCode = "";
},
// Save the game mode and connect via WebSocket
startGameMode(mode) {
  this.currentGameMode = mode;
  // console.log("Starting game mode:", mode);
  this.connectToGame(mode);
},

connectToGame(gameMode) {
  if (this.gameSocket) return;
  
  const localGameMode = gameMode;
  const roomName =  "default_room";
  this.gameSocket = new WebSocket(`wss://${window.location.host}/ws/friendPong/${roomName}/`);
  this.gameSocket.onopen = () => {
    API.get('/api/profile/').then(response => {
    const username = response.data.username;
    this.localPlayer = username;
    let initMessagePayload = {
      type: "init", // Indiquer que c'est un message d'initialisation
      info: {
        game: localGameMode, // Mode de jeu (create_private ou join_private)
        playerName: username,
      }
    };
    if (gameMode === 'join_private') { // Si mode 'join_private', ajouter le code de join
      initMessagePayload.info.join_code = this.joinCode;
    }
    this.gameSocket.send(JSON.stringify(initMessagePayload)); // **ENVOYER LE MESSAGE JSON "init"**
  });
}
  this.gameSocket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    const messageType = data.type;

    if (messageType === "game_update" && this.gameStarted) {
      this.gameState = data.game_state;
      this.updateCanvas();
    } 
    
    else if (messageType === "players_ready") {
      this.gameStarted = true;
      this.handleMatchReady(data);
    } 
    
    else if (messageType === "role_assignment") {
      this.playerRole = data.role;
      console.log(this.playerRole);
    }

    else if (messageType === "game_over") {
      this.gameStarted = false;
      this.gameOverMessage = data.message;
      this.winner = data.winner;
    }

    else if (messageType === "private_room_code") {
      this.privateRoomCode = data.code; // Stocker le code de room privée reçu du back-end
    }
  };

  this.gameSocket.onclose = () => {
    this.gameSocket = null;
    this.gameStarted = false; // 🔥 Arrêter le jeu en cas de déconnexion
  };
},
handleMatchReady(payload) {
  console.log("Attention magie...",payload);
  if (this.playerRole === "player2") {
    this.opponentPlayer = payload.player1
  }
  else {
    this.opponentPlayer = payload.player2
  }
  console.log("Oponent : ", this.opponentPlayer)
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
  console.log("Sending player moves:", message);
  this.gameSocket.send(JSON.stringify(message));
},
updateGameState(message) {
  this.gameState = message.game_state; 
  this.updateCanvas();
},
updateCanvas() {
  if (!this.gameStarted) return; // Ensure the game has started before updating the canvas
  const canvas = this.$refs.pongCanvas;
  if (!canvas) {
  //   console.warn("Canvas not found – it might not be rendered yet.");
    return;
  }

  console.log("Updating canvas...");
  const ctx = canvas.getContext("2d");
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = "white";

  const ballRadius = Math.min(canvas.width, canvas.height) * 0.015;
      const paddleMarginHorizontal = canvas.width * 0.03;
      const paddleWidth = canvas.width * 0.013;
      const paddleHeight = canvas.height * 0.1;
      const scoreFontSize = Math.min(canvas.width, canvas.height) * 0.04;
      const scoreMarginTop = scoreFontSize + 10;

      // Dessiner la balle
      ctx.beginPath();
      ctx.arc(this.gameState.ball_x * canvas.width, this.gameState.ball_y * canvas.height, ballRadius, 0, Math.PI * 2);
      ctx.fill();

      // Dessiner les paddles (centrés verticalement et positionnés avec marges horizontales)
      ctx.fillRect(paddleMarginHorizontal, this.gameState.player1_y * canvas.height - paddleHeight / 2, paddleWidth, paddleHeight);
      ctx.fillRect(canvas.width - paddleMarginHorizontal - paddleWidth - paddleWidth, this.gameState.player2_y * canvas.height - paddleHeight / 2, paddleWidth, paddleHeight); // Ajustement pour positionner correctement Paddle 2

      // Affichage des scores (positionnés avec marge verticale basée sur la taille de la police)
      ctx.font = `${scoreFontSize}px Arial`;
      ctx.fillText(this.gameState.score1, canvas.width / 4, scoreMarginTop);
      ctx.fillText(this.gameState.score2, 3 * canvas.width / 4, scoreMarginTop);
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
      if (event.key === 'ArrowUp') {
        this.keysPressed.up = true;
      }
      if (event.key === 'ArrowDown') {
        this.keysPressed.down = true;
      }
      this.sendPlayerMoves();
    },

    handleKeyUp(event) {
      if (!this.playerRole) return;
      if (event.key === 'ArrowUp'){
        this.keysPressed.up = false;
      }
      if (event.key === 'ArrowDown') {
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
},
mounted() {
window.addEventListener("keydown", this.handleKeyDown);
window.addEventListener("keyup", this.handleKeyUp);
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
.player-controls {
  margin-bottom: 10px;
}
.pong-page {
  color: #fff;
  position: relative;
}
.content {
  padding: 20px;
  text-align: center;
}
.player-controls {
  margin: 20px auto;
  width: 30%;
  background-color: rgba(17, 16, 16, 0.53);
  border-radius: 8px;
  padding: 10px;
}
.game-container {
  margin-top: 20px;
  border-radius: 8px;
  padding: 10px;
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