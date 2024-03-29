import { createStore } from 'vuex';

const store = createStore({
  state: {
    username: null,
    roles: []
  },
  mutations: {
    setUsername(state, username) {
      state.username = username;
    },
    setRoles(state, roles) {
      state.roles = roles;
    }
  },
});

export default store;
