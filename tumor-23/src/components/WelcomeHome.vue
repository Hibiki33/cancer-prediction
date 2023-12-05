<template>
  <div class="welcome-container">
    <h1>{{ title }}</h1>
    <p class="welcome-message">{{ welcomeMessage }}</p>
    <ul>
      <li v-for="photo in photos" :key="photo">
        <img :src="photo" alt="Photo" class="photo-item" />
      </li>
      <li class="image-list">
        <img src="https://wnico-images.oss-cn-beijing.aliyuncs.com/img/202312051826586.jpg" alt="Additional Photo" class="photo-item" />
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
// import { defineProps } from 'vue';

const Welcome = defineProps<{
  title: string;
  photos: string[];
}>();

const welcomeMessage = "欢迎来到我们的网站！这里是欢迎信息！！";


</script>

<style scoped>
.photo-item {
  max-width: 94%;
  max-height: 100vh;
}

.welcome-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  //height: 100vh;
}

.image-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
  list-style: none;
}

.welcome-message {
  text-align: center;
}

</style>