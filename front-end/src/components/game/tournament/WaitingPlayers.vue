<template>
  <div class="container">
    <h2>{{ $t("waiting-players") }}...</h2>
    <Card class="card">
      <div class="players-grid">
        <TextBox
          class="player-name"
          v-for="(player, index) in playerNames"
          :key="index"
          :placeholder="`${$t('player')} ${index + 1}`"
          v-model="playerNames[index]"
          :disabled="index === 0 && !isCreator"
          @save="updatePlayerNames"
          :modifiable="true" 
        />
      </div>
      <div>
        <ButtonAtom
          class="start-button"
          variant="42"
          fontSize="18px"
          @click="startTournament"
          :disabled="tournamentStarted || playerNames.length < 4"
        >
          {{ $t("start-tournament") }}
        </ButtonAtom>
      </div>
      <div v-if="startCountdown > 0 && !tournamentStarted">
        <p :class="{ 'start-text': !isCreator }">{{ $t("start-tournament") }} {{ $t("in") }} {{ startCountdown }} seconds...</p>
      </div>
    </Card>
  </div>
</template>

<script>
import API from "@/api";
import Card from "@/components/atoms/Card.vue";
import TextBox from "@/components/atoms/ModifyInformations.vue";
import ButtonAtom from "@/components/atoms/Button.vue";

export default {
  name: "WaitingPlayers",
  components: {
    Card,
    ButtonAtom,
    TextBox,
  },
  props: ['players', 'isCreator', 'tournamentId'],
  data() {
    return {
      playerNames: ['Player 1', 'Player 2', 'Player 3', 'Player 4'],
      tournamentStarted: false,
      startCountdown: 0,
      showQuitConfirm: false,
      user: {
        name: '',
        cover_photo: '',
      },
      loading: false,
    };
  },
  created() {
    this.fetchUserProfile();
  },
  methods: {
    fetchUserProfile() {
      if (this.loading) return;
      this.loading = true;
      API.get("/api/profile/")
        .then(response => {
          const data = response.data;
          console.log("Account data fetched successfully:", data);
          this.user.name = data.username;
          this.user.cover_photo = data.cover_photo;
          this.playerNames[0] = this.user.name;
          this.$emit('updatePlayerNames', this.playerNames);
        })
        .catch(error => {
          console.error("Error fetching account data:", error);
        })
        .finally(() => {
          this.loading = false;
        });
    },
    startTournament() {
      this.tournamentStarted = true;
      this.$emit('startTournament');
    },
    updatePlayerNames() {
      if (this.loading) return;
      this.loading = true;
      this.$emit('updatePlayerNames', this.playerNames);
      this.loading = false;
    }
  },
  // watch: {
  //   players(newPlayers) {
  //     this.playerNames = [this.user.name, ...newPlayers.map(player => player.name)];
  //     this.updatePlayerNames();
  //   }
  // }
};
</script>

<style scoped>
.container {
  margin-top: 100px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.tournament-id {
  font-size: 20px;
  margin: 20px 0;
}

.card {
  height: 280px;
  width: 550px;
  background: #333;
  border-radius: 10px;
}

.players-grid {
  margin-top: 10px;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.start-button {
  margin-top: 65px;
  padding: 10px;
  margin-bottom: 15px;
}

.player-name {
  width: 230px;
}

.start-text {
  margin-top: 55px;
}

@media (max-width: 768px) {
  .container {
    margin-top: 50px;
  }
  .card {
    width: 275px;
    height: 380px;
  }
  .players-grid {
    grid-template-columns: 1fr;
  }
  .player-name {
    width: 280px;
  }
  .start-button {
    margin-top: 60px;
  }
}
</style>