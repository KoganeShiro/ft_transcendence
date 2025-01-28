<template>
  <div class="game-choice-page">
    <HeaderOrganism />
    <div class="game-choice-content">
      <h1>{{ $t("game-choice") }}</h1>
      <div class="game-cards-container">
        <GameCard
          backgroundImage="@/assets/pong.png"
          gameName="Pong"
          @game-chosen="handleGameChoice"
          class="game-card"
        >
          <h2>Pong</h2>
        </GameCard>
        <GameCard
          backgroundImage="@/assets/tic-tac-toe.png"
          gameName="Tic-Tac-Toe"
          @game-chosen="handleGameChoice"
          class="game-card"
        >
          <h2>Tic-Tac-Toe</h2>
        </GameCard>
      </div>
    </div>
    <FooterOrganism />
  </div>
</template>

<script>
import HeaderOrganism from "@/components/header/navbar.vue";
import FooterOrganism from "@/components/footer.vue";
import GameCard from "@/components/game/GameChoice.vue";

export default {
  components: {
    HeaderOrganism,
    FooterOrganism,
    GameCard
  },
  methods: {
    handleGameChoice(gameName) {
      // Handle game choice logic here
      console.log(`${gameName} chosen!`);
      // Add your game navigation logic here
    }
  }
};
</script>

<style scoped>
.game-choice-page {
  text-align: center;
  color: white;
  background-color: #222;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.game-choice-content {
  margin: 50px auto;
  padding: 20px;
  max-width: 800px;
  color: white;
  font-size: 1rem;
  line-height: 1.6;
}

.game-cards-container {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 20px;
}

.game-card {
  width: calc(50% - 20px);
  max-width: 300px;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.game-card:hover {
  transform: scale(1.05);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}
</style>