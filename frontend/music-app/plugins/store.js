import { createStore } from 'vuex';
import createPersistedState from "vuex-persistedstate";

const store = createStore({
  plugins: [createPersistedState()],
  state: {
    username: null,
    roles: [],
    isAuthenticated: false,
  },
  mutations: {
    login(state) {
      state.isAuthenticated = true;
    },
    logout(state) {
      state.isAuthenticated = false;
    },
    setUsername(state, username) {
      state.username = username;
    },
    setRoles(state, roles) {
      state.roles = roles;
    }
  },
  actions: {
    loginUser({ commit }) {
      if (localStorage.getItem('authtoken')!== "null") {
        commit('login');
      }
    },
    logoutUser({ commit }) {
      commit('logout');
    },
  },
  getters: {
    isAuthenticated: state => state.isAuthenticated,
  },
});

export default store;
