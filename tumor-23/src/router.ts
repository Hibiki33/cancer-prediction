import { createRouter, createWebHistory } from "vue-router";
import Diagnose from "./Diagnose.vue";
import Welcome from "./Welcome.vue";

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
    // 其他页面的路由配置
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;