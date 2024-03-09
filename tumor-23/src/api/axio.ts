import axios from 'axios'
import {ElLoading, ElMessage} from 'element-plus'

let loading: any;
const startLoading = () => {

    interface Options {
        lock: boolean;
        text: string;
        background: string;
    }

    const options: Options = {
        lock: true,
        text: "加载中...",
        background: '#FFFFFF'
    }
    loading = ElLoading.service(options);
}

const endLoading = () => {
    loading.close();
}

// 设置接口超时时间
axios.defaults.timeout = 60000;

axios.defaults.baseURL = 'http://127.0.0.1:8000/'
// http request 拦截器
axios.interceptors.request.use(function (config){
    // 在发送请求前做些什么
    // startLoading();
    //config.headers['X-Requested-With'] = 'XMLHttpRequest'
    if (localStorage.eleToken) {
        config.headers.Authorization = "Bearer " + localStorage.eleToken;
    } else if (localStorage.refreshToken) {
        config.headers.Authorization = "Bearer " + localStorage.refreshToken;
    }
    return config;
},function (error) {
    // 对请求错误做些什么
    ElMessage.error('网络连接异常,请稍后再试')
    return Promise.reject(error);
});


export default axios