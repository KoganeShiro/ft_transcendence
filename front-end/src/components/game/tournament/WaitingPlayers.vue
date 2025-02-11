<template>
  <div class="container">
    <h2>{{ $t("waiting-players") }}...</h2>
    <p class="tournament-id">
      {{ $t("tournament-id") }} <strong>{{ tournamentId }}</strong>
    </p>
    <Card class="card">
      <div class="players-grid">
        <TextBox
          class="player-name"
          v-for="(player, index) in playerNames"
          :key="index"
          :placeholder="`${$t('player')} ${index + 1}`"
          v-model="playerNames[index]"
          :disabled="!isCreator"
        />
      </div>
      <!-- Only show the start controls if the user is the creator -->
      <div v-if="isCreator">
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
        <p :class="{ 'start-text': !isCreator }" >Starting tournament in {{ startCountdown }} seconds...</p>
      </div>
    </Card>
  </div>
  <!-- Quit confirmation popup: it appears when showQuitConfirm is true -->
  <!-- <ConfirmQuitTournament
    v-if="showQuitConfirm"
    @confirm="quitTournament"
    @cancel="showQuitConfirm = false"
  /> -->
</template>

<script>
import Card from "@/components/atoms/Card.vue";
import TextBox from "@/components/atoms/ModifyInformations.vue";
import ButtonAtom from "@/components/atoms/Button.vue";
// import ConfirmQuitTournament from "@/components/game/tournament/ConfirmQuitTournament.vue";

export default {
  name: "WaitingPlayers",
  components: {
    Card,
    ButtonAtom,
    TextBox,
    // ConfirmQuitTournament, // Register the quit popup component
  },
  props: ['players', 'isCreator', 'tournamentId', 'creatorName'],
  data() {    return {
      playerNames: [this.creatorName, ...this.players.map(player => player.name)],
      tournamentStarted: false,
      startCountdown: 0,
      showQuitConfirm: false
    };
  },
  methods: {
    addPlayer(name) {
      this.playerNames.push(name);
      if (this.playerNames.length >= 4 && !this.tournamentStarted) {
        this.startCountdown = 10;
        const countdownInterval = setInterval(() => {
          if (this.startCountdown > 0) {
            this.startCountdown--;
          } else {
            clearInterval(countdownInterval);
            this.startTournament();
          }
        }, 1000);
      }
    },
    startTournament() {
      this.tournamentStarted = true;
      this.$emit('startTournament');
    },
    // quitTournament() {
    //   this.$emit('quitTournament');
    // }
  },
  watch: {
    players(newPlayers) {
      this.playerNames = [this.creatorName, ...newPlayers.map(player => player.name)];
    }
  },
  mounted() {
    // Hard code new players joining the tournament
    setTimeout(() => { this.addPlayer("Player 4"); }, 2000);
    setTimeout(() => { this.addPlayer("Player 5"); }, 4000);
    setTimeout(() => { this.addPlayer("Player 6"); }, 6000);
  }
};
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  color: white;
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

/*
v-if="!isCreator"
*/
.start-text {
  margin-top: 55px;
}

@media (max-width: 768px) {
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