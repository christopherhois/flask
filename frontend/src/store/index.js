import { createStore } from 'vuex';
import axios from 'axios';

export default createStore({
    state: {
        user: null,
        token: localStorage.getItem('token') || ''
    },
    mutations: {
        setUser(state, user) {
            state.user = user;
        },
        setToken(state, token) {
            state.token = token;
            localStorage.setItem('token', token);
        },
        clearAuthData(state) {
            state.user = null;
            state.token = '';
            localStorage.removeItem('token');
        }
    },
    actions: {
        async login({ commit }, authData) {
            const response = await axios.post('http://89.58.1.183:5000/api/auth/login', authData);
            commit('setToken', response.data.token);
            await this.dispatch('fetchUser');
        },
        async fetchUser({ commit, state }) {
            if (!state.token) {
                return;
            }
            try {
                const response = await axios.get('http://89.58.1.183:5000/api/auth/user', {
                    headers: {
                        Authorization: `Bearer ${state.token}`
                    }
                });
                commit('setUser', response.data);
            } catch (error) {
                console.error('Error fetching user data:', error);
                commit('clearAuthData');
            }
        },
        logout({ commit }) {
            commit('clearAuthData');
        }
    },
    getters: {
        isAuthenticated(state) {
            return !!state.token;
        },
        user(state) {
            return state.user;
        },
        isAdmin(state) {
            return state.user ? state.user.isAdmin : false;
        }
    }
});
