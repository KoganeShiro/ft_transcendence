<template>
  <div class="game-mode-page">
    <HeaderOrganism />

    <div class="game-mode-content">
      <div class="h1">
        <h1>{{ $t("select-mode") }} {{ gameName }}</h1>
      </div>
      <div class="game-cards-container">
        <div class="game-card" v-for="(card, index) in cards" :key="index">
          <GameCard
            class="card"
            :backgroundImage="card.image"
            :gameName="card.name"
            @game-chosen="handleModeChoice(card.mode)"
          >
            <div class="card-overlay">
              <span class="game-name">{{ card.name }}</span>
            </div>
          </GameCard>
        </div>
      </div>
    </div>

    <button class="back-button" @click="goBack">{{ $t("select-back") }}</button>

    <FooterOrganism />
  </div>
</template>

<script>
import { useRouter, useRoute } from "vue-router";
import { useI18n } from 'vue-i18n';
import HeaderOrganism from "@/components/header/navbar.vue";
import FooterOrganism from "@/components/footer.vue";
import GameCard from "@/components/game/GameChoice.vue";
import Solo from "@/assets/solo.png";
import Remote from "@/assets/remote.png";
import Local from "@/assets/local.png";
import Tournament from "@/assets/tournament.svg";

export default {
  components: {
    HeaderOrganism,
    FooterOrganism,
    GameCard,
  },
  setup() {
    const { t } = useI18n();
    const router = useRouter();
    const route = useRoute();
    const gameName = route.query.game || "Game";

    const handleModeChoice = (mode) => {
      if (gameName) {
        router.push(`/${gameName.toLowerCase()}/${mode}`);
      }
    };

    const goBack = () => {
      router.push("/game-choice");
    };

    const cards = [
      { image: Solo, name: t('solo'), mode: "solo" },
      { image: Remote, name: t('multi-remote'), mode: "remote" },
      { image: Local, name: t('multi-local'), mode: "local" },
      { image: Tournament, name: t('tournament'), mode: "tournament" },
    ];

    return { gameName, handleModeChoice, goBack, cards };
  },
};
</script>

<style scoped>
.h1 {
  text-align: center;
  margin-bottom: 50px;
}

.game-mode-page {
  text-align: center;
  color: white;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.game-mode-content {
  margin: 50px auto;
  max-width: 800px;
  color: white;
  font-size: 1rem;
  line-height: 1.6;
}

.game-cards-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px;
}

.first-row,
.second-row {
  display: flex;
  justify-content: center;
  gap: 20px;
}

.back-button {
  margin-top: 20px;
  padding: 10px 20px;
  font-size: 1rem;
  background: #ff5757;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 10px;
  transition: 0.3s ease;
  font-weight: bold;
  width: 200px;
  margin-left: 60%;
  margin-bottom: 20px;
}

.game-card {
  width: 350px;
  height: 200px;
  cursor: pointer;
  position: relative;
  background-color: rgba(0, 0, 0, 0.6);
  border-radius: 12px;
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
  border-radius: 12px;
}

.back-button:hover {
  background: #ff1c1c;
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
  .back-button {
    margin-left: 50%;
  }
}
</style>