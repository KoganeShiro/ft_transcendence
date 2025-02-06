<template>
  <div class="template">
    <HeaderOrganism />
    <div class="container">
      <h2>{{ $t("waiting-players") }}...</h2>
      <p class="tournament-id">
        {{ $t("tournament-id") }}: <strong>{{ tournamentId }}</strong>
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
            :disabled="tournamentStarted"
          >
            {{ $t("start-tournament") }}
          </ButtonAtom>
          <div v-if="startCountdown > 0 && !tournamentStarted">
            <p>Starting tournament in {{ startCountdown }} seconds...</p>
          </div>
        </div>
      </Card>
    </div>
    <FooterOrganism />
  </div>
</template>

<script>
import { useRouter, useRoute } from "vue-router";
import Card from "@/components/atoms/Card.vue";
import TextBox from "@/components/atoms/ModifyInformations.vue";
import ButtonAtom from "@/components/atoms/Button.vue";
import HeaderOrganism from "@/components/header/navbar.vue";
import FooterOrganism from "@/components/footer.vue";

export default {
  name: "WaitingPlayers",
  components: {
    Card,
    ButtonAtom,
    HeaderOrganism,
    FooterOrganism,
    TextBox,
  },
  data() {
    return {
      playerNames: [],
      isCreator: false,
      tournamentId: "", // to store the tournament code from the route query
      startCountdown: 10, // countdown (in seconds) before automatic start
      tournamentStarted: false,
    };
  },
  setup() {
    const router = useRouter();
    const route = useRoute();
    return { router, route };
  },
  created() {
    this.isCreator = this.route.query.isCreator === "true";
    const count = Number(this.route.query.playerCount) || 4;
    this.playerNames = Array(count).fill("");
    // Get the tournament code from the route query, or default to "N/A"
    this.tournamentId = this.route.query.tournamentCode || "N/A";
  },
  mounted() {
    if (this.isCreator) {
      this.startTimer();
    }
  },
  methods: {
    startTimer() {
      const timer = setInterval(() => {
        if (this.startCountdown > 0) {
          this.startCountdown--;
        } else {
          clearInterval(timer);
          if (!this.tournamentStarted) {
            this.startTournament();
          }
        }
      }, 1000);
    },
    startTournament() {
      this.tournamentStarted = true;
      // Navigate to the matchmaking/game page.
      this.router.push("/matchmaking");
    },
  },
  // Prevent navigation away from the waiting page
  beforeRouteLeave(to, from, next) {
    next(false);
  },
};
</script>

<style scoped>
.container {
  margin-top: -50px;
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
  height: 150px;
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
}

.player-name {
  width: 230px;
}

@media (max-width: 768px) {
  .card {
    width: 300px;
    height: 300px;
  }
  .players-grid {
    grid-template-columns: 1fr;
  }
  .player-name {
    width: 280px;
  }
  .start-button {
    margin-top: 75px;
  }
}
</style>
