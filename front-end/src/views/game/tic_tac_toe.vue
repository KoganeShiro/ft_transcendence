<template>
  <div class="tic-tac-toe-page">
    <HeaderOrganism />

    <!-- Heading showing which mode is active -->
    <div class="heading">
      <h1>Tic Tac Toe - {{ mode }} mode</h1>
    </div>

    <!-- Game content -->
    <div class="tic-tac-toe-content">
      <TicTacToeGame :mode="mode" :useImages="false" />
    </div>

    <FooterOrganism />
  </div>
</template>

<script>
import { computed } from "vue";
import { useRoute } from "vue-router";
import HeaderOrganism from "@/components/header/navbar.vue";
import FooterOrganism from "@/components/footer.vue";
import TicTacToeGame from "@/components/game/TicTacToeGame.vue";

export default {
  name: "TicTacToe",
  components: {
    HeaderOrganism,
    FooterOrganism,
    TicTacToeGame,
  },
  setup() {
    const route = useRoute();

    const mode = computed(() => {
      console.log("Route params:", route.params);
      return route.params.mode;
    });

    return { mode };
  },
};
</script>

<style scoped>
.tic-tac-toe-page {
  background-color: #222;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.tic-tac-toe-content {
  margin: 50px auto;
  line-height: 1.6;
}

@media screen and (max-width: 768px) {
  .heading {
    font-size: 1rem;
  }
}
</style>
