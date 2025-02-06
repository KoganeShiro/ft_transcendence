<template>
  <div class="credit-page">
    <HeaderOrganism />

    <div class="credit-content">
      <h1>{{ $t("credits") }}</h1>
      <p class="credit-text">
        {{ $t("creditsText") }}
      </p>
      <div class="avatar-container">
        <AvatarAtom
          imageUrl="https://avatars.githubusercontent.com/u/126095786?s=96&v=4"
          pseudo="KoganeShiro"
          link="https://github.com/KoganeShiro"
          class="ks" />
        <AvatarAtom
          imageUrl="https://avatars.githubusercontent.com/u/115719789?v=4"
          pseudo="Lapinew"
          link="https://github.com/Lapinew"
          class="dl" />
        <AvatarAtom
          imageUrl="https://avatars.githubusercontent.com/u/138602095?v=4"
          pseudo="gkubina"
          link="https://github.com/gkubina"
          class="gk" />
      </div>
      <div class="github">
        <a href="https://github.com/KoganeShiro/ft_transcendence" target="_blank" rel="noopener noreferrer">
          {{ $t("github") }}
          <span class="stars">
            <span class="star">&#9733;</span>
            <span class="star">&#9733;</span>
            <span class="star">&#9733;</span>
          </span>
        </a>
      </div>
    </div>

    <FooterOrganism />
  </div>
</template>

<script>
import HeaderOrganism from "@/components/header/navbar.vue";
import FooterOrganism from "@/components/footer.vue";
import { useLanguage } from '@/components/useLanguage.js';
import AvatarAtom from "@/components/atoms/Avatar.vue";

export default {
  components: {
    HeaderOrganism,
    FooterOrganism,
    AvatarAtom
  },
  setup() {
    const { changeLanguage } = useLanguage();
    return {
      changeLanguage
    };
  },
};
</script>

<style scoped>
.credit-page {
  text-align: center;
  color: var(--text-color);
  background-color: var(--background-color);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.credit-content {
  text-align: center;
  line-height: 1.6;
}

.avatar-container {
  margin-top: 50px;
  display: flex;
  justify-content: center;
  gap: 50px;
  flex-wrap: wrap;
  margin-bottom: 50px;
}

.github {
  font-weight: 700;
  font-size: 1.2rem;
  position: relative;
  display: inline-block;
  margin-top: 50px;
}

.github a {
  color: var(--text-color);
  text-decoration: none;
  display: inline-block;
  transition: transform 0.3s ease, color 0.3s ease;
}

.github a .stars {
  position: absolute;
  top: -30px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 5px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.github a:hover {
  transform: translateY(-10px);
  color: var(--text-color);
}

.github a:hover .stars {
  opacity: 1;
}

.github a .star {
  font-size: 1.2rem;
  animation: star-float 1s infinite alternate;
}

.github a .star:nth-child(1) {
  animation-delay: 0.1s;
}

.github a .star:nth-child(2) {
  animation-delay: 0.2s;
}

.github a .star:nth-child(3) {
  animation-delay: 0.3s;
}

@keyframes star-float {
  from {
    transform: translateY(0);
  }
  to {
    transform: translateY(-10px);
  }
}

@keyframes spin {
  from {
    transform: rotateY(0deg);
  }
  to {
    transform: rotateY(360deg);
  }
}

@keyframes move-left-right {
  from {
    transform: translateX(0);
  }
  to {
    transform: translateX(-10px);
  }
}

@media (max-width: 600px) {
  .avatar-container {
    flex-direction: column;
    align-items: center;
    margin-bottom: 30px;
  }
  .github {
    margin-top: 15px;
    margin-bottom: 10px;
  }

  .ks, .dl, .gk {
    animation: spin 2s linear forwards;
  }

  .ks {
    animation-delay: 0s, 5s;
  }

  .dl {
    animation-delay: 1s, 6s;
  }

  .gk {
    animation-delay: 2s, 7s;
  }

  .github a {
    animation: move-left-right 2s infinite alternate ease-in-out;
  }

  @keyframes move-left-right {
    from {
      transform: translateX(0);
    }
    to {
      transform: translateX(10px);
    }
  }

  @keyframes spin {
    from {
      transform: rotateY(0deg);
    }
    to {
      transform: rotateY(360deg);
    }
  }
}
</style>