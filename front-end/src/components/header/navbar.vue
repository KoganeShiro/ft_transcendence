<template>
    <header class="header">
      <h1>FT_TRANSCENDENCE</h1>
      <button class="menu-btn" @click="toggleMenu">☰</button>
    </header>
  </template>
  
  <script>
  export default {
    methods: {
      toggleMenu() {
        console.log("Menu toggled!");
      },
    },
  };
  </script>
  
  <style scoped>
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #333;
    color: white;
    padding: 10px 20px;
  }
  .menu-btn {
    background: transparent;
    border: none;
    color: white;
    font-size: 1.5rem;
    cursor: pointer;
  }
  </style>
  