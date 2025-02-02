import { createStore } from "vuex";

export default createStore({
  state: {
    theme: localStorage.getItem("theme") || "dark",
    lang: localStorage.getItem("lang") || "en"
  },
  mutations: {
    setLang(state, lang) {
      state.lang = lang;
      localStorage.setItem("lang", lang);

      import("@/plugins/i18n").then(({ default: i18n }) => {
        i18n.global.locale = lang;
      });
    },
    setTheme(state, theme) {
      console.log("Setting theme:", theme);
      state.theme = theme;
      localStorage.setItem("theme", theme);
      document.body.setAttribute("data-theme", theme);
    }
  },
  actions: {
    changeLang({ commit }, lang) {
      commit("setLang", lang);
    },
    changeTheme({ commit }, theme) {
      commit("setTheme", theme);
    }
  },
  getters: {
    selectedLanguage: (state) => state.lang,
    selectedTheme: (state) => state.theme
  }
});