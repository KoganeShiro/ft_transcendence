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
              :pseudo="player1.name"
              :imageUrl="player1.imageUrl"
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
              :pseudo="player2.name"
              :imageUrl="player2.imageUrl"
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
import { ref, onMounted } from 'vue';
import { useI18n } from 'vue-i18n';
import AvatarAtom from '@/components/atoms/Avatar.vue';
import defaultAvatar from '@/assets/profile.png';
import guestAvatar from '@/assets/profile2.png';

export default {
  name: 'Versus',
  components: { AvatarAtom },
  props: {
    player1: {
      type: Object,
      default: () => ({
        name: '',
        imageUrl: defaultAvatar,
      }),
    },
    player2: {
      type: Object,
      default: () => ({
        name: '',
        imageUrl: guestAvatar,
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
    const opponentStatus = ref(t("opponent_found"));
    // console.log("Player 1:", props.player1);
    // console.log("Player 2:", props.player2);

    const emitTimeUp = () => {
      emit('time-up');
    };

    // Start a timer on mount. After `duration` seconds, hide the component.
    onMounted(() => {
      setTimeout(() => {
        show.value = false;
      }, props.duration * 1000);
    });

    return {
      show,
      opponentStatus,
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