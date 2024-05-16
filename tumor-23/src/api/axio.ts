import axios from 'axios'
import {ElLoading, ElMessage} from 'element-plus'

axios.defaults.timeout = 6000000;

axios.defaults.baseURL = 'http://10.134.110.90:8000/'

axios.interceptors.request.use(function (config){
    if (localStorage.eleToken) {
        config.headers.Authorization = "Bearer " + localStorage.eleToken;
    } else if (localStorage.refreshToken) {
        config.headers.Authorization = "Bearer " + localStorage.refreshToken;
    }
    return config;
},function (error) {
    ElMessage.error('通信失败')
    return Promise.reject(error);
});


export default axios