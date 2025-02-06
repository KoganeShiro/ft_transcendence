<template>
  <div :class="cardClass" :style="cardStyle" @click="chooseGame">
    <slot />
  </div>
</template>

<script>
export default {
  props: {
    backgroundImage: {
      type: String,
      required: true,
    },
    gameName: {
      type: String,
      required: true,
    },
    // backgroundColor: {
    //   type: String,
    //   default: "#ffffff", // Default background color
    // },
    padding: {
      type: String,
      default: "20px",
    },
    borderRadius: {
      type: String,
      default: "15px",
    },
    shadow: {
      type: String,
      default: "0 4px 6px rgba(0, 0, 0, 0.1)",
    },
  },
  computed: {
    cardClass() {
      return "game-card";
    },
    cardStyle() {
      return {
        // backgroundColor: this.backgroundColor,
        backgroundImage: `url(${this.getImageUrl(this.backgroundImage)})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        cursor: 'pointer',
        color: 'white',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        textAlign: 'center',
        borderRadius: '15px',
        boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
      };
    },
  },
  methods: {
    chooseGame() {
      this.$emit('game-chosen', this.gameName);
    },
    getImageUrl(imagePath) {
      return new URL(imagePath, import.meta.url).href;
    },
  },
};
</script>


<style scoped>
.game-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.game-card:hover {
  transform: scale(1.05);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

@media (max-width: 600px) {
  .game-card {
    width: 100%;
  }
}
</style>
