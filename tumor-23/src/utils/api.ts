import axios, { AxiosInstance } from 'axios';
import { store } from '~/store/store'

const instance: AxiosInstance = axios.create({
    baseURL: 'http://127.0.0.1:8000', // 你的 API 地址
    timeout: 5000, // 请求超时时间
    headers: {
        'Content-Type': 'application/json',
        // 'Authorization': 'Bearer ' + localStorage.getItem('token'),
    },
});

instance.interceptors.request.use(
    config => {
        // 在这里通过本地存储或状态管理获取 token
        if (store.state.authToken) {
            config.headers.Authorization = "Bearer " + store.state.authToken;
        }
        return config;
    },
    error => {
        return Promise.reject(error);
    }
)


export default instance;