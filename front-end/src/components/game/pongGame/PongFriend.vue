<template>
    <div>
      <!-- <h1>Pong Game</h1>
  
      <div v-if="!gameStarted && !gameOverMessage">
        <h2>Choisissez un mode de jeu :</h2>
  
        <button @click="startGameMode('quick_play')" v-if="false">Jeu Rapide (Non implémenté)</button> <br> <br> <button @click="showCreatePrivateRoom">Créer une Partie Privée</button> <br> <br>
  
        <button @click="showJoinPrivateRoom">Rejoindre une Partie Privée</button> <br> <br>
  
        <div v-if="isCreatingPrivateRoom">
          <h3>Créer une Partie Privée</h3>
          <p>Cliquez sur le bouton ci-dessous pour générer un code de room privée :</p>
          <button @click="createPrivateRoom">Générer un Code de Room Privée</button>
          <div v-if="privateRoomCode">
            <p>Code de votre room privée : <strong>{{ privateRoomCode }}</strong></p>
            <p>Partagez ce code avec votre ami pour qu'il puisse rejoindre votre partie privée.</p>
          </div>
        </div>
  
        <div v-if="isJoiningPrivateRoom">
          <h3>Rejoindre une Partie Privée</h3>
          <p>Entrez le code de la room privée :</p>
          <input type="text" v-model="joinCode" placeholder="Code de la room privée">
          <button @click="joinPrivateRoom">Rejoindre</button>
        </div>
      </div>
   -->
      <canvas
      ref="pongCanvas"
      class="canvas"
      :width="900"
      :height="500"
    ></canvas>
  
      <!-- <div v-if="gameStarted && !gameOverMessage">
        <p>Score: Player 1 - {{ gameState.score1 }} | Player 2 - {{ gameState.score2 }}</p>
      </div>
  
      <div v-else-if="gameOverMessage">
        <h2>Partie Terminée !</h2>
        <p>{{ gameOverMessage }}</p>
        <p>Le vainqueur est : <strong>{{ winner }}</strong></p>
      </div>
  
      <div v-else-if="!gameStarted && !gameOverMessage && !isCreatingPrivateRoom && !isJoiningPrivateRoom">
        <p>En attente de joueurs...</p>  </div> -->
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
        gameOverMessage: null,
        winner: null,
        keysPressed: {
          up: false,
          down: false,
        },
        frameCount: 0, // AJOUTER CE COMPTEUR
        lastFrameTime: 0, // AJOUTER CETTE VARIABLE
        fps: 0, // AJOUTER CETTE VARIABLE POUR FPS
        
        // Nouvelles variables pour la gestion des rooms privées :
        isCreatingPrivateRoom: false, // Booléen pour afficher/masquer la section "Créer une Partie Privée"
        isJoiningPrivateRoom: false,  // Booléen pour afficher/masquer la section "Rejoindre une Partie Privée"
        privateRoomCode: null,       // Pour stocker le code de room privée généré
        joinCode: '',               // Pour stocker le code de room privée saisi par l'utilisateur
        currentGameMode: null,      // Pour stocker le mode de jeu courant ('quick_play'
      };
    },
  
    methods: {
      // Initialisation de la connexion WebSocket
    startGameMode(mode) {
      this.currentGameMode = mode; // Stocker le mode de jeu sélectionné
      this.connectToGame(mode);     // Appeler connectToGame en passant le mode
    },

    showCreatePrivateRoom() {
      this.isCreatingPrivateRoom = true;
      this.isJoiningPrivateRoom = false; // S'assurer que l'autre section est masquée
      this.privateRoomCode = null;      // Réinitialiser le code précédent si affiché
      this.joinCode = '';             // Réinitialiser le code de join si saisi
    },

    showJoinPrivateRoom() {
      this.isJoiningPrivateRoom = true;
      this.isCreatingPrivateRoom = false; // S'assurer que l'autre section est masquée
      this.privateRoomCode = null;      // Réinitialiser le code précédent si affiché
      this.joinCode = '';             // Réinitialiser le code de join si saisi
    },

    createPrivateRoom() {
      this.privateRoomCode = 'Generating...'; // Afficher un message pendant la génération (optionnel)
      this.startGameMode('create_private');   // Lancer la connexion en mode "create_private"
    },

    joinPrivateRoom() {
        if (this.joinCode) {
            this.startGameMode('join_private'); // Lancer la connexion en mode "join_private"
        } else {
            alert("Veuillez entrer un code de room privée."); // Gérer le cas où le code est vide
        }
    },

    connectToGame(gameMode) {
        if (this.gameSocket) return;
        const localGameMode = gameMode;
        const roomName = 'default_room'; // Choisissez un nom de room par défaut pour l'instant
        this.gameSocket = new WebSocket(`wss://${window.location.host}/ws/friendPong/${roomName}/`);  
        this.gameSocket.onopen = () => {
            console.log("avant envoie");
            console.log(localGameMode);

            let initMessagePayload = {
                type: "init", // Indiquer que c'est un message d'initialisation
                info: {
                    game: localGameMode, // Mode de jeu (create_private ou join_private)
                }
            };
            if (gameMode === 'join_private') { // Si mode 'join_private', ajouter le code de join
                initMessagePayload.info.join_code = this.joinCode;
            }
            this.gameSocket.send(JSON.stringify(initMessagePayload)); // **ENVOYER LE MESSAGE JSON "init"**
        };
  
        this.gameSocket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            const messageType = data.type;
    
            // console.log("**[DEBUG FRONTEND] Message WebSocket reçu :", data); //  REMETTEZ CE LOG POUR VOIR TOUS LES MESSAGES
    
            if (messageType === "game_update") {
                this.gameState = data.game_state;
                this.updateCanvas();
            } 
            
            else if (messageType === "players_ready") {
                this.gameStarted = true;
            } 
            
            else if (messageType === "role_assignment") {
                this.playerRole = data.role;
            }

            else if (messageType === "game_over") {
                console.log("**[DEBUG FRONTEND] Message game_over REÇU :", data); // RE-VÉRIFIEZ CE LOG SPÉCIFIQUE
                this.gameStarted = false;
                this.gameOverMessage = data.message;
                this.winner = data.winner;
                console.log("this.gameOverMessage après game_over:", this.gameOverMessage); // AJOUTEZ CE LOG POUR VÉRIFIER LA VARIABLE VUE.JS
                console.log("this.winner après game_over:", this.winner); // AJOUTEZ CE LOG POUR VÉRIFIER LA VARIABLE VUE.JS
                console.log("Partie terminée côté front-end : " + data.message);
            }

            else if (messageType === "private_room_code") {
                this.privateRoomCode = data.code; // Stocker le code de room privée reçu du back-end
                console.log("**[DEBUG FRONTEND] Code de room privée reçu :", this.privateRoomCode);
            }
        };
  
            this.gameSocket.onclose = () => {
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
    //   this.connectToGame();
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
  
  <style scoped>
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