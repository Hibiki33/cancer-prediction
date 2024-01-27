import { Store } from 'vuex'

declare module '@vue/runtime-core' {
    interface State {
        count: number;
        isLoggedIn: boolean;
        authToken: string | null;
    }

    // 为 `this.$store` 提供类型声明
    interface ComponentCustomProperties {
        $store: Store<State>
    }
}