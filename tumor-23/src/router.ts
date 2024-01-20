import { createRouter, createWebHistory } from "vue-router";
import Diagnose from "./Diagnose.vue";
import Welcome from "./Welcome.vue";
import Result from "~/components/Result.vue";
import Upload from "~/components/upload.vue";
import WebsiteIntroduce from "~/components/WebsiteIntroduce.vue";

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
    }
    // 其他页面的路由配置
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
