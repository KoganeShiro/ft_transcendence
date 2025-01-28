import { createStore } from "vuex";

export default createStore({
  state: {
    theme: "dark",
    lang: localStorage.getItem("lang") || "en"
  },
  mutations: {
    setLang(state, lang) {
      state.lang = lang;
      localStorage.setItem("lang", lang);

      import("@/plugins/i18n").then(({ default: i18n }) => {
        i18n.global.locale = lang;
      });
    }
  },
  actions: {
    changeLang({ commit }, lang) {
      commit("setLang", lang);
    }
  },
  getters: {
    selectedLanguage: (state) => state.lang
  }
});
