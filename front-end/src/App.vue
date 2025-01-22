<template>
    <div id="app">
      <!-- Main application content will be rendered here -->
      <router-view />
    </div>
  </template>
  
  <script>
  export default {
    name: "App",
  };
  </script>
  
  <style>
  /* General styles for the application */
  #app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    background-color: #222;
    min-height: 100vh;
  }
  body, html {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    background-color: #222;
  }

  </style>
  