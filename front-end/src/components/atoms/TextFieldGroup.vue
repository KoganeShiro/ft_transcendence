<template>
    <div class="input-group">
      <slot></slot>
    </div>
  </template>
  
  <script>
  export default {};
  </script>
  
  <style scoped>
  .input-group {
    display: flex;
    flex-direction: column;
    flex-wrap: wrap;
    justify-content: center;
    gap: 5px;
  }
  </style>
  