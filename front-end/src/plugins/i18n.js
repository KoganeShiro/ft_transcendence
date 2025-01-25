import { createI18n } from "vue-i18n";
// Keep separate imports for clarity
import enTerms from "@/locales/en/terms.json";
import enPrivacy from "@/locales/en/privacy.json";
import frTerms from "@/locales/fr/terms.json";
import frPrivacy from "@/locales/fr/privacy.json";
import deTerms from "@/locales/de/terms.json";
import dePrivacy from "@/locales/de/privacy.json";

import store from "@/store";

const i18n = createI18n({
  legacy: false,
  locale: store.state.lang || "en",
  fallbackLocale: "en",
  messages: {
    en: {
      terms: enTerms.terms,
      privacy: enPrivacy.privacy
    },
    fr: {
      terms: frTerms.terms,
      privacy: frPrivacy.privacy
    },
    de: {
      terms: deTerms.terms,
      privacy: dePrivacy.privacy
    }
  }
});

export default i18n;