<template>
  <div class="game-choice-page">
    <HeaderOrganism />
    <div class="game-choice-content">
      <h1>{{ $t("game-choice") }}</h1>
      <div class="game-cards-container">
        <div class="game-card" v-for="(card, index) in cards" :key="index">
          <GameCard
            class="card"
            :backgroundImage="card.image"
            :gameName="card.name"
            @game-chosen="handleGameChoice(card.name)"
          >
            <div class="card-overlay">
              <span class="game-name">{{ card.name }}</span>
            </div>
          </GameCard>
        </div>
      </div>
    </div>
    <FooterOrganism />
  </div>
</template>

<script>
import { useRouter } from "vue-router";
import HeaderOrganism from "@/components/header/navbar.vue";
import FooterOrganism from "@/components/footer.vue";
import GameCard from "@/components/game/GameChoice.vue";
import pongImage from "@/assets/pong.png";
import ticTacToeImage from "@/assets/tic-tac-toe.png";

export default {
  components: {
    HeaderOrganism,
    FooterOrganism,
    GameCard,
  },
  data() {
    return {
      pongImage,
      ticTacToeImage,
      cards: [
        { image: pongImage, name: "Pong" },
        { image: ticTacToeImage, name: "Tic Tac Toe" },
      ],
    };
  },
  setup() {
    const router = useRouter();

    const handleGameChoice = (gameName) => {
      router.push({ path: "/select-mode", query: { game: gameName } }); // Pass game name
    };

    return { handleGameChoice };
  },
};
</script>

<style scoped>
.game-choice-page {
  text-align: center;
  color: white;
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
  flex-direction: row;
  justify-content: center;
  flex-wrap: wrap;
  gap: 20px;
}

.game-card {
  width: 500px;
  height: 250px;
  cursor: pointer;
  position: relative;
  background-color: rgba(0, 0, 0, 0.6);
  border-radius: 15px;
}

.game-card .card-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.5);
  color: white;
  font-size: 1.5rem;
  font-weight: bold;
  text-shadow: 1px 1px 2px black;
  border-radius: 15px;
}

@media (max-width: 600px) {
  .game-cards-container {
    flex-direction: column;
    align-items: center;
  }
  .game-card {
    width: 300px;
    height: 150px;
  }
}
</style>