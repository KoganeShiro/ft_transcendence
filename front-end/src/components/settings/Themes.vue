<template>
    <button 
      class="theme-button" 
      :class="{ active: isActive }" 
      @click="selectTheme"
    >
      <img :src="imageUrl" :alt="themeName" class="theme-image" />
      <span class="theme-name">{{ themeName }}</span>
    </button>
  </template>
  
  <script>
  export default {
    name: "ThemeButton",
    props: {
      themeName: {
        type: String,
        required: true
      },
      imageUrl: {
        type: String,
        required: true
      },
      isActive: {
        type: Boolean,
        default: false
      }
    },
    methods: {
      selectTheme() {
        this.$emit("select", this.themeName);
      }
    }
  };
  </script>
  
  <style scoped>
  .theme-button {
    display: flex;
    flex-direction: column;
    align-items: center;
    background: var(--text-box-color);
    border: none;
    border-radius: 8px;
    padding: 10px;
    margin: 10px;
    cursor: pointer;
    transition: transform 0.2s ease, background 0.3s ease;
  }
  .theme-button:hover {
    transform: scale(1.05);
    background: var(--text-box-color);
  }
  .theme-button.active {
    background: var(--sidebar-color);
    border: 2px solid #007bff;
    transform: scale(1.09);
  }
  .theme-image {
    width: 100px;
    height: 100px;
    border-radius: 8px;
    object-fit: cover;
    margin-bottom: 10px;
  }
  .theme-name {
    font-size: 1rem;
    color: var(--text-color);
    font-weight: bold;
  }
  </style>
  