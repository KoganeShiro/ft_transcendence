<template>
  <div>
    <h1>Pong Game</h1>
    <canvas ref="pongCanvas" width="900" height="500"></canvas>
    <div v-if="gameStarted">
      <p>Score: Player 1 - {{ gameState.score1 }} | Player 2 - {{ gameState.score2 }}</p>
    </div>
    <div v-else>
      <p>Waiting for players...</p>
    </div>
  </div>
</template>

<script>
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
      keysPressed: {
        up: false,
        down: false,
      },
      frameCount: 0, // AJOUTER CE COMPTEUR
      lastFrameTime: 0, // AJOUTER CETTE VARIABLE
      fps: 0, // AJOUTER CETTE VARIABLE POUR FPS
    };
  },

  methods: {
    // Initialisation de la connexion WebSocket
  connectToGame() {
    if (this.gameSocket) return;

    // console.log('Tentative de connexion WebSocket...');
    // this.gameSocket = new WebSocket('ws://localhost:8000/ws/pong/');
    this.gameSocket = new WebSocket('wss://c1r6p9.42lehavre.fr:1443/ws/pong/');

    this.gameSocket.onopen = () => {
      // console.log('Connexion WebSocket réussie !');
      this.gameSocket.send(JSON.stringify({
        type: "init",
        info:{
          game: "creat",
        }
      }));
      // this.sendInitialMoves();
    };

    this.gameSocket.onmessage = (function(event) {
      const message = JSON.parse(event.data);
      // console.log("🔵 CLIENT - Message WebSocket REÇU (BRUT):", message); // LOG BRUT

      if (message.type === 'game_update') {
        this.updateGameState(message);
      } else if (message.type === 'role_assignment') {
        this.playerRole = message.role; // Stocker le rôle du joueur (player1 ou player2)
      }

      if (message.role) {
        this.playerRole = message.role; // Stocker le rôle du joueur (player1 ou player2) -  <-- CETTE LIGNE EST REDONDANTE ET INUTILE (déjà fait dans le bloc 'role_assignment')
      }
    }).bind(this);

    this.gameSocket.onclose = () => {
      // console.log('Connexion WebSocket fermée.');
      this.gameSocket = null;
      this.gameStarted = false; // 🔥 Arrêter le jeu en cas de déconnexion
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
      // console.log("🟢 CLIENT :",message);
    },

    // Mettre à jour l'état du jeu à chaque cycle
    updateGameState(message) { // <-- REVENIR AU PARAMÈTRE "message" (PLUS CLAIR)
    // console.log("🔵 🔵🔵🔵🔵CLIENT - updateGameState() - THIS CONTEXT:", this); // <-- LOG DU CONTEXTE this (À GARDER)
    //     console.log("🔵🔵🔵🔵🔵 ENTERED updateGameState - message:", message); // <-- AJOUTER CE NOUVEAU LOG (TRÈS IMPORTANT !)

    //     console.log('🔵 CLIENT - Début traitement message "game_update" - message.game_state:', message.game_state);
    //     console.log('🔵 CLIENT - updateGameState() - ETAT DU JEU AVANT MISE A JOUR - this.gameState:', this.gameState);

        // Log de l'état du jeu AVANT la mise à jour
        // console.log("🔵 🔵🔵🔵🔵 AVANT:", this.gameState); // <-- LOG DU CONTEXTE this (À GARDER)
        // console.log("🔵 MESSAGE",message.game_state);
        this.gameState = message.game_state; 
        console.log("🔵 🔵🔵🔵🔵 APRES:", this.gameState); // <-- LOG DU CONTEXTE this (À GARDER)
        // <-- UTILISER message.game_state POUR METTRE À JOUR this.gameState (TRÈS IMPORTANT)
        // Log de l'état du jeu APRÈS la mise à jour
        this.updateCanvas();
      },

    // Dessiner l'état du jeu sur le canvas
    updateCanvas() {
      const canvas = this.$refs.pongCanvas;
      const ctx = canvas.getContext('2d');
      
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.fillStyle = 'white';

      // Dessiner la balle
      ctx.beginPath();
      ctx.arc(this.gameState.ball_x * canvas.width, this.gameState.ball_y * canvas.height, 7, 0, Math.PI * 2);
      ctx.fill();

    //   console.log("🔵 CLIENT - updateCanvas() - AVANT dessin Paddle 1 - this.gameState.player1_y:", this.gameState.player1_y);
    //  console.log("🔵 CLIENT - updateCanvas() - AVANT dessin Paddle 2 - this.gameState.player2_y:", this.gameState.player2_y);

      // Dessiner les paddles
      ctx.fillRect(20, this.gameState.player1_y * canvas.height - 30, 10, 60);
      ctx.fillRect(canvas.width - 30, this.gameState.player2_y * canvas.height - 30, 10, 60);

      // Affichage des scores
      ctx.font = '30px Arial';
      ctx.fillText(this.gameState.score1, canvas.width / 4, 30);
      ctx.fillText(this.gameState.score2, 3 * canvas.width / 4, 30);
    },

    animationLoop() {

      // console.time('🔵 CLIENT - updateCanvas() execution time'); // DÉBUT MESURE TEMPS
        this.updateCanvas();
        // console.timeEnd('🔵 CLIENT - updateCanvas() execution time'); // FIN MESURE TEMPS


      this.frameCount++;

      const currentTime = performance.now(); // TEMPS ACTUEL EN MILLISECONDES
        const deltaTime = currentTime - this.lastFrameTime; // TEMPS ÉCOULÉ DEPUIS LA FRAME PRÉCÉDENTE
        if (deltaTime >= 1000) { // SI PLUS DE 1 SECONDE S'EST ÉCOULÉE
          this.fps = this.frameCount; // METTRE À JOUR FPS (FRAMES PAR SECONDE)
          this.frameCount = 0; // RÉINITIALISER COMPTEUR DE FRAMES
          this.lastFrameTime = currentTime; // METTRE À JOUR LE TEMPS DE LA DERNIÈRE FRAME
          // console.log("🔵 CLIENT - FPS (Frames Per Second):", this.fps); // LOG FPS DANS LA CONSOLE
        }

      // // this.updateCanvas(); 
      requestAnimationFrame(this.animationLoop);
    },

    // Simuler l'envoi des mouvements
    // sendInitialMoves() {
    //   // Par exemple, tu pourrais détecter les touches fléchées pour les mouvements :
    //   window.addEventListener('keydown', this.handleKeyDown);
    //   window.addEventListener('keyup', this.handleKeyUp);
    // },

    handleKeyDown(event) {
      if (!this.playerRole) return;
      if (event.key === 'ArrowUp') {
        this.keysPressed.up = true;
        // console.log(`'${this.playerRole} begin arrow up'`)
      }
      if (event.key === 'ArrowDown') {
        this.keysPressed.down = true;
        // console.log(`'${this.playerRole} begin arrow down'`)
      }
      this.sendPlayerMoves();
    },

    handleKeyUp(event) {
      if (!this.playerRole) return;
      if (event.key === 'ArrowUp'){
        // console.log(`${this.playerRole} stop arrow up`)
        this.keysPressed.up = false;
      }
      if (event.key === 'ArrowDown') {
        // console.log(`'${this.playerRole} stop arrow down'`)
        this.keysPressed.down = false;
      }
      this.sendPlayerMoves();
    },
  },

  mounted() {
    this.connectToGame();
    // gameState: {
    //     ball_x: 0.5,
    //     ball_y: 0.5,
    //     score1: 0,
    //     score2: 0,
    //     player1_y: 0.5,
    //     player2_y: 0.5,
    //   },
    window.addEventListener('keydown', this.handleKeyDown);
    window.addEventListener('keyup', this.handleKeyUp);
    this.animationLoop(); // 👈👈👈 AJOUTER CETTE LIGNE EXACTEMENT ICI !!!  *C'EST ESSENTIEL POUR DÉMARRER LA BOUCLE D'ANIMATION*
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

<style scoped>
#gameCanvas {
  border: 1px solid black;
  background-color: #000;
}
</style>
