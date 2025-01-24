<template>
    <button @click="toggleTheme">Toggle Theme</button>
  </template>
  
  <script>
  import { mapState } from "vuex";
  
  export default {
    computed: {
      ...mapState(["theme"]),
    },
    watch: {
      theme(newTheme) {
        document.body.className = newTheme;
      },
    },
    mounted() {
      document.body.className = this.theme;
    },
  };
  </script>
  