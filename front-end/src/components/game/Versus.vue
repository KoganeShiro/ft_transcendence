<template>
    <div class="versus-container" v-if="show.value">
      <div class="versus-background">
        <div class="text">
          <h1>{{ opponentStatus.value }}</h1>
        </div>
        <div class="versus-content">
          <!-- Player 1 Avatar -->
          <div class="player">
            <AvatarAtom
              :imageUrl="player1.imageUrl"
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
  </template>

  
  <script>
  import { reactive, watch, onMounted } from 'vue';
  import AvatarAtom from '@/components/atoms/Avatar.vue';
  import defaultAvatar from '@/assets/searching.webp';
  import anotherAvatar from '@/assets/profile2.png';
  
  export default {
    components: {
      AvatarAtom,
    },
    props: {
      player1: {
        type: Object,
        required: true,
      },
      duration: {
        type: Number,
        default: 30,
      },
    },
    setup(props, { emit }) {
      const player2 = reactive({
        imageUrl: defaultAvatar,
        pseudo: 'Waiting for an opponent...',
        link: '',
      });
  
      const show = reactive({ value: true });
      const opponentStatus = reactive({ value: 'Waiting for an opponent...' });
  
      onMounted(() => {
        setTimeout(() => {
          player2.imageUrl = anotherAvatar;
          player2.pseudo = 'OpponentName';
          player2.link = 'https://opponent-profile.com';
        }, 2000);
      });
  
      watch(player2, (newVal) => {
        if (newVal.pseudo !== 'Waiting for an opponent...') {
          opponentStatus.value = 'Opponent found!';
          setTimeout(() => {
            show.value = false;
            emit('time-up');
          }, props.duration);
        }
      });
  
      return {
        player2,
        show,
        opponentStatus,
      };
    },
  };
  </script>
  
  <style scoped>
  @keyframes fadeIn {
    0% {
      opacity: 0;
      transform: scale(0.8);
    }
    100% {
      opacity: 1;
      transform: scale(1);
    }
  }
  
  @keyframes bounce {
    0%, 20%, 50%, 80%, 100% {
      transform: translateY(0);
    }
    40% {
      transform: translateY(-30px);
    }
    60% {
      transform: translateY(-15px);
    }
  }
  
  @keyframes slideIn {
    0% {
      opacity: 0;
      transform: translateX(-100%);
    }
    100% {
      opacity: 1;
      transform: translateX(0);
    }
  }
  
  @keyframes slideInReverse {
    0% {
      opacity: 0;
      transform: translateX(100%);
    }
    100% {
      opacity: 1;
      transform: translateX(0);
    }
  }
  
  .versus-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
    width: 100vw;
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 9999;
  }
  
  .versus-background {
    background-color: #222;
    padding: 100px;
    border-radius: 10px;
    box-shadow: 0 0 15px rgba(0, 0, 0, 0.5);
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
  
  @media (max-width: 768px) {
    .versus-content {
      flex-direction: column;
    }
    .versus-text h1 {
      font-size: 2rem;
    }
  }
  </style>