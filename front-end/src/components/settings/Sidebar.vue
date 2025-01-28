<template>
  <div class="sidebar-container">
    <div class="sidebar-arrow" @click="toggleSidebar">
      <span>&#9656;</span>
    </div>
    <div :class="['sidebar', { open: isOpen }]">
      <ButtonGroup class="sidebar-group-element">
        <ButtonAtom
          variant="ghost"
          class="sidebar-item"
          :class="{ active: selectedPage === 'Account' }"
          @click="selectPage('Account')"
        >
          {{ $t("account") }}
        </ButtonAtom>
        <ButtonAtom
          variant="ghost"
          class="sidebar-item"
          :class="{ active: selectedPage === 'Appearance' }"
          @click="selectPage('Appearance')"
        >
          {{ $t("appearance") }}
        </ButtonAtom>
        <ButtonAtom
          variant="ghost"
          class="sidebar-item"
          :class="{ active: selectedPage === 'Languages' }"
          @click="selectPage('Languages')"
        >
          {{ $t("language") }}
        </ButtonAtom>
      </ButtonGroup>
    </div>
  </div>
</template>

<script>
import ButtonGroup from "@/components/atoms/ButtonGroup.vue";
import ButtonAtom from "@/components/atoms/Button.vue";

export default {
  components: {
    ButtonGroup,
    ButtonAtom,
  },
  name: "Sidebar",
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
    },
  },
};
</script>

<style scoped>
.sidebar-container {
  width: 200px;
  height: 550px;
  background-color: #2c2c2c;
  color: #fff;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  padding: 20px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  font-size: 1.5rem;
}

.sidebar-arrow {
    position: absolute;
    top: 50%;
    right: -20px;
    transform: translateY(-50%);
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

.sidebar-group {
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
  transition: background-color 0.2s ease;
}

.sidebar-item:hover,
.sidebar-item.active {
  background-color: #505050;
  transform: scale(1.05);
}

@media (max-width: 668px) {
  .sidebar-container {
    position: fixed;
    top: 0;
    left: 0;
    height: 100vh;
    z-index: 1000;
  }

  .sidebar-arrow {
    display: block;
  }

  .sidebar {
    transform: translateX(-100%);
    transition: transform 0.3s ease-in-out;
  }

  .sidebar.open {
    transform: translateX(0);
  }
}

</style>
