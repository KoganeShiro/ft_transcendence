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
import { useRouter } from "vue-router";
import { useI18n } from "vue-i18n";
import HeaderOrganism from "@/components/header/navbar.vue";
import FooterOrganism from "@/components/footer.vue";
import GameCard from "@/components/game/GameChoice.vue";
import { computed } from 'vue';
import { useStore } from 'vuex';

const getThemeImage = (mode, theme) => {
  try {
    if (theme === 'teapot') {
      theme = 'volcano';
    }
    return new URL(
      `../../assets/custom-icon/${mode}-${theme}.png`,
      import.meta.url
    ).href;
  } catch (error) {
    console.error(`Error loading image for ${mode} in ${theme} theme:`, error);
    return fallbackImage;
  }
};


export default {
  name: "PongModeSelection",
  components: {
    HeaderOrganism,
    FooterOrganism,
    GameCard,
  },
  setup() {
    const { t } = useI18n();
    const router = useRouter();
    const store = useStore();
    const currentTheme = computed(() => store.state.theme || 'moon');

    const gameName = "Pong";

    const handleModeChoice = (mode) => {
      router.push(`/pong/${mode}`);
    };

    const goBack = () => {
      router.push("/game-choice");
    };

    const cards = computed(() => [
      { image: getThemeImage('solo', currentTheme.value), name: t("solo"), mode: "solo" },
      { image: getThemeImage('remote', currentTheme.value), name: t("multi-remote"), mode: "remote" },
      { image: getThemeImage('local', currentTheme.value), name: t("multi-local"), mode: "local" },
      { image: getThemeImage('tournament', currentTheme.value), name: t("tournament"), mode: "tournament" },
      { image: getThemeImage('multi', currentTheme.value), name: t("more-than-2"), mode: "multiplayer" },
    ]);

    console.log(cards);


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

.back-button {
  margin-top: 20px;
  padding: 10px 20px;
  font-size: 1rem;
  /* background: #ff5757; */
  background: var(--back);
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
  background: #db1919d0;
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
