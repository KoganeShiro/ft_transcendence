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
        backgroundImage: `url(${this.backgroundImage})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        padding: this.padding,
        borderRadius: this.borderRadius,
        boxShadow: this.shadow,
        cursor: 'pointer',
        color: 'white',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        textAlign: 'center',
        height: '200px',
      };
    },
  },
  methods: {
    chooseGame() {
      this.$emit('game-chosen', this.gameName);
    },
  },
};
</script>

<style scoped>
.game-card {
  display: flex;
  flex-direction: column;
  justify-content: center;
}
</style>