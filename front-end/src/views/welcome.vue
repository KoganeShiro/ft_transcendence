<template>
  <div class="welcome-template">
    <HeaderOrganism />
    <div class="welcome-content">
      <TextAtom class="welcome-text">Welcome</TextAtom>
      <ButtonGroupMolecule class="button-group">
        <router-link to="/login" class="button-link">
          <ButtonAtom variant="primary">Login</ButtonAtom>
        </router-link>
        <router-link to="/register" class="button-link">
          <ButtonAtom variant="secondary">Register</ButtonAtom>
        </router-link>
        <!-- <ButtonAtom variant="ghost">Play as guest</ButtonAtom> -->
      </ButtonGroupMolecule>
    </div>
    <FooterOrganism />
  </div>
</template>

<script>
import HeaderOrganism from "@/components/header/navbar.vue";
import TextAtom from "@/components/atoms/Text.vue";
import ButtonAtom from "@/components/atoms/Button.vue";
import ButtonGroupMolecule from "@/components/atoms/ButtonGroup.vue";
import FooterOrganism from "@/components/footer.vue";

export default {
  components: {
    HeaderOrganism,
    TextAtom,
    ButtonAtom,
    ButtonGroupMolecule,
    FooterOrganism,
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
  margin-top: -100px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  flex-grow: 1;
}

.welcome-text {
  font-size: 5rem;
  font-weight: bold;
  margin-bottom: 150px;
}

.button-group {
  display: flex;
  gap: 15px;
}

.button-group >>> * {
  font-size: 30px;
  padding: 35px 100px;
  transition: transform 0.2s;
}

.button-group >>> *:hover {
  transform: scale(1.05);
}

.button-link {
  display: contents;
}

</style>