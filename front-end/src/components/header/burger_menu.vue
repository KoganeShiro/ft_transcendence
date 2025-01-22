<template>
    <div :class="['burger-menu', { active: isActive }]">
      <ButtonGroupMolecule>
        <ButtonAtom variant="menu">Play</ButtonAtom>
        <ButtonAtom variant="menu">Profile</ButtonAtom>
        <ButtonAtom variant="menu">Settings</ButtonAtom>
        <ButtonAtom variant="menu">Log out</ButtonAtom>
        <ButtonAtom variant="menu">Credits</ButtonAtom>
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
    padding: 20px;
    background-color: #333;
    color: #ffffff;
    overflow-y: auto;
    transition: transform 0.3s ease-in-out;
    transform: translateX(100%);
    border-radius: 10px;
  }
  
  .burger-menu.active {
    transform: translateX(0);
  }
  .button-group > * {
    display: flex;
    flex-direction: column;
    font-size: 20px;
    padding: 15px 50px;
  }
  .button-group > *:hover {
    transform: scale(1.05);
  }
  </style>