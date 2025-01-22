<template>
    <p :class="className">
      <slot />
    </p>
  </template>
  
  <script>
  export default {
    props: {
      className: {
        type: String,
        default: "",
      },
    },
  };
  </script>
  
  <style scoped>
  p {
    font-family: "Arial", sans-serif;
    margin: 0;
    padding: 0;
  }
  </style>
  