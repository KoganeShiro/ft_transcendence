
<template>
  <div class="pong-container">
    <Versus 
      v-if="showVersus"
      :player1="localPlayer"
      :player2="opponentPlayer"
      @time-up="handleTimeUp"
    />
    <div v-else class="content">
    <div class="player-controls">
      <h2 class="mobile-hide">{{ $t('commands') }}</h2>
      <p class="mobile-hide">{{ $t('move-up') }}<span class="span">w</span></p>
      <p class="mobile-hide">{{ $t('move-down') }} <span class="span">s</span></p>
    </div>
    <div class="username">
      <p class="player-left">{{ localPlayer.pseudo }}</p>
      <p class="player-right">{{ opponentPlayer.pseudo }}</p>
    </div>
    <canvas 
      ref="pongCanvas"
      class="canvas"
      :width="896"
      :height="496">
    </canvas>
  </div>
  </div>
</template>

<script>
import API from '@/api.js';
import Versus from '@/components/game/Versus_remote.vue';
import defaultAvatar from '@/assets/profile.png';

export default {
  name: 'PongRemote',
  components: { Versus },
  data() {
    return {
      showVersus: true, // controls overlay visibility
      gameSocket: null,
      gameState: {
        ball_x: 0.5,
        ball_y: 0.5,
        score1: 0,
        score2: 0,
        player1_y: 0.5,
        player2_y: 0.5,
      },
      gameStarted: false,
      playerRole: null,
      keysPressed: { up: false, down: false },
      localPlayer: { pseudo: "Player1", imageUrl: "" },
      opponentPlayer: { pseudo: "loading...", imageUrl: "" },
      frameCount: 0,
      lastFrameTime: 0,
      fps: 0,
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
    connectToGame() {
      if (this.gameSocket) return;
      //call API -> check if online -> YES : continue else Return(login)
      
      
      this.gameSocket = new WebSocket(`wss://${window.location.host}/ws/pong/`);

      this.gameSocket.onopen = () => {
        console.log("[PongRemote] WebSocket connected.");
        // Fetch local profile data
        API.get('/api/profile/')
          .then(response => {
            const username = response.data.username;
            console.log("[PongRemote] Local profile received:", response.data);
            this.localPlayer.pseudo = username;
            this.$emit('players-update', {
              localPlayer: this.localPlayer,
              opponentPlayer: this.opponentPlayer
            });
            const initMessagePayload = {
              type: "init",
              info: { game: "creat", playerName: username }
            };
            this.gameSocket.send(JSON.stringify(initMessagePayload));
          });
      };

      this.gameSocket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        const messageType = data.type;
        // console.log("[PongRemote] Received message:", data);
        
        if (messageType === "game_update") {
          this.gameState = data.game_state;
          this.updateCanvas();
        } 
        else if (messageType === "players_ready") {
          console.log("[PongRemote] players_ready received:", data);
          let opponentUsername = "";
          // Use playerRole to determine opponent username (fallback if role missing)
          if (this.playerRole === "player1") {
            opponentUsername = data.player2;
          } else {
            opponentUsername = data.player1 || data.player2;
          }
          console.log("[PongRemote] Opponent username received:", opponentUsername);
          this.opponentPlayer.pseudo = opponentUsername;
          if (opponentUsername === "loading...") {
            console.log("[PongRemote] Opponent not found yet, waiting...");
            return;
          }
          console.log("[PongRemote] Calling API to get opponent profile for:", opponentUsername);
          API.get(`/api/profile/${opponentUsername}`)
            .then(response => {
              console.log("[PongRemote] Opponent profile received:", response.data);
              this.opponentPlayer.pseudo = response.data.username;
              this.opponentPlayer.imageUrl = response.data.cover_photo;
              // Emit updated players data if needed
              this.$emit('players-update', {
                localPlayer: this.localPlayer,
                opponentPlayer: this.opponentPlayer
              });
              // Signal that an opponent was found: hide the Versus overlay after a delay
              this.handleOpponentFound();
            })
            .catch(err => {
              console.error("[PongRemote] Error fetching opponent profile:", err);
              // Fallback: use the received username with no image
              this.opponentPlayer.pseudo = opponentUsername;
              this.opponentPlayer.imageUrl = defaultAvatar;
              this.$emit('players-update', {
                localPlayer: this.localPlayer,
                opponentPlayer: this.opponentPlayer
              });
              this.handleOpponentFound();
            });
          this.gameStarted = true;
        } else if (messageType === "role_assignment") {
          this.playerRole = data.role;
          console.log("[PongRemote] role_assignment received. Player role is:", this.playerRole);
        } 
        else if (messageType === "game_over") {
          this.gameStarted = false;
          this.winner = data.winner;
          this.handleGameEnded(data.winner);
        }
      };

      this.gameSocket.onclose = () => {
        console.log("[PongRemote] WebSocket closed.");
        this.gameSocket = null;
        this.gameStarted = false;
      };
    },
    handleOpponentFound() {
      console.log("[PongRemote] Opponent found, will hide Versus overlay after delay.");
      // Delay hiding Versus overlay by 3 seconds (adjust as needed)
      setTimeout(() => {
        this.handleTimeUp();
      }, 3000);
    },
    handleTimeUp() {
      console.log("[PongRemote] Versus time-up, hiding overlay.");
      this.showVersus = false;
      // Optionally emit an event to the parent if needed:
      this.$emit('opponent-found');
    },

    async handleGameEnded(winner) {
      if (this.requestSent) return;
      this.requestSent = true;
      try {
        console.log("Game ended. Winner:", winner);
        // Always fetch both profiles.
        const localResponse = await API.get("/api/profile/");
        const opponentResponse = await API.get(`/api/profile/${this.opponentPlayer.pseudo}`);

        let gameOverData = {};
        // Use the player's role to determine if the local player won or lost.
        if (winner === "player1") {
          if (this.playerRole === "player1") {
            // Local wins.
            gameOverData = {
              type: "win",
              winnerName: localResponse.data.username,
              winnerImage: localResponse.data.cover_photo,
              loserName: opponentResponse.data.username,
              loserImage: opponentResponse.data.cover_photo
            };
          } else {
            // Local loses.
            gameOverData = {
              type: "loss",
              winnerName: opponentResponse.data.username,
              winnerImage: opponentResponse.data.cover_photo,
              loserName: localResponse.data.username,
              loserImage: localResponse.data.cover_photo
            };
          }
        } else if (winner === "player2") {
          if (this.playerRole === "player2") {
            // Local wins.
            gameOverData = {
              type: "win",
              winnerName: localResponse.data.username,
              winnerImage: localResponse.data.cover_photo,
              loserName: opponentResponse.data.username,
              loserImage: opponentResponse.data.cover_photo
            };
          } else {
            // Local loses.
            gameOverData = {
              type: "loss",
              winnerName: opponentResponse.data.username,
              winnerImage: opponentResponse.data.cover_photo,
              loserName: localResponse.data.username,
              loserImage: localResponse.data.cover_photo
            };
          }
        } else {
          console.error("Unknown winner:", winner);
          return;
        }
        // Emit the game-over event with the popup data.
        this.$emit("game-over", gameOverData);
      } catch (error) {
        console.error("Error fetching user data:", error);
      }
      finally {
        this.requestSent = false;
      }
      if (this.gameSocket) { // Fermer le WebSocket
        this.gameSocket.close();
        this.gameSocket = null; // Important : mettre gameSocket à null après la fermeture
        this.gameStarted = false; // Réinitialiser gameStarted
      }
    },




    sendPlayerMoves() {
      if (!this.gameSocket || this.gameSocket.readyState !== WebSocket.OPEN) return;
      const moves = { up: this.keysPressed.up, down: this.keysPressed.down };
      const message = { type: "moves", player: this.playerRole, moves: moves };
      this.gameSocket.send(JSON.stringify(message));
    },
    updateCanvas() {
      const canvas = this.$refs.pongCanvas;
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.fillStyle = 'white';
      const ballRadius = Math.min(canvas.width, canvas.height) * 0.015;
      const paddleMarginHorizontal = canvas.width * 0.03;
      const paddleWidth = canvas.width * 0.012;
      const paddleHeight = canvas.height * 0.1;
      const scoreFontSize = Math.min(canvas.width, canvas.height) * 0.04;
      const scoreMarginTop = scoreFontSize + 10;
      ctx.beginPath();
      ctx.arc(this.gameState.ball_x * canvas.width, this.gameState.ball_y * canvas.height, ballRadius, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillRect(paddleMarginHorizontal, this.gameState.player1_y * canvas.height - paddleHeight / 2, paddleWidth, paddleHeight);
      ctx.fillRect(canvas.width - paddleMarginHorizontal - paddleWidth * 2, this.gameState.player2_y * canvas.height - paddleHeight / 2, paddleWidth, paddleHeight);
      ctx.font = `${scoreFontSize}px Arial`;
      ctx.fillText(this.gameState.score1, canvas.width / 4, scoreMarginTop);
      ctx.fillText(this.gameState.score2, 3 * canvas.width / 4, scoreMarginTop);
    },
    animationLoop() {
      if (this.gameStarted == false) return;
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
      if (event.key === 'w') this.keysPressed.up = true;
      if (event.key === 's') this.keysPressed.down = true;
      this.sendPlayerMoves();
    },
    handleKeyUp(event) {
      if (!this.playerRole) return;
      if (event.key === 'w') this.keysPressed.up = false;
      if (event.key === 's') this.keysPressed.down = false;
      this.sendPlayerMoves();
    },
  },

  mounted() {
    this.connectToGame();
    window.addEventListener('keydown', this.handleKeyDown);
    window.addEventListener('keyup', this.handleKeyUp);
    this.animationLoop();
  },
  beforeUnmount() {
    window.removeEventListener('keydown', this.handleKeyDown);
    window.removeEventListener('keyup', this.handleKeyUp);
    if (this.gameSocket) this.gameSocket.close();
  },
};
</script>

<style scoped>
.pong-container {
  position: relative;
}

.content {
	text-align: center;
  }
  .player-controls {
	margin: 10px auto;
	width: 30%;
	background-color: rgba(17, 16, 16, 0.53);
	border-radius: 8px;
	padding: 10px;
  }
  .username {
	display: flex;
	justify-content: space-between;
  }
  .player-left, .player-right {
	font-weight: bold;
	background-color: rgba(17, 16, 16, 0.53);
	border-radius: 8px;
	padding: 10px;
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
	background-color: none;
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
</style>
