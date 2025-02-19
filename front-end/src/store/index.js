import { createStore } from 'vuex';

export default createStore({
  state: {
    theme: 'dark',
    lang: 'en',
  },
  mutations: {
    setTheme(state, theme) {
      state.theme = theme;
    },
    setLanguage(state, lang) {
      state.lang = lang;
    },
  },
  actions: {
    changeTheme({ commit }, theme) {
      const validThemes = ['light', 'dark', 'ocean', 'forest', 'volcano', 'teapot'];
      if (validThemes.includes(theme.toLowerCase())) {
        commit('setTheme', theme);
      } else {
        commit('setTheme', 'dark');
      }
    },
    changeLanguage({ commit }, lang) {
      const validLanguages = ['en', 'fr', 'de'];
      if (validLanguages.includes(lang.toLowerCase())) {
        commit('setLanguage', lang);
      } else {
        commit('setLanguage', 'en');
      }
    },
    initializeApp({ commit }) {
      // Initialize the app with default settings or fetch initial data
      const theme = localStorage.getItem('theme') || 'dark';
      const lang = localStorage.getItem('lang') || 'en';
      commit('setTheme', theme);
      commit('setLanguage', lang);
    },
  },
  getters: {
    selectedTheme: state => state.theme,
    selectedLanguage: state => state.lang,
  },
});
