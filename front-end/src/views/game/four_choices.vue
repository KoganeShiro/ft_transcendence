<template>
    <div class="game-mode-page">
      <HeaderOrganism />
  
      <div class="game-mode-content">
        <h1>{{ $t("game-mode") }}</h1>
        <GameCards 
          backgroundImage="@/assets/pong.png"
          class="pong"/>
        <GameCards class="tic-tac-toe"/>
      </div>
      <FooterOrganism />
    </div>
  </template>
  
  <script>
  import HeaderOrganism from "@/components/header/navbar.vue";
  import FooterOrganism from "@/components/footer.vue";
  import GameCards from "@/components/game/GameChoice.vue";
  
  export default {
    components: {
      HeaderOrganism,
      FooterOrganism,
      GameCards
    },
    methods: {
    handleGameChoice() {
      // Handle game choice logic here
      console.log('Game chosen!');
    },
  },
  };
  </script>


<style scoped>
.game-mode-page {
  text-align: center;
  color: white;
  background-color: #222;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.game-mode-content {
  margin: 50px auto;
  padding: 20px;
  max-width: 800px;
  color: white;
  font-size: 1rem;
  line-height: 1.6;
}
</style>