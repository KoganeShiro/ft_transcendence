<template>
  <div class="header-container">
    <header class="header">
      <router-link to="/" class="header-link">
        <h1>FT_TRANSCENDENCE</h1>
      </router-link>
      <button v-if="showBurgerMenu" class="menu-btn" @click="toggleMenu">
        <svg v-if="!isMenuVisible" width="30" height="30" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="burger-icon">
          <path d="M3 6.00092H21M3 12.0009H21M3 18.0009H21" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <svg v-else width="35" height="30" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="cross-icon">
          <path d="M6 6L18 18M6 18L18 6" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>
    </header>
    <Burger_menu v-if="showBurgerMenu" :class="{ active: isMenuVisible }" />
  </div>
</template>


<script>
import Burger_menu from "@/components/header/burger_menu.vue";

export default {
  components: {
    Burger_menu,
  },
  props: {
    showBurgerMenu: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      isMenuVisible: false,
    };
  },
  methods: {
    toggleMenu() {
      this.isMenuVisible = !this.isMenuVisible;
    },
  },
};
</script>


<style scoped>
.header-container {
  position: relative;
  margin-bottom: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #333;
  color: white;
  padding: 10px 20px;
  height: 50px;
}

.header-link {
  text-decoration: none;
  color: inherit;
}

.header-link h1 {
  font-size: 1.3rem;
}

.menu-btn {
  background: transparent;
  border: none;
  cursor: pointer;
  z-index: 1001;
}

.burger-icon,
.cross-icon {
  width: 30px;
  height: 30px;
  stroke: var(--icon-color, rgb(255, 255, 255));
  stroke-width: 2;
}

</style>
