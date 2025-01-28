<template>
  <div class="template">
    <HeaderOrganism :showBurgerMenu="false"/>
    <div class="welcome-content">
      <TextAtom class="welcome-text">{{ $t("welcome") }}</TextAtom>
      <ButtonGroupMolecule class="button-group">
        <router-link to="/login" class="button-link">
          <ButtonAtom variant="primary"> {{ $t("login") }} </ButtonAtom>
        </router-link>
        <router-link to="/register" class="button-link">
          <ButtonAtom variant="secondary">{{ $t("register") }}</ButtonAtom>
        </router-link>
        <!-- <ButtonAtom variant="ghost">Play as guest</ButtonAtom> -->
      </ButtonGroupMolecule>
    </div>
    <FooterOrganism />
  </div>
</template>

<script>
import HeaderOrganism from "@/components/header/navbar.vue";
import FooterOrganism from "@/components/footer.vue";
import TextAtom from "@/components/atoms/Text.vue";
import ButtonAtom from "@/components/atoms/Button.vue";
import ButtonGroupMolecule from "@/components/atoms/ButtonGroup.vue";
import { useLanguage } from '@/components/useLanguage.js';

export default {
  components: {
    HeaderOrganism,
    TextAtom,
    ButtonAtom,
    ButtonGroupMolecule,
    FooterOrganism,
  },
  setup() {
    const { changeLanguage } = useLanguage()
    return {
      changeLanguage
    }
  },
};
</script>


<style scoped>

.welcome-content {
  margin-top: -100px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  flex-grow: 1;
}

.welcome-text {
  font-size: 300%;
  font-weight: bold;
  margin-bottom: 150px;
}

.button-group {
  display: flex;
  gap: 15px;
}

.button-group :deep(*) {
  font-size: 30px;
  padding: 35px 100px;
  transition: transform 0.2s;
}

.button-group :deep(*:hover) {
  transform: scale(1.05);
}

.button-link {
  display: contents;
}

</style>