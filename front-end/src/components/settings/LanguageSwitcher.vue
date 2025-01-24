<template>
  <div>
    <ButtonAtom variant="en-lang">English</ButtonAtom>
    <ButtonAtom variant="fr-lang">Français</ButtonAtom>
    <ButtonAtom variant="de-lang">Deutsch</ButtonAtom>
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
