<template>
  <div>
    <h2>{{ $t("matchmaking") }}</h2>
    <div class="matches">
      <MatchItem
        v-for="match in matches"
        :key="match.id"
        :match="match"
      />
    </div>
    <div v-if="timer > 0">{{ timer }} {{ $t("until-start") }}</div>
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
.matches {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.timer {
  margin-top: 55px;
  font-size: 1.2em;
  font-weight: bold;
}

</style>