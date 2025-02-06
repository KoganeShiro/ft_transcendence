// store/modules/invitations.js
export default {
  namespaced: true, // Crucial for namespacing
  state: () => ({
    showInvitation: false,
    invitationData: null
  }),
  mutations: {
    SHOW_INVITATION(state, payload) {
      state.showInvitation = true
      state.invitationData = payload
    },
    HIDE_INVITATION(state) {
      state.showInvitation = false
      state.invitationData = null
    }
  },
  actions: {
    showInvitation({ commit }, data) {
      commit('SHOW_INVITATION', data)
    },
    hideInvitation({ commit }) {
      commit('HIDE_INVITATION')
    }
  }
}
