import { createRouter, createWebHistory } from "vue-router";
import Diagnose from "./Diagnose.vue";
import Welcome from "./Welcome.vue";
import Result from "~/components/Result.vue";
import Upload from "~/components/upload.vue";
import WebsiteIntroduce from "~/components/WebsiteIntroduce.vue";
import Login from "~/components/Login.vue"
import Signup from "~/components/Signup.vue";
import { store } from "~/store/store"

// const store = useStore();

const routes = [
    {
        path: "/",
        name: "Welcome",
        component: Welcome,
    },
    {
        path: "/diagnose",
        name: "Diagnose",
        component: Diagnose,
    },
    {
        path: "/intro",
        name: "WebsiteIntroduce",
        component: WebsiteIntroduce
    },
    {
        path: "/login",
        name: "Login",
        component: Login
    },
    {
        path: "/signup",
        name: "Signup",
        component: Signup
    }
    // 其他页面的路由配置
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

router.beforeEach((to, from, next) => {
    if (to.path === '/login' || to.path === '/signup') {
        next();
    } else {

        // let token = localStorage.getItem('Authorization');
        const isLogin = store.state.isLoggedIn
        if (isLogin) {
            next();
        } else {
            next('/login');
        }
    }
});

export default router;
