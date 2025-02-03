<template>
  <div class="stats-container">
    <h1>Stats</h1>
    <div class="stats">
      <p><strong>Wins:</strong> {{ stats.wins }}</p>
      <p><strong>Losses:</strong> {{ stats.losses }}</p>
      <p><strong>Best Score:</strong> {{ stats.bestScore }}</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      stats: {
        wins: 10,
        losses: 5,
        bestScore: 100,
      },
    };
  },
};
</script>

<style scoped>
.stats-container {
  padding: 20px;
  color: var(--text-color);
}

.stats p {
  font-size: 1.2rem;
  margin: 10px 0;
}
</style>
