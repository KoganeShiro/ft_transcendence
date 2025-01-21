<template>
    <div class="button-group">
      <slot />
    </div>
  </template>
  
  <script>
  export default {};
  </script>
  
  <style scoped>
  .button-group {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  </style>
  