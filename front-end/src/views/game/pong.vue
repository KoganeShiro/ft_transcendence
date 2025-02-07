<template>
  <div class="template">
    <HeaderOrganism />
    <div class="heading-container" :class="{'mobile-hide': mode === 'tournament'}">
      <!-- <h1>Pong - {{ modeDisplay }} Mode</h1> -->
    </div>
    <div class="game-container">
      <!-- Dynamically render the component based on the mode -->
      <component :is="currentComponent" :mode="mode" />
    </div>
    <!--
          Make a component for each mode
          Front for solo
            ===+> have the versus component with the AI in the front
          Front random and friend versus (remote)
            ===+> have the versus component sending
                    information to the backend (who is the opponent)
         Front for local versus
            ===+> have the versus component sending
                    information to the backend (guest and host match)
         Front for tournament
            ===+> Call create tournament component, create/join logic
                    have the versus component sending
                    information to the backend (guest and host match) 
         Front for 4 player mode
            ===+> have (a new ?) versus component sending
                    information to the backend
    -->
    <FooterOrganism />
  </div>
</template>

<script>
import { useRoute } from "vue-router";
import { computed } from "vue";

// Import your different game components
import PongSolo from "@/components/game/pongFront/PongSolo.vue";
import PongRemote from "@/components/game/pongFront/PongRemote.vue";
import PongFourPlayer from "@/components/game/pongFront/PongMulti.vue";
import PongGame from "@/components/game/PongGame.vue";
import PongLocal from "@/components/game/pongFront/PongLocal.vue";
import PongTournament from "@/components/game/pongFront/PongTournament.vue";
import PongWithFriend from "@/components/game/pongFront/PongWithFriend.vue";

import HeaderOrganism from "@/components/header/navbar.vue";
import FooterOrganism from "@/components/footer.vue";

export default {
  name: "PongGamePage",
  components: {
    HeaderOrganism,
    FooterOrganism,
    PongSolo,
    PongRemote,
    PongFourPlayer,
    PongLocal,
    PongTournament,
    PongWithFriend,
    PongGame,
  },
  setup() {
    const route = useRoute();

    // Get the mode from the route params (e.g. /pong/solo, /pong/remote, /pong/4player)
    const mode = computed(() => route.params.mode || 'solo');

    // Create a user-friendly display name for the mode.
    const modeDisplay = computed(() => {
      if (mode.value === 'multiplayer') return '4 Player';
      if (mode.value === 'remote') return 'Remote';
      if (mode.value === 'solo') return 'Solo';
      if (mode.value === 'local') return 'Local';
      if (mode.value === 'tournament') return 'Tournament';
      if (mode.value === 'with-friend') return 'With Friend';
      // Fallback
      return mode.value.charAt(0).toUpperCase() + mode.value.slice(1);
    });
    console.log(mode.value);
    // Decide which component to render based on the mode.
    const currentComponent = computed(() => {
      switch (mode.value) {
        case 'solo':
          return PongSolo;
        case 'remote':
          return PongRemote;
        case 'local':
          return PongLocal;
        case 'multiplayer':
          return PongFourPlayer;
        case 'tournament':
          return PongTournament;
        case 'withFriend':
          return PongWithFriend;

        default:
          return PongGame;
      }
    });

    return {
      mode,
      modeDisplay,
      currentComponent,
    };
  },
};
</script>

<style scoped>
.pong-page {
  /* min-height: 73vh; */
  display: flex;
  flex-direction: column;
}

.heading-container {
  text-align: center;
}

.heading-container h1 {
  font-size: 2rem;
  margin: 0;
}

.game-container {
  flex: 1;
  padding: 10px;
  border-radius: 8px;
  background-color: #1e1e1e;
}

/* Example mobile hide class */
.mobile-hide {
  display: none;
}
</style>
