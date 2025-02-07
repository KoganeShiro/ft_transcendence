<template>
  <div class="tic-tac-toe-page">
    <HeaderOrganism />

    <!-- Heading showing which mode is active -->
    <div class="heading">
      <h1>Tic Tac Toe - {{ mode }} mode</h1>
    </div>

    <!-- Front for random and friend versus (remote)
            ===+> have the versus component sending
                    information to the backend (who is the opponent)
         Front for solo
            ===+> have the versus component (gameplay on the front)
         Front for local versus
            ===+> have the versus component sending
                    information to the backend (guest and host match)
          Front for 4 player mode
            ===+> have (a new ?) versus component sending
                    information to the backend
     -->

    <!-- Game content -->
    <div class="tic-tac-toe-content">
      <!-- front -->
      <TicTacToeGame />
    </div>

    <FooterOrganism />
  </div>
</template>

<script>
import { computed } from "vue";
import { useRoute } from "vue-router";
import HeaderOrganism from "@/components/header/navbar.vue";
import FooterOrganism from "@/components/footer.vue";
import TicTacToeGame from "@/components/game/TicTacToeFront.vue";

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
  background-color: var(--background-color);
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
