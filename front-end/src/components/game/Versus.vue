<template>
  <transition name="fade" @after-leave="emitTimeUp">
    <div class="versus-container" v-if="show">
      <div class="versus-background">
        <div class="text">
          <h1>{{ opponentStatus }}</h1>
        </div>
        <div class="versus-content">
          <!-- Player 1 Avatar using the locally managed user profile -->
          <div class="player">
            <AvatarAtom
              :pseudo="localPlayer1.pseudo"
              :imageUrl="localPlayer1.imageUrl"
              :showPseudo="true"
              pseudoPosition="bottom"
              class="animate-avatar"
            />
          </div>
          <!-- VS Text -->
          <div class="versus-text">
            <h1>VS</h1>
          </div>
          <!-- Player 2 Avatar (opponent) -->
          <div class="player">
            <AvatarAtom
              :imageUrl="opponent.imageUrl"
              :pseudo="opponent.pseudo"
              :showPseudo="true"
              pseudoPosition="bottom"
              class="animate-avatar"
            />
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
import { ref, onMounted, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import AvatarAtom from '@/components/atoms/Avatar.vue';
import defaultAvatar from '@/assets/searching.webp';
import guestAvatar from '@/assets/profile2.png';
import API from '@/api.js';

export default {
  name: 'Versus',
  components: { AvatarAtom },
  props: {
    player1: {
      type: Object,
      default: () => ({
        pseudo: 'Player 1',
        imageUrl: defaultAvatar,
      }),
    },
    player2: {
      type: Object,
      default: () => ({
        pseudo: 'Opponent',
        imageUrl: defaultAvatar,
      }),
    },
    duration: {
      type: Number,
      default: 3,
    },
  },
  setup(props, { emit }) {
    const show = ref(true);
    const { t } = useI18n();
    const opponentStatus = ref(t("search-opponent"));

    // Local reactive copy for player1 info
    const localPlayer1 = ref({
      pseudo: props.player1.pseudo,
      imageUrl: props.player1.imageUrl,
      link: props.player1.link,
    });

    // Local opponent object we want to keep in sync with props.player2
    const opponent = ref({
      pseudo: 'loading...',
      imageUrl: defaultAvatar,
      link: ''
    });

    // Function to update the opponent info
    function updateOpponent(playerData) {
      opponent.value.pseudo = playerData.pseudo || 'Opponent';
      opponent.value.link = playerData.link;
      opponent.value.imageUrl = playerData.imageUrl || guestAvatar;
      
      // Optionally fetch updated profile info if needed
      if (opponent.value.pseudo && opponent.value.pseudo !== 'AI' && opponent.value.pseudo !== 'Guest') {
        API.get(`/api/profile/${playerData.pseudo}`)
          .then(response => {
            const { username, cover_photo } = response.data;
            opponent.value.pseudo = username;
            opponent.value.imageUrl = cover_photo;
          })
          .catch(error => {
            console.error("Error fetching player data:", error);
          });
      }
      opponentStatus.value = 'Opponent found!';
      setTimeout(() => {
        show.value = false;
      }, props.duration * 1000);
    }

    // Initial fetch for localPlayer1
    onMounted(async () => {
      try {
        const response = await API.get('/api/profile/');
        const { username, cover_photo } = response.data;
        localPlayer1.value.pseudo = username;
        localPlayer1.value.imageUrl = cover_photo;
      } catch (error) {
        console.error("Error fetching player data:", error);
      }
      // Initialize opponent info from prop on mount
      updateOpponent(props.player2);
    });

    const emitTimeUp = () => {
      emit('time-up');
    };

    return {
      show,
      opponentStatus,
      localPlayer1,
      opponent,
      emitTimeUp,
    };
  },
};
</script>



<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 1s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

.versus-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  color: var(--text-color);
}

.versus-background {
  background-color: var(--text-box-color, rgba(0,0,0,0.8));
  padding: 100px;
  border-radius: 10px;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.8);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.text {
  text-align: center;
  width: 100%;
  animation: fadeIn 1s ease-in-out;
}

.versus-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 50px;
  margin-top: 20px;
}

.player {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.versus-text h1 {
  font-size: 3rem;
  animation: bounce 2s infinite;
}

.animate-avatar {
  animation: fadeIn 1s ease-in-out, slideIn 1s ease-in-out;
}

.animate-avatar:nth-child(1) {
  animation: fadeIn 1s ease-in-out, slideInReverse 1s ease-in-out;
}

@keyframes fadeIn {
  0% { opacity: 0; transform: scale(0.8); }
  100% { opacity: 1; transform: scale(1); }
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-30px); }
  60% { transform: translateY(-15px); }
}

@keyframes slideIn {
  0% { opacity: 0; transform: translateX(-100%); }
  100% { opacity: 1; transform: translateX(0); }
}

@keyframes slideInReverse {
  0% { opacity: 0; transform: translateX(100%); }
  100% { opacity: 1; transform: translateX(0); }
}

@media (max-width: 768px) {
  .versus-content {
    flex-direction: column;
  }
  .versus-text h1 {
    font-size: 2rem;
  }
}
</style>