<template>
  <div class="page-container">
    <h1>{{ $t("create-join") }}</h1>
    <div class="container">
      <!-- Create Tournament Card -->
      <Card class="card">
        <div class="section-nb">
          <label class="label">{{ $t("number-players") }}</label>
          <PlayerCount v-model="playerCount" />
        </div>

        <ButtonAtom
          class="create-button"
          variant="ghost"
          fontSize="20px"
          @click="createTournament"
        >
          {{ $t("create-tournament") }}
        </ButtonAtom>
      </Card>

      <!-- Join Tournament Card -->
      <Card class="card">
        <div class="section">
          <label class="label">{{ $t("join") }}</label>
          <TextField
            class="tournament-code"
            :placeholder="$t('tournament-id')"
            v-model="tournamentCode"
          />
        </div>

        <ButtonAtom
          class="join-button"
          variant="ghost"
          fontSize="20px"
          @click="joinTournament"
        >
          {{ $t("join-tournament") }}
        </ButtonAtom>
      </Card>
    </div>
  </div>
</template>

<script>
import { inject, ref } from 'vue';
import Card from '@/components/atoms/Card.vue';
import TextField from '@/components/atoms/TextField.vue';
import PlayerCount from '@/components/game/PlayerCount.vue';
import ButtonAtom from '@/components/atoms/Button.vue';

export default {
  components: { Card, TextField, PlayerCount, ButtonAtom },
  setup(_, { emit }) {
    const showTournamentBanner = inject('showTournamentBanner');
    const playerCount = ref(4);
    const tournamentCode = ref('');

    const createTournament = () => {
      // Logic to create a tournament with the specified player count
      const tournamentId = '12345'; // Replace with actual tournament ID from your logic
      showTournamentBanner(tournamentId);
      emit('tournamentCreated', { tournamentId });
    };

    const joinTournament = () => {
      // Logic to join a tournament with the specified tournament code
      //check if the tournament code is valid
      emit('tournamentJoined', tournamentCode.value);
    };

    return {
      playerCount,
      tournamentCode,
      createTournament,
      joinTournament,
    };
  },
};
</script>


<style scoped>
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

  .section-nb {
    margin-bottom: 50px;
  }

  .section {
    margin-bottom: 30px;
  }

  .create-button {
    margin-top: 20px;
    padding: 15px 0;
  }

  .join-button {
    padding: 15px;
  }

  .join-button, .create-button {
    background-color: var(--overlay-color);
    color: var(--text-color);
  }

  .join-button:hover, .create-button:hover {
    background-color: var(--side-btn-color);
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
  