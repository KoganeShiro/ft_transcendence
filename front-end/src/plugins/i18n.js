import { createI18n } from "vue-i18n";

// Import translation files
import enTerms from "@/locales/en/terms.json";
import enPrivacy from "@/locales/en/privacy.json";
import frTerms from "@/locales/fr/terms.json";
import frPrivacy from "@/locales/fr/privacy.json";
import deTerms from "@/locales/de/terms.json";
import dePrivacy from "@/locales/de/privacy.json";
import en from "@/locales/en/en.json"; // General translations
import fr from "@/locales/fr/fr.json";
import de from "@/locales/de/de.json";

const i18n = createI18n({
  legacy: false,
  locale: store.state.lang, // Use Vuex state as default language
  fallbackLocale: "en",
  messages: {
    en: {
      ...en,
      terms: enTerms.terms,
      privacy: enPrivacy.privacy
    },
    fr: {
      ...fr,
      terms: frTerms.terms,
      privacy: frPrivacy.privacy
    },
    de: {
      ...de,
      terms: deTerms.terms,
      privacy: dePrivacy.privacy
    }
  }
});

import store from "@/store";

store.watch(
  (state) => state.lang,
  (newLang) => {
    i18n.global.locale = newLang; 
  }
);

export default i18n;
