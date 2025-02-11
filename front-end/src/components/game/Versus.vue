<template>
  <!-- Use a transition wrapper for a smooth fade-out -->
  <transition name="fade" @after-leave="emitTimeUp">
    <div class="versus-container" v-if="show">
      <div class="versus-background">
        <div class="text">
          <h1>{{ opponentStatus }}</h1>
        </div>
        <div class="versus-content">
          <!-- Player 1 Avatar -->
          <div class="player">
            <AvatarAtom
              :pseudo="player1.pseudo"
              :showPseudo="true"
              pseudoPosition="bottom"
              :link="player1.link"
              class="animate-avatar"
            />
          </div>
          <!-- VS Text -->
          <div class="versus-text">
            <h1>VS</h1>
          </div>
          <!-- Player 2 Avatar -->
          <div class="player">
            <AvatarAtom
              :imageUrl="player2.imageUrl"
              :pseudo="player2.pseudo"
              :showPseudo="true"
              pseudoPosition="bottom"
              :link="player2.link"
              class="animate-avatar"
            />
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
import { ref, watch, onMounted } from 'vue';
import AvatarAtom from '@/components/atoms/Avatar.vue';
import defaultAvatar from '@/assets/searching.webp';
import anotherAvatar from '@/assets/profile2.png';

export default {
  name: 'Versus',
  components: {
    AvatarAtom,
  },
  props: {
    player1: {
      type: Object,
      default: () => ({
        imageUrl: 'https://via.placeholder.com/100',
        pseudo: 'Player 1',
        link: '#'
      })
    },
    // Duration in seconds before fading out after an opponent is found
    duration: {
      type: Number,
      default: 3,
    },
  },
  setup(props, { emit }) {
    // Control the overlay visibility
    const show = ref(true);
    
    // Reactive status message
    const opponentStatus = ref('Waiting for an opponent...');
    
    // Create a reactive object for player2 with default values.
    const player2 = ref({
      imageUrl: defaultAvatar,
      pseudo: 'Waiting for an opponent...',
      link: '',
    });
    
    onMounted(() => {
      // Simulate finding an opponent after 2 seconds.
      setTimeout(() => {
        player2.value.imageUrl = anotherAvatar;
        player2.value.pseudo = 'OpponentName';
      }, 3000);
    });
    
    // Watch for changes in player2 pseudo.
    watch(
      () => player2.value.pseudo,
      (newVal) => {
        if (newVal !== 'Waiting for an opponent...') {
          opponentStatus.value = 'Opponent found!';
          // Wait for props.duration seconds before starting the fade-out transition.
          setTimeout(() => {
            show.value = false; // This will trigger the fade transition.
          }, props.duration * 1000);
        }
      }
    );
    
    // When the fade transition is complete, emit an event so the parent can hide the overlay.
    const emitTimeUp = () => {
      emit('time-up');
    };

    return {
      show,
      opponentStatus,
      player2,
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
