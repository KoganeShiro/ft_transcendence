// store/modules/game.js
export default {
    namespaced: true,
    state: () => ({
      isInGame: false
    }),
    mutations: {
      SET_IN_GAME(state, value) {
        state.isInGame = value;
      }
    },
    actions: {
      setInGame({ commit }, value) {
        commit('SET_IN_GAME', value);
      }
    }
  };
  