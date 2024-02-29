<template>
  <el-row justify="center">
    <el-col :span="12">
      <div>
        <h3>
          测试项目
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
          <div class="button-container">
            <el-row class="mb-4"> 
                <input type="file" id="file" accept="image/*" class="hidden-input" ref="fileInput" @change="selectPicture">
                <el-button type="primary" @click="openFileInput" v-show="showInputImg">
                  选择照片
                </el-button>
            </el-row>
            <el-row class="mb-4"> 
              <el-button type="primary" @click="uploadToServer" v-show="1">
                上传到服务器
              </el-button>
            </el-row>
            <el-row class="mb-4"> 
              <el-button type="primary" :disabled="!flag" @click="showResult()">
                {{ flag ? '查看结果' : '等待结果' }}
              </el-button>
            </el-row>
            <div class="multiline"> {{schedule}} </div>
          </div>
        </div>
      </div>
    </el-col>
<!--    <el-col :span="12">-->
<!--      <div class="title1">-->
<!--        <h3>-->
<!--          测试项目2-->
<!--        </h3>-->
<!--      </div>-->
<!--      <div class="uploadFile">-->
<!--        <ul v-show="uploadImg1.length !== 0" class="image-list">-->
<!--          <li v-for="(item, index) in uploadImg1" :key="index" class="addPic">-->
<!--            <div class="image-wrapper">-->
<!--              <img :src="item.src" class="uploaded-image">-->
<!--              <div class="image-overlay">-->
<!--                <p>{{ item.name }}</p>-->
<!--              </div>-->
<!--            </div>-->
<!--            <div class="elem-image">-->
<!--              <div v-for="fit in fits" :key="fit" class="block">-->
<!--                <span class="demonstration">{{ fit }}</span>-->
<!--                <el-image style="width: 100px; height: 100px" :src="item.src" :fit="fit" />-->
<!--              </div>-->
<!--            </div>-->
<!--          </li>-->
<!--        </ul>-->
<!--        <div class="upload-button-wrapper">-->
<!--          <div class="button-container">-->
<!--            <el-row class="mb-4"> -->
<!--                <input type="file" id="file" accept="image/*" class="hidden-input" ref="fileInput" @change="selectPicture">-->
<!--                <el-button type="primary" @click="openFileInput1" v-show="showInputImg1">选择照片</el-button>  -->
<!--            </el-row>-->
<!--            <el-row class="mb-4"> -->
<!--              <el-button type="primary" @click="uploadToServer" v-show="1">上传到服务器</el-button>-->
<!--            </el-row>-->
<!--            <el-row class="mb-4"> -->
<!--              <el-button type="primary" @click="openResultWindow(1)">查看结果</el-button>-->
<!--            </el-row>-->
<!--          </div>-->
<!--        </div>-->
<!--      </div>-->
<!--    </el-col>-->
  </el-row>
</template>

<script>
import {doPostPicture} from "~/api/api";
import api from '../utils/api'

const fits = ['fill']

export default {
  data() {
    return {
      uploadImg0: [],
      uploadImg1: [],
      schedule: "",
      file: "",
      flag: false,
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
    showResult() {
      api.get('/medicalCase/get_schedule').then(
          res => {
            console.log(res.data)
            this.schedule = res.data.schedule
            console.log(this.schedule)
          }
      )
    },
    openFileInput() {
      this.$refs.fileInput.click();
    },
    openFileInput1() {
      this.$refs.fileInput1.click();
    },
    selectPicture(e) {
      this.uploadImg0 = [];
      this.file = e.target.files[0];
      const src = window.URL.createObjectURL(this.file);
      console.log(file)
      this.uploadImg0.push({ src, name: this.file.name });
    },
    selectPicture1(e) {
      this.uploadImg1 = [];
      this.file = e.target.files[0];
      const src = window.URL.createObjectURL(this.file);
      this.uploadImg1.push({ src, name: this.file.name });
    },
    uploadToServer() {
      // 将照片上传到远程服务器
      // 你可以在这里使用axios或其他方法将照片上传到服务器
      doPostPicture(this.file).then(
          res => {
            this.flag = true
          }
      );
      // alert('上传成功');
    },
    openResultWindow(index) {
      const uploadResultKey = `uploadResult${index}`;
      const result = this[uploadResultKey] || '暂无结果'; // 如果结果为空，显示默认消息

      // 打开一个新窗口并显示结果
      const resultWindow = window.open('', '_blank');
      resultWindow.document.write(`
<p>${result}</p>
<img src="https://pic.imgdb.cn/item/6537baf1c458853aef11adef.jpg" alt="Uploaded Image" style="max-width: 100%; max-height: 100%;"/>
`);
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


.button-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
}

.el-row {
  margin-top: 10px;  /* 上间隔 */
  margin-bottom: 10px; /* 下间隔 */
}

.multiline {
  white-space: pre-line;
}

</style>