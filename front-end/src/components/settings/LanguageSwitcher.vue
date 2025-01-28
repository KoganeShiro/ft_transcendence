<template>
  <div class="language-content">
    <h2>{{ $t("language") }}</h2>
  </div>
  <div class="lang-btn-container">
    <ButtonAtom
      variant="lang"
      class="lang-btn"
      :class="{ selected: currentLang === 'en' }"
      @click="switchLang('en')"
    >
      {{ $t("english") }}
    </ButtonAtom>
    <ButtonAtom
      variant="lang"
      class="lang-btn"
      :class="{ selected: currentLang === 'fr' }"
      @click="switchLang('fr')"
    >
      {{ $t("french") }}
    </ButtonAtom>
    <ButtonAtom
      variant="lang"
      class="lang-btn"
      :class="{ selected: currentLang === 'de' }"
      @click="switchLang('de')"
    >
      {{ $t("german") }}
    </ButtonAtom>
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import { useI18n } from "vue-i18n";
import ButtonAtom from "@/components/atoms/Button.vue";

export default {
  components: {
    ButtonAtom,
  },
  setup() {
    const { locale } = useI18n();
    return { locale };
  },
  computed: {
    ...mapGetters(["selectedLanguage"]),
    currentLang() {
      return this.selectedLanguage;
    },
  },
  methods: {
    ...mapActions(["changeLang"]),
    switchLang(lang) {
      if (lang !== this.currentLang) {
        this.changeLang(lang);
        this.locale = lang;
      }
    }
  }
};
</script>


<style scoped>
.lang-btn-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 20px;
}

.lang-btn {
  width: 220px;
  text-align: left;
  padding: 14px;
  border-radius: 10px;
  font-size: 1rem;
  color: white;
  transition: all 0.3s ease;
  background-color: transparent;
}

.lang-btn:hover,
.lang-btn.selected {
  background-color: #505050;
  transform: scale(1.05);
  font-weight: bold;
}
</style>
