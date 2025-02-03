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
  margin-left: 300px;
  margin-right: 50px;
}

.lang-btn {
  text-align: left;
  padding: 14px;
  border-radius: 10px;
  font-size: 1rem;
  color: var(--text-color);
  transition: all 0.3s ease;
  background-color: transparent;
}

.lang-btn:hover,
.lang-btn.selected {
  /* background-color: #505050; */
  background-color: var(--sidebar-hoover-color);
  transform: scale(1.05);
  font-weight: bold;
}

@media (max-width: 1268px) {
  .lang-btn-container {
    margin-left: 100px;
  }
}

@media (max-width: 968px) {
  .lang-btn-container {
    margin-left: 50px;
  }
}

@media (max-width: 468px) {
  .lang-btn-container {
    margin-left: 15px;
    margin-right: 15px;
  }
}

</style>
