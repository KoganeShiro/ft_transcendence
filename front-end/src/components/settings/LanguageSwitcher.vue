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
import { mapGetters } from "vuex";
import ButtonAtom from "@/components/atoms/Button.vue";
import API from '@/api.js';
import { useLanguage } from '@/components/useLanguage.js';

export default {
  components: {
    ButtonAtom,
  },
  setup() {
    const { changeLanguage } = useLanguage();
    return {
      changeLanguage
    };
  },
  computed: {
    ...mapGetters(["selectedLanguage"]),
    currentLang() {
      return this.selectedLanguage;
    },
  },
  methods: {
    async switchLang(lang) {
      if (lang !== this.currentLang) {
        try {
          await API.patch('/api/profile_update/', { lang: lang });
          this.changeLanguage(lang);
        } catch (error) {
          console.error("Error updating language:", error);
        }
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
