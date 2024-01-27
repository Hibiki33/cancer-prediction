<script setup lang="ts">

import { useRouter } from 'vue-router';
import api from '../utils/api'

const signupForm = {
  username: "",
  password: "",
}

const router = useRouter();

const login = () => {
  if (signupForm.username === '' || signupForm.password === '') {
    alert('账号或密码不能为空');
  } else {
    api.post('/user/sign_up/?token=${token}', signupForm).then(
        res => {
          console.log(res.data);
          router.push('/');
          alert('注册成功');
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
    <input type="text" v-model="signupForm.username" placeholder="用户名"/>
    <input type="text" v-model="signupForm.password" placeholder="密码"/>
    <button @click="login">注册</button>
  </div>
</template>

<style scoped>

</style>