<template>
  <div class="page-container">
    <h1>{{ $t("history") }}</h1>
    <ul class="history-list">
      <li v-for="(item, index) in history" :key="index">
        {{ item }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      history: [
        "User vs AI on Pong - Win",
        "User vs AI on Tic Tac Toe - Win",
        "User vs AI on Chess - Loss",
      ],
    };
  },
};
</script>

<style scoped>
.page-container {
  padding: 20px;
  color: white;
}

.history-list {
  list-style: none;
  padding: 0;
}

.history-list li {
  padding: 10px;
  background-color: #444;
  margin: 10px 0;
  border-radius: 8px;
}
</style>
