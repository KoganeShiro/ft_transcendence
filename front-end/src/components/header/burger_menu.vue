<template>
    <div :class="['burger-menu', { active: isActive }]">
      <ButtonGroupMolecule class="menu-btn-group">
        <router-link to="/game-choice" class="button-link">
          <ButtonAtom variant="menu">{{ $t("play") }}</ButtonAtom>
        </router-link>
        <router-link to="/profile" class="button-link">
          <ButtonAtom variant="menu">{{ $t("profile") }}</ButtonAtom>
        </router-link>
        <router-link to="/settings" class="button-link">
          <ButtonAtom variant="menu">{{ $t("settings") }}</ButtonAtom>
        </router-link>
        <router-link to="/logout" class="button-link">
          <ButtonAtom variant="menu">{{ $t("logout") }}</ButtonAtom>
        </router-link>
        <router-link to="/credits" class="button-link">
          <ButtonAtom variant="menu">{{ $t("credits") }}</ButtonAtom>
        </router-link>
    </ButtonGroupMolecule>

    </div>
  </template>
  
  <script>
import ButtonAtom from "@/components/atoms/Button.vue";
import ButtonGroupMolecule from "@/components/atoms/ButtonGroup.vue";
import TextAtom from "@/components/atoms/Text.vue";

  export default {
    components: {
      TextAtom,
      ButtonAtom,
      ButtonGroupMolecule,
    },
    name: 'BurgerMenu',
    props: {
      isActive: {
        type: Boolean,
        default: false,
      },
    },
  };
  </script>
  
  <style scoped>
  .burger-menu {
    position: fixed;
    top: 50px;
    right: 0;
    bottom: 0;
    width: 270px;
    height: 300px;
    background-color: #333;
    color: #ffffff;
    overflow-y: auto;
    transition: transform 0.3s ease-in-out;
    transform: translateX(100%);
    border-radius: 10px;
    z-index: 1000;
  }
  
  .burger-menu.active {
    transform: translateX(0);
  }
  .menu-btn-group :deep(*) {
    display: flex;
    flex-direction: column;
    font-size: 20px;
    padding: 15px 0px;
  }

  .button-link {
    display: contents;
  }

  </style>