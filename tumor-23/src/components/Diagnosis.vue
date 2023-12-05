<template>

  <el-row>
    <el-col :span="12">
      <div class="title1">
        <h3>
          测试项目1
        </h3>
      </div>
      <div class="uploadFile">
        <ul v-show="uploadImg0.length !== 0" class="image-list">
          <li v-for="(item, index) in uploadImg0" :key="index" class="addPic">
            <div class="image-wrapper">
              <img :src="item.src" class="uploaded-image">
              <div class="image-overlay">
                <p>{{ item.name }}</p>
              </div>
            </div>
            <div class="elem-image">
              <div v-for="fit in fits" :key="fit" class="block">
                <span class="demonstration">{{ fit }}</span>
                <el-image style="width: 100px; height: 100px" :src="item.src" :fit="fit" />
              </div>
            </div>
          </li>
        </ul>
        <div class="upload-button-wrapper">
          <input type="file" id="file" accept="image/*" class="hidden-input" ref="fileInput" @change="selectPicture">
          <button class="select-button" @click="openFileInput" v-show="showInputImg">选择照片</button>
          <button class="upload-button" @click="uploadToServer" v-show="1">上传到服务器</button>
        </div>
      </div>
    </el-col>
    <el-col :span="12">
      <div class="title1">
        <h3>
          测试项目2
        </h3>
      </div>
      <div class="uploadFile">
        <ul v-show="uploadImg1.length !== 0" class="image-list">
          <li v-for="(item, index) in uploadImg1" :key="index" class="addPic">
            <div class="image-wrapper">
              <img :src="item.src" class="uploaded-image">
              <div class="image-overlay">
                <p>{{ item.name }}</p>
              </div>
            </div>
            <div class="elem-image">
              <div v-for="fit in fits" :key="fit" class="block">
                <span class="demonstration">{{ fit }}</span>
                <el-image style="width: 100px; height: 100px" :src="item.src" :fit="fit" />
              </div>
            </div>
          </li>
        </ul>
        <div class="upload-button-wrapper">
          <input type="file" id="file" accept="image/*" class="hidden-input" ref="fileInput1" @change="selectPicture1">
          <button class="select-button" @click="openFileInput1" v-show="showInputImg1">选择照片</button>
          <button class="upload-button" @click="uploadToServer" v-show="1">上传到服务器</button>
        </div>
      </div>
    </el-col>
  </el-row>
</template>

<script>
const fits = ['fill']

export default {
  data() {
    return {
      uploadImg0: [],
      uploadImg1: [],
    };
  },
  computed: {
    showInputImg() {
      return this.uploadImg0.length < 3;
    },
    showInputImg1() {
      return this.uploadImg1.length < 3;
    },
  },
  methods: {
    openFileInput() {
      this.$refs.fileInput.click();
    },
    openFileInput1() {
      this.$refs.fileInput1.click();
    },
    selectPicture(e) {
      this.uploadImg0 = [];
      const file = e.target.files[0];
      const src = window.URL.createObjectURL(file);
      this.uploadImg0.push({ src, name: file.name });
    },
    selectPicture1(e) {
      this.uploadImg1 = [];
      const file = e.target.files[0];
      const src = window.URL.createObjectURL(file);
      this.uploadImg1.push({ src, name: file.name });
    },
    uploadToServer() {
      // 将照片上传到远程服务器
      // 你可以在这里使用axios或其他方法将照片上传到服务器
      alert('上传成功');
    },
  },
};
</script>

<style scoped>
.uploadFile {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.image-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
  list-style: none;
}

.addPic {
  position: relative;
}

.image-wrapper {
  position: relative;
  width: 200px;
  height: 200px;
}

.uploaded-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: rgba(0, 0, 0, 0.5);
  color: #fff;
  padding: 10px;
  text-align: center;
  pointer-events: none; /* 防止遮罩层遮挡文件选择框 */
}

.upload-button-wrapper {
  position: relative;
}

.select-button,
.upload-button {
  width: 200px;
  height: 40px;
  background-color: #409eff;
  color: #fff;
  cursor: pointer;
  border-radius: 4px;
  transition: background-color 0.3s;
  display: flex;
  justify-content: center;
  align-items: center;
}

.select-button:hover,
.upload-button:hover {
  background-color: #66b1ff;
}

.hidden-input {
  display: none;
}
</style>