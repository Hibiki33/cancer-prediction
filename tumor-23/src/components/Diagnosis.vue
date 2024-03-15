<template>

  <body>
    <div class="base_container">
      <div class="files_column">
        <div class="image">
          <div v-if="chooseFlag">
            <img :src="imgUrl" alt="Preview" class="image-preview">
          </div>
          <div v-else>
            <img src="/cancer_picture.png" alt="Placeholder" class="image-placeholder">
          </div>
        </div>
        <div class="result">
          <el-input
              type="textarea"
              :rows="2"
              placeholder="请输入内容"
              v-model="schedule"
              :autosize="{ minRows: 5, maxRows: 8}"
              readonly>
          </el-input>
        </div>
      </div>
      <div style="width: 1px; height: 800px; background-color: #0a0a0a;"></div>
      <div class="buttons_column">
        <div class="upload-button-wrapper">
          <div class="button-container">
            <div class="button_gap">
              <el-row>
                <input type="file" id="file" accept="image/*" class="hidden-input" ref="fileInput" @change="selectPicture">
                <el-button type="primary" @click="openFileInput" v-show="showInputImg" round>
                  选择照片
                </el-button>
              </el-row>
            </div>
            <div class="button_gap">
              <el-row>
                <el-button type="primary" @click="uploadToServer" v-show="1" round>
                  上传到服务器
                </el-button>
              </el-row>
            </div>
            <div class="button_gap">
              <el-row>
                <el-button type="info" :disabled="!resultFlag" @click="showResult()" round>
                  {{ resultFlag ? '查看结果' : '等待结果' }}
                </el-button>
              </el-row>
            </div>
            <div class="button_gap">
              <el-row>
                <el-button type="success" round>
                  <el-upload :type="file" :on-change="handleUpload" :auto-upload="false" :multiple="false" :show-file-list="false">
                    上传文件
                  </el-upload>
                </el-button>
              </el-row>
            </div>

          </div>
        </div>
      </div>
    </div>
    <el-row justify="center">
      <!--    <el-col :span="12">-->
      <!--      <div>-->
      <!--        <h3>-->
      <!--          测试项目-->
      <!--        </h3>-->
      <!--      </div>-->
      <!--      <div class="uploadFile">-->
      <!--        <ul v-show="uploadImg0.length !== 0" class="image-list">-->
      <!--          <li v-for="(item, index) in uploadImg0" :key="index" class="addPic">-->
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
      <!--                <el-button type="primary" @click="openFileInput" v-show="showInputImg">-->
      <!--                  选择照片-->
      <!--                </el-button>-->
      <!--            </el-row>-->
      <!--            <el-row class="mb-4"> -->
      <!--              <el-button type="primary" @click="uploadToServer" v-show="1">-->
      <!--                上传到服务器-->
      <!--              </el-button>-->
      <!--            </el-row>-->
      <!--            <el-row class="mb-4"> -->
      <!--              <el-button type="primary" :disabled="!chooseFlag" @click="showResult()">-->
      <!--                {{ chooseFlag ? '查看结果' : '等待结果' }}-->
      <!--              </el-button>-->
      <!--            </el-row>-->
      <!--            <div class="multiline"> {{schedule}} </div>-->
      <!--          </div>-->
      <!--        </div>-->
      <!--      </div>-->
      <!--    </el-col>-->
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
  </body>

</template>

<script>

import {doPostPicture} from "~/api/api";
import api from '../utils/api'
import { handleUpload } from '~/composables/upload'

const fits = ['fill']

export default {
  data() {
    return {
      uploadImg0: [],
      uploadImg1: [],
      schedule: "暂无结果",
      file: "",
      chooseFlag: false,
      imgUrl: null,
      resultFlag: false,
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
    handleUpload,
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
      this.imgUrl = window.URL.createObjectURL(this.file);
      this.chooseFlag = true;
      const url = this.imgUrl;
      console.log(this.file);
      console.log(this.imgUrl);
      this.uploadImg0.push({ url, name: this.file.name });
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
            this.resultFlag = true
          }
      );
      lert('上传成功');
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
html {
  height:100%;
}

.base_container {
  display: flex;
}

.files_column {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 5;
}

.image-preview, .image-placeholder {
  max-width: 800px;
  max-height: 500px;
}

.buttons_column {
  flex: 3;
}

.image {
  flex: 2;
  border: thick double #CAE2F5;
}

.result {
  flex: 1;
  margin-top: 20px;
  width: 60%;
}

.button_gap {
  margin-top: 50px;
  margin-bottom: 50px;
}

.upload-button-wrapper {
  position: relative;
}

.hidden-input {
  display: none;
}

.button-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  margin-top: 50px;
  max-width: 400px;
}

</style>
