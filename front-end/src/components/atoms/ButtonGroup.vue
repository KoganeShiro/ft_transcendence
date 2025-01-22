<template>
  <div class="button-group">
    <slot></slot>
  </div>
</template>

<script>
export default {};
</script>

<style scoped>
.button-group {
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;
  justify-content: center;
  gap: 5px;
}
</style>
