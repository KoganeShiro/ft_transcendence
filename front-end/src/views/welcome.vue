<template>
  <div class="welcome-template">
    <HeaderOrganism />

    <div class="welcome-content">
      <TextAtom className="welcome-text">Welcome</TextAtom>

      <ButtonGroupMolecule>
        <ButtonAtom variant="primary">Login</ButtonAtom>
        <ButtonAtom variant="secondary">Register</ButtonAtom>
        <ButtonAtom variant="ghost">Play as guest</ButtonAtom>
      </ButtonGroupMolecule>
    </div>

    <FooterOrganism />
  </div>
</template>

<script>
import HeaderOrganism from "@/components/header/navbar.vue";
import TextAtom from "@/components/atoms/Text.vue";
import ButtonAtom from "@/components/atoms/Button.vue";
import ButtonGroupMolecule from "@/components/molecules/ButtonGroup.vue";

export default {
  components: {
    HeaderOrganism,
    TextAtom,
    ButtonAtom,
    ButtonGroupMolecule,
  },
};
</script>

<style scoped>
.welcome-template {
  text-align: center;
  color: white;
  background-color: #222;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.welcome-content {
  margin-top: 50px;
}

.welcome-text {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 20px;
}

.footer {
  background-color: #333;
  padding: 10px 20px;
  color: white;
  font-size: 0.9rem;
}
</style>
