import { createStore } from 'vuex'

export default createStore({
  state: {
    theme: 'dark',
    lang: 'en'
  },
  mutations: {
    setTheme(state, theme) {
      state.theme = theme
    },
    setLang(state, lang) {
      state.lang = lang
    }
  },
  actions: {
    initializeApp({ commit }) {
      const savedTheme = localStorage.getItem('theme') || 'dark'
      const savedLang = localStorage.getItem('lang') || 'en'
      commit('setTheme', savedTheme)
      commit('setLang', savedLang)
    },
    changeTheme({ commit }, theme) {
      commit('setTheme', theme)
      localStorage.setItem('theme', theme)
    },
    changeLang({ commit }, lang) {
      commit('setLang', lang)
      localStorage.setItem('lang', lang)
    }
  }
})