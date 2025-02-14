<template>
  <div>
    <!-- <h1>Pong Game</h1> -->
    <canvas 
      ref="pongCanvas"
      class="canvas"
      :width=900
      :height=500>
    </canvas>
    <!-- <div v-if="gameStarted && !gameOverMessage">  <p>Score: Player 1 - {{ gameState.score1 }} | Player 2 - {{ gameState.score2 }}</p>
    </div>
    <div v-else-if="gameOverMessage"> <h2>Partie Terminée !</h2>
      <p>{{ gameOverMessage }}</p> <p>Le vainqueur est : <strong>{{ winner }}</strong></p> </div>
    <div v-else-if="!gameStarted"> <p>Waiting for players...</p>
    </div> -->
  </div>
</template>

<script>
import API from '@/api.js';

export default {
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
      lastSentTime: 0,
      playerRole: null,
      gameOverMessage: null,
      winner: null,
      keysPressed: {
        up: false,
        down: false,
      },
      localPlayer: "Player 1",
      opponentPlayer: "Opponent",
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
        API.get('/api/profile/').then(response => {
        const username = response.data.username;
        this.localPlayer = username;
        let initMessagePayload = {
          type: "init", // Indiquer que c'est un message d'initialisation
          info: {
            game: "creat", // Mode de jeu (create_private ou join_private)
            playerName: username,
          }
        };
        this.gameSocket.send(JSON.stringify(initMessagePayload));
        // this.sendInitialMoves();
      });
    }
      this.gameSocket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        const messageType = data.type;
  
        if (messageType === "game_update") {
          this.gameState = data.game_state;
          this.updateCanvas();
        } 
        else if (messageType === "players_ready") {
          if(this.playerRole === "player1"){
            this.opponentPlayer = data.player2;
          }
          else{
            this.opponentPlayer = data.player1;
          }
          console.log("Oponant :", this.opponentPlayer);
          this.gameStarted = true;
        } 
        else if (messageType === "role_assignment") {
          this.playerRole = data.role;
          console.log(this.playerRole); //if player 1, we are left, if player 2, we are right
        }
        else if (messageType === "game_over") {
          this.gameStarted = false;
          this.gameOverMessage = data.message;
          this.winner = data.winner;
        }
      };

        this.gameSocket.onclose = () => {
        this.gameSocket = null;
        this.gameStarted = false;
      };
    },

    // Envoi des mouvements du joueur
    sendPlayerMoves() {
      if (!this.gameSocket || this.gameSocket.readyState !== WebSocket.OPEN) return;
      
      const moves = { // Créez l'objet 'moves' directement avec les clés "up" et "down"
        up: this.keysPressed.up,    // Utilisez this.keysPressed.up directement
        down: this.keysPressed.down  // Utilisez this.keysPressed.down directement
      };

      const message = {
        type: "moves",
        player: this.playerRole, // Gardez le rôle du joueur pour identification
        moves: moves             // Envoyez l'objet 'moves'
      };

      this.gameSocket.send(JSON.stringify(message));
    },

    // Mettre à jour l'état du jeu à chaque cycle
    updateGameState(message) { // <-- REVENIR AU PARAMÈTRE "message" (PLUS CLAIR)
        this.gameState = message.game_state; 
        this.updateCanvas();
      },

    // Dessiner l'état du jeu sur le canvas
    updateCanvas() {
      const canvas = this.$refs.pongCanvas;
      const ctx = canvas.getContext('2d');

      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.fillStyle = 'white';

      // Dimensions responsives (calculées en pourcentage du canvas)
      const ballRadius = Math.min(canvas.width, canvas.height) * 0.015;
      const paddleMarginHorizontal = canvas.width * 0.03;
      const paddleWidth = canvas.width * 0.012;
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

      this.updateCanvas();

      this.frameCount++;

      const currentTime = performance.now(); // TEMPS ACTUEL EN MILLISECONDES
        const deltaTime = currentTime - this.lastFrameTime; // TEMPS ÉCOULÉ DEPUIS LA FRAME PRÉCÉDENTE
        if (deltaTime >= 1000) { // SI PLUS DE 1 SECONDE S'EST ÉCOULÉE
          this.fps = this.frameCount; // METTRE À JOUR FPS (FRAMES PAR SECONDE)
          this.frameCount = 0; // RÉINITIALISER COMPTEUR DE FRAMES
          this.lastFrameTime = currentTime; // METTRE À JOUR LE TEMPS DE LA DERNIÈRE FRAME
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
  },

  mounted() {
    this.connectToGame();
    window.addEventListener('keydown', this.handleKeyDown);
    window.addEventListener('keyup', this.handleKeyUp);
    this.animationLoop();
  },

  beforeUnmount() {
    // Fermer la connexion WebSocket avant de détruire le composant
    window.removeEventListener('keydown', this.handleKeyDown);
    window.removeEventListener('keyup', this.handleKeyUp);
    if (this.gameSocket) {
      this.gameSocket.close();
    }
  },

};
</script>

