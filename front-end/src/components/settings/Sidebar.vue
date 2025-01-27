<template>
    <div class="sidebar-container">
      <div class="sidebar-arrow" @click="toggleSidebar" @touchstart="startDrag" @touchmove="drag" @touchend="endDrag">
        <span>&#9656;</span>
      </div>
      <div :class="['sidebar', { 'open': isOpen }]">
        <ButtonGroup class="sidebar-group-element">
          <ButtonAtom variant="ghost" @click="selectPage('Account')">Account</ButtonAtom>
          <ButtonAtom variant="ghost" @click="selectPage('Appearance')">Appearance</ButtonAtom>
          <ButtonAtom variant="ghost" @click="selectPage('Languages')">Languages</ButtonAtom>
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
        startX: 0,
        currentX: 0,
      };
    },
    methods: {
      toggleSidebar() {
        this.isOpen = !this.isOpen;
      },
      startDrag(e) {
        this.startX = e.touches[0].clientX;
        this.currentX = this.startX;
      },
      drag(e) {
        this.currentX = e.touches[0].clientX;
        const diff = this.currentX - this.startX;
        if (diff > 50) {
          this.isOpen = true;
        } else if (diff < -50) {
          this.isOpen = false;
        }
      },
      endDrag() {
        this.startX = 0;
        this.currentX = 0;
      },
      selectPage(page) {
        this.$emit('page-selected', page);
      },
    },
  };
  </script>
  
  <style scoped>
.sidebar-container {
  width: 150px;
  height: 200px;
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
  background-color: #3a3a3a;
  color: #fff;
  text-align: left;
  border-radius: 8px;
  transition: background-color 0.2s ease;
}

.sidebar-item:hover {
  background-color: #505050;
  cursor: pointer;
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
