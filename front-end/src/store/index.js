import { createStore } from 'vuex';

export default createStore({
  state: {
    theme: 'light',
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
      if (theme.toLowerCase() === 'light' || theme.toLowerCase() === 'dark'
            || theme.toLowerCase() === 'ocean' || theme.toLowerCase() === 'forest'
            || theme.toLowerCase() === 'volcano' || theme.toLowerCase() === 'Teapot') {
        commit('setTheme', theme);
      }
      else {
        commit('setTheme', 'dark');
      }
    },
    changeLanguage({ commit }, lang) {
      if (lang.toLowerCase() === 'en' || lang.toLowerCase() === 'fr' || lang.toLowerCase() === 'de') {
        commit('setLanguage', lang);
      }
      else {
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
