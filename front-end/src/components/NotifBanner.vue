<template>
  <div v-if="visible" class="tournament-banner">
    <div class="banner-content">
      <p class="banner-message">
        {{ message }} <strong>#{{ tournamentId }}</strong>
      </p>
      <button class="close-btn" @click="closeBanner">×</button>
    </div>
  </div>
</template>

<script>
export default {
  name: "TournamentBanner",
  props: {
    tournamentId: {
      type: [String, Number],
      required: true,
    },
    message: {
      type: String,
      default: "A new tournament has been created!",
    },
    duration: {
      type: Number,
      default: 0,
    },
  },
  data() {
    return {
      visible: true,
    };
  },
  mounted() {
    if (this.duration > 0) {
      setTimeout(() => {
        this.visible = false;
      }, this.duration);
    }
  },
  methods: {
    closeBanner() {
      this.visible = false;
    },
  },
};
</script>

<style scoped>
.tournament-banner {
  position: fixed;
  margin-top: 60px;
  left: 0;
  width: 100%;
  background-color: var(--banner-bg, #ffcc00);
  color: var(--banner-text, #333);
  padding: 15px;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  z-index: 1000;
}

.banner-content {
  display: flex;
  align-items: center;
  max-width: 1200px;
  width: 100%;
  padding: 0 20px;
  justify-content: space-between;
}

.banner-message {
  margin: 0;
  font-size: 18px;
  flex-grow: 1;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  line-height: 1;
  cursor: pointer;
  color: var(--banner-text, #333);
}
</style>
