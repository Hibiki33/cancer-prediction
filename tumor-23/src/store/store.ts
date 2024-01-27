import Vuex from 'vuex';
import { InjectionKey } from 'vue'
import { createStore, Store } from 'vuex'
import createPersistedState from "vuex-persistedstate";

export interface State {
    count: number;
    isLoggedIn: boolean;
    authToken: string | null;
}

export const key: InjectionKey<Store<State>> = Symbol()

export const store = createStore<State>({
    state: {
        count: 0,
        isLoggedIn: false,
        authToken: null
    },
    mutations: {
        logIn(state, login) {
            state.isLoggedIn = login;
        },
        setToken(state, token) {
            state.authToken = token
        }
    },
    plugins: [
        createPersistedState({
            // 存储方式：localStorage、sessionStorage、cookies
            storage: window.sessionStorage,
            // 存储的 key 的key值
            key: "store",
            render(state: any) {
                // 要存储的数据：本项目采用es6扩展运算符的方式存储了state中所有的数据
                return { ...state };
            }
        })
    ]
})
// interface RootState {
//     isLoggedIn: boolean;
//     authToken: string | null;
// }
//
// const state: RootState = {
//     isLoggedIn: false,
//     authToken: null,
// };
//
// const mutations = {
//     isLogin(state: RootState, isLoggedIn: boolean) {
//         state.isLoggedIn = isLoggedIn;
//     },
//     Token(state: RootState, authToken: string | null) {
//         state.authToken = authToken;
//     },
// };
//
// const actions = {
//     login({ commit }: any, { authToken }: { authToken: string }) {
//         commit('setLoggedIn', true);
//         commit('setAuthToken', authToken);
//     },
//     logout({ commit }: any) {
//         commit('setLoggedIn', false);
//         commit('setAuthToken', null);
//     },
// };
//
// export default new Vuex.Store({
//     state,
//     mutations,
//     actions,
// });