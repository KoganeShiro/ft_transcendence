<template>
  <div class="tournament-container">
    <h2 class="tournament-title">{{ $t("matchmaking") }}</h2>
    <div class="matches">
      <MatchItem
        v-for="match in matches"
        :key="match.id"
        :match="match"
      />
    </div>
    <div v-if="timer > 0" class="timer">
      {{ timer }} {{ $t("until-start") }}
    </div>
  </div>
</template>

<script>
import MatchItem from '@/components/game/tournament/Match.vue';

export default {
  components: { MatchItem },
  props: ['matches'],
  data() {
    return {
      timer: 5
    };
  },
  mounted() {
    this.startTimer();
  },
  methods: {
    startTimer() {
      const interval = setInterval(() => {
        if (this.timer > 0) {
          this.timer--;
        } else {
          clearInterval(interval);
          this.$emit('matchStart');
        }
      }, 1000);
    }
  }
};
</script>

<style scoped>
.tournament-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 30px;
  background-color: var(--card-color);
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.tournament-title {
  text-align: center;
  font-size: 2.5em;
  margin-bottom: 30px;
  text-transform: uppercase;
  letter-spacing: 2px;
}

.matches {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  gap: 20px;
}

.timer {
  margin-top: 40px;
  font-size: 1.4em;
  font-weight: bold;
  text-align: center;
  padding: 15px;
  background-color: var(--card-color);
  border-radius: 8px;
}

@media (max-width: 600px) {
  .tournament-container {
    padding: 20px;
  }

  .tournament-title {
    font-size: 2em;
  }

  .timer {
    font-size: 1.2em;
  }
}
</style>
