<template>
    <h1> {{ $t("create-join") }} </h1>
    <div class="container">
  
      <Card class="card">
        <!-- Player Count Selection -->
        <div class="section-nb">
        <label class="label">{{ $t("number-players") }}</label>
          <PlayerCount v-model="playerCount" />
        </div>
  
        <!-- Player Names Input Fields
        <div class="section-player">
          <label class="label">Name of the Players</label>
          <div class="players-grid">
            <TextField
                class="player-name"
              v-for="(player, index) in playerCount"
              :key="index"
              :placeholder="`${index + 1}/ Player name`"
              v-model="playerNames[index]"
            />
          </div>
        </div> -->
        
        <!-- Start Button -->
        <ButtonAtom
            class="create-button"
          variant="ghost"
          fontSize="20px"
          @click="createTournament"
        >
        {{ $t("create-tournament") }}
        </ButtonAtom>
      </Card>
      <Card class="card">
        <!-- Player Count Selection -->
        <div class="section-nb">
        <label class="label">{{ $t("join") }}</label>
          <TextField
            class="tournament-code"
            :placeholder="$t('tournament-id')"
            v-model="playerNames[0]"
            />
        </div>
  
        <!-- Join Button -->
        <ButtonAtom
            class="join-button"
          variant="ghost"
          fontSize="20px"
          @click="createTournament"
        >
        {{ $t("join-tournament") }}
        </ButtonAtom>
      </Card>
    </div>
  </template>
  
  <script>
  import Card from "@/components/atoms/Card.vue";
  import TextField from "@/components/atoms/TextField.vue";
  import PlayerCount from "@/components/game/PlayerCount.vue";
  import ButtonAtom from "@/components/atoms/Button.vue";
  
  export default {
    components: {
      Card,
      TextField,
      PlayerCount,
      ButtonAtom,
    },
    data() {
      return {
        playerCount: 4,
        playerNames: Array(4).fill(""),
      };
    },
    watch: {
      playerCount(newCount) {
        this.playerNames = Array(newCount).fill("");
      },
    },
    methods: {
        createTournament() {
            console.log("Tournament Started with Players:", this.playerNames);
      },
    },
  };
  </script>
  
  <style scoped>
  /* Center the content */
  .container {
    display: flex;
    flex-direction: column;
    align-items: center;
    color: white;
    font-family: "Arial", sans-serif;
    text-align: center;
    padding-top: 50px;
  }
  
  .card {
    height: 250px;
    width: 550px;
    background: #333;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    margin-bottom: 20px;
  }
  
  /* Labels */
  .label {
    font-size: 22px;
    font-weight: bold;
    margin-bottom: 20px;
    display: block;
    text-align: left;
    margin-left: 30px;
  }
  
  /* Grid for player name inputs */
  .players-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }

  .player-name {
    width: 250px;
  }

  .section-nb {
    margin-bottom: 50px;
  }

  .create-button {
    margin-top: 20px;
    padding: 15px 0;
  }

  .tournament-code {
    margin-top: 30px;
    width: 350px;
    margin-left: 25px;
  }

  @media screen and (max-width: 768px) {
    .card {
      width: 90%;
    }

    h1 {
      font-size: 25px;
    }

    .label {
      font-size: 19px;
    }

    .tournament-code {
      width: 80%;
      margin-left: 18px;
    }
    
  }
  </style>
  