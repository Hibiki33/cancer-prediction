<template>
  <el-upload
    ref="uploadRef"
    class="upload-demo"
    action="https://run.mocky.io/v3/9d059bf9-4660-45f2-925d-ce80ad6c4d15"
    :auto-upload="false"
    @change="handleImageChange"

  >
    <template #trigger>
      <el-button type="primary">select file</el-button>
    </template>

    <el-button class="ml-3" type="success" @click="submitUpload">
      upload
    </el-button>

    <template #tip>
      <div class="el-upload__tip">
      </div>
    </template>




  </el-upload>

  <div class="demo-image">
    <div v-for="fit in fits" :key="fit" class="block">
      <span class="demonstration">{{  }}</span>
      <el-image style="width: 300px; height: 300px" :src="imageSrc" :fit="fit" />
    </div>
  </div>

  <div>Results would be shown here</div>
</template>


<script lang="ts" setup>
import { ref } from 'vue'
import type { UploadInstance } from 'element-plus'
import { Picture as IconPicture } from '@element-plus/icons-vue'


const uploadRef = ref<UploadInstance>()
const imageSrc = ref('')
const fits = ['fill']
const uploadResult = ref('')

const submitUpload = () => {
  uploadRef.value!.submit()
  uploadRef.value.onSuccess = (response, file, fileList) => {
  uploadResult.value = response
}

}


const handleImageChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    readImage(file)
  }
}

const readImage = (file: File) => {
  imageSrc.value = URL.createObjectURL(file)
}
</script>


<style scoped>
.demo-image .block {
  padding: 30px 0;
  text-align: center;
  justify-content: center;

  border-right: solid 1px var(--el-border-color);
  display: inline-block;
  width: 20%;
  box-sizing: border-box;
  vertical-align: top;
}
.demo-image .block:last-child {
  border-right: none;
}
.demo-image .demonstration {
  display: block;
  color: var(--el-text-color-secondary);
  font-size: 14px;
  margin-bottom: 20px;
}
</style>
