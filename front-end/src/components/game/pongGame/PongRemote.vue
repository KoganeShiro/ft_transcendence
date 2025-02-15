<template>
  <div>
    <canvas 
      ref="pongCanvas"
      class="canvas"
      :width="900"
      :height="500">
    </canvas>
  </div>
</template>

<script>
import API from '@/api.js';

export default {
  name: 'PongRemote',
  data() {
    return {
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
      keysPressed: {
        up: false,
        down: false,
      },
      localPlayer: {
        pseudo: "Player1",
        imageUrl: "",
        link: ""
      },
      opponentPlayer: {
        pseudo: "loading...",
        imageUrl: "",
        link: ""
      },
      frameCount: 0,
      lastFrameTime: 0,
      fps: 0,
    };
  },
  methods: {
    connectToGame() {
      if (this.gameSocket) return;
      this.gameSocket = new WebSocket(`wss://${window.location.host}/ws/pong/`);
      
      this.gameSocket.onopen = () => {
        // Get local player info via API
        API.get('/api/profile/').then(response => {
          const username = response.data.username;
          this.localPlayer.pseudo = username;
          // Optionally update imageUrl and link if available
          // Emit updated local player to the parent
          this.$emit('players-update', {
            localPlayer: this.localPlayer,
            opponentPlayer: this.opponentPlayer
          });
          // Send init message to WebSocket
          const initMessagePayload = {
            type: "init",
            info: {
              game: "creat",
              playerName: username,
            }
          };
          this.gameSocket.send(JSON.stringify(initMessagePayload));
        });
      };

      this.gameSocket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        const messageType = data.type;
        
        if (messageType === "game_update") {
          this.gameState = data.game_state;
          this.updateCanvas();
        } else if (messageType === "players_ready") {
          // Determine opponent username based on player role
          let opponentUsername = "";
          if (this.playerRole === "player1") {
            opponentUsername = data.player2;
          } else {
            opponentUsername = data.player1;
          }
          // Initially update opponentPlayer with the received username
          this.opponentPlayer.pseudo = opponentUsername;
          // Now call the API to get the opponent's full profile details
          API.get(`/api/profile/${opponentUsername}`)
            .then(response => {
              // Update opponentPlayer with data from the API
              this.opponentPlayer.pseudo = response.data.username;
              this.opponentPlayer.imageUrl = response.data.cover_photo;
              // Optionally update link if available
              // Emit updated players data to the parent
              this.$emit('players-update', {
                localPlayer: this.localPlayer,
                opponentPlayer: this.opponentPlayer
              });
            })
            .catch(err => {
              console.error("Error fetching opponent profile", err);
              // Fallback: keep the username and clear the image if necessary
              this.opponentPlayer.pseudo = opponentUsername;
              this.opponentPlayer.imageUrl = "";
              this.$emit('players-update', {
                localPlayer: this.localPlayer,
                opponentPlayer: this.opponentPlayer
              });
            });
          this.gameStarted = true;
        } else if (messageType === "role_assignment") {
          this.playerRole = data.role;
        } else if (messageType === "game_over") {
          this.gameStarted = false;
          // Handle game over logic if needed
        }
      };

      this.gameSocket.onclose = () => {
        this.gameSocket = null;
        this.gameStarted = false;
      };
    },
    sendPlayerMoves() {
      if (!this.gameSocket || this.gameSocket.readyState !== WebSocket.OPEN) return;
      const moves = {
        up: this.keysPressed.up,
        down: this.keysPressed.down
      };
      const message = {
        type: "moves",
        player: this.playerRole,
        moves: moves
      };
      this.gameSocket.send(JSON.stringify(message));
    },
    updateCanvas() {
      const canvas = this.$refs.pongCanvas;
      const ctx = canvas.getContext('2d');
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.fillStyle = 'white';

      // Calculate dimensions
      const ballRadius = Math.min(canvas.width, canvas.height) * 0.015;
      const paddleMarginHorizontal = canvas.width * 0.03;
      const paddleWidth = canvas.width * 0.012;
      const paddleHeight = canvas.height * 0.1;
      const scoreFontSize = Math.min(canvas.width, canvas.height) * 0.04;
      const scoreMarginTop = scoreFontSize + 10;

      // Draw the ball
      ctx.beginPath();
      ctx.arc(this.gameState.ball_x * canvas.width, this.gameState.ball_y * canvas.height, ballRadius, 0, Math.PI * 2);
      ctx.fill();

      // Draw paddles
      ctx.fillRect(paddleMarginHorizontal, this.gameState.player1_y * canvas.height - paddleHeight / 2, paddleWidth, paddleHeight);
      ctx.fillRect(canvas.width - paddleMarginHorizontal - paddleWidth * 2, this.gameState.player2_y * canvas.height - paddleHeight / 2, paddleWidth, paddleHeight);

      // Draw scores
      ctx.font = `${scoreFontSize}px Arial`;
      ctx.fillText(this.gameState.score1, canvas.width / 4, scoreMarginTop);
      ctx.fillText(this.gameState.score2, 3 * canvas.width / 4, scoreMarginTop);
    },
    animationLoop() {
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
      if (event.key === 'ArrowUp') {
        this.keysPressed.up = false;
      }
      if (event.key === 'ArrowDown') {
        this.keysPressed.down = false;
      }
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
    if (this.gameSocket) {
      this.gameSocket.close();
    }
  },
};
</script>
