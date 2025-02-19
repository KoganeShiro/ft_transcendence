import { useI18n } from 'vue-i18n';
import { useStore } from 'vuex';

export function useLanguage() {
  const store = useStore();
  const { locale } = useI18n({ useScope: 'global' });

  const changeLanguage = (lang) => {
    store.dispatch('changeLanguage', lang);
    locale.value = lang;
  };

  return {
    changeLanguage
  };
}
