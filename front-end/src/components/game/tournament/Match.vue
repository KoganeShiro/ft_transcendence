<!-- MatchItem.vue -->
<template>
    <div class="match">
      <TextBox :modelValue="match.player1" :modifiable="false" class="field" />
      <span class="vs">vs</span>
      <TextBox :modelValue="match.player2" :modifiable="false" class="field" />
    </div>
  </template>
  
  <script>
  import TextBox from "@/components/atoms/ModifyInformations.vue";
  export default {
    name: "MatchItem",
    components: { TextBox },
    props: {
      match: { type: Object, required: true }
    }
  };
  </script>
  
  <style scoped>
  .match {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    align-items: center;
    margin-bottom: 10px;
    gap: 10px;
    padding: 15px;
    border-radius: 8px;
    background: rgba(99, 99, 99, 0.1);
  }
  .vs {
    font-weight: bold;
    font-size: 1.2em;
    color: var(--text-color);
    margin-bottom: 10px;
  }
  .timer, .status {
    font-weight: bold;
    font-size: 1rem;
  }

  </style>