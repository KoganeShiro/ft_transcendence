<template>
  <div class="lang-btn-container">
    <ButtonAtom variant="lang-en" class="lang-btn" @click="switchLang('en')">🇬🇧 English</ButtonAtom>
    <ButtonAtom variant="lang-fr" class="lang-btn" @click="switchLang('fr')">🇫🇷 Français</ButtonAtom>
    <ButtonAtom variant="lang-de" class="lang-btn" @click="switchLang('de')">🇩🇪 Deutsch</ButtonAtom>
  </div>
</template>

<script>
import { mapActions } from "vuex";
import ButtonAtom from "@/components/atoms/Button.vue";

export default {
  components: {
    ButtonAtom,
  },
  methods: {
    ...mapActions(["changeLang"]),
    switchLang(lang) {
      this.changeLang(lang); // Update Vuex state
    },
  },
};
</script>

<style scoped>
.lang-btn-container {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.lang-btn {
  width: 100%;
  text-align: left;
  padding: 10px;
}
</style>
