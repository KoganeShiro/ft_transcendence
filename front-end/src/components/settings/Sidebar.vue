<template>
  <div class="sidebar-container" :class="{ open: isOpen }">
    <div class="sidebar-arrow" @click="toggleSidebar">
      <span v-if="!isOpen">&#9656;</span>
      <span v-else>&#9666;</span>
    </div>
    <div class="sidebar">
      <ButtonGroup class="sidebar-group-element">
        <ButtonAtom
          variant="ghost"
          class="sidebar-item"
          :class="{ active: selectedPage === 'Account' }"
          @click="selectPage('Account')"
        >
          {{ $t('account') }}
        </ButtonAtom>
        <ButtonAtom
          variant="ghost"
          class="sidebar-item"
          :class="{ active: selectedPage === 'Appearance' }"
          @click="selectPage('Appearance')"
        >
          {{ $t('appearance') }}
        </ButtonAtom>
        <ButtonAtom
          variant="ghost"
          class="sidebar-item"
          :class="{ active: selectedPage === 'Languages' }"
          @click="selectPage('Languages')"
        >
          {{ $t('language') }}
        </ButtonAtom>
      </ButtonGroup>
    </div>
  </div>
</template>

<script>
import ButtonGroup from "@/components/atoms/ButtonGroup.vue";
import ButtonAtom from "@/components/atoms/Button.vue";

export default {
  name: "Sidebar",
  components: {
    ButtonGroup,
    ButtonAtom,
  },
  data() {
    return {
      isOpen: false,
      selectedPage: "Account", // Default active page
    };
  },
  methods: {
    toggleSidebar() {
      this.isOpen = !this.isOpen;
    },
    selectPage(page) {
      this.selectedPage = page;
      this.$emit("page-selected", page);
      // On mobile, hide the sidebar after selection.
      this.isOpen = false;
    },
  },
};
</script>

<style scoped>
.sidebar-container {
  height: 550px;
  background-color: #2c2c2c;
  color: #fff;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  padding: 20px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  font-size: 1.5rem;
  position: relative;
}

/* Sidebar arrow is hidden on desktop by default */
.sidebar-arrow {
  margin-top: 100px;
  position: absolute;
  right: -25px;
  background-color: #333;
  color: white;
  padding: 10px 5px;
  border-radius: 0 5px 5px 0;
  cursor: pointer;
  display: none;
}

.sidebar {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.sidebar-group-element {
  width: 100%;
}

.sidebar-item {
  display: block;
  width: 100%;
  padding: 10px 20px;
  margin-bottom: 10px;
  color: #fff;
  text-align: left;
  border-radius: 8px;
  transition: background-color 0.2s ease, transform 0.2s ease;
}

.sidebar-item:hover,
.sidebar-item.active {
  background-color: #505050;
  transform: scale(1.05);
}

/* Mobile Styles */
@media (max-width: 668px) {
  .sidebar-container {
    margin-top: 100px;
    position: fixed;
    top: 0;
    left: 0;
    z-index: 1000;
    transform: translateX(-100%);
    transition: transform 0.3s ease-in-out;
  }
  .sidebar-container.open {
    transform: translateX(0);
  }
  .sidebar-arrow {
    display: block;
  }
}
</style>
