<script setup lang="ts">

import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import api from '../utils/api'
import { key } from '~/store/store'

const loginForm = {
  username: '',
  password: ''
};

let userToken;

const store = useStore(key)

const router = useRouter();
const login = () => {

  if (loginForm.username === '' || loginForm.password === '') {
    alert('账号或密码不能为空');
  } else {
    api.post('/user/login/', loginForm).then(
        res => {
          console.log(res.data);
          userToken = 'Bearer ' + res.data.data.token;
          console.log(userToken);

          store.commit('logIn', true);
          store.commit('setToken', userToken);
          router.push('/');
          alert('登录成功');
        }
    ).catch(error => {
      alert('账号或密码错误');
      console.log(error);
    });
  }
}

</script>

<template>
  <div>
    <input type="text" v-model="loginForm.username" placeholder="用户名"/>
    <input type="text" v-model="loginForm.password" placeholder="密码"/>
    <button @click="login">登录</button>
  </div>
</template>

<style scoped>

</style>
