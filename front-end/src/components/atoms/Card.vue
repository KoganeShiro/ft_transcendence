<template>
    <div :class="cardClass" :style="cardStyle">
      <slot />
    </div>
  </template>
  
  <script>
  export default {
    props: {
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
      background: {
        type: String,
        default: "#2D2D2D",
      },
      width: {
        type: String,
        default: "",
      },
    },
    computed: {
      cardClass() {
        return "card";
      },
      cardStyle() {
        return {
          padding: this.padding,
          borderRadius: this.borderRadius,
          boxShadow: this.shadow,
          backgroundColor: "var(--card-color)",
          width: this.width,
        };
      },
    },
  };
  </script>
  
  <style scoped>
  .card {
    display: flex;
    flex-direction: column;
  }

  @media (max-width: 700px) {
    .card {
      height: 90%;
    }
  }
  </style>
  