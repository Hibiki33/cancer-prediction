<template>
  <body>
    <div class="base_container">
      <div class="files_column">
        <div class="image">
          <vue-cropper ref="cropper" :img="option.img" :output-size="option.size" :output-type="option.outputType" :info="true" :full="option.full" :fixed="fixed" :fixed-number="fixedNumber"
                       :can-move="option.canMove" :can-move-box="option.canMoveBox" :fixed-box="option.fixedBox" :original="option.original"
                       :auto-crop="option.autoCrop" :auto-crop-width="option.autoCropWidth" :auto-crop-height="option.autoCropHeight" :center-box="option.centerBox"
                       :high="option.high" :max-img-size="option.max" @crop-moving="cropMoving" mode="cover"></vue-cropper>
        </div>
        <div class="result">
          <div style="display: flex; flex-direction: row">
            <div style="flex: 1; padding-right: 5px">
            方案
            <el-input
                type="textarea"
                :rows="2"
                placeholder="请输入内容"
                v-model="result_case"
                :autosize="{ minRows: 8, maxRows: 15}"
                readonly>
            </el-input>
            </div>
            <div style="flex: 1; padding-left: 5px">
            预测
            <el-input
                type="textarea"
                :rows="2"
                placeholder="请输入内容"
                v-model="result_predict"
                :autosize="{ minRows: 8, maxRows: 15}"
                readonly>
            </el-input>
            </div>
          </div>

        </div>
      </div>
      <div style="width: 1px; height: 800px; background-color: #0a0a0a;"></div>
      <div class="buttons_column">
        <div class="upload-button-wrapper">
          <div class="button-container">
            <el-row class="el_row_s">
              姓名 *
              <el-input v-model="patient_name" placeholder="请输入内容" class="input"></el-input>
            </el-row>
            <el-row class="el_row_s">
              性别 *
              <el-select v-model="patient_gender" placeholder="请选择" class="input">
                <el-option v-for="item in gender_option" :key="item.value" :label="item.label" :value="item.value"></el-option>
              </el-select>
            </el-row>
            <el-row class="el_row_s">
              确诊时间 *
              <el-date-picker v-model="diagnosis_date" type="Date" placeholder="选择日期" style="max-width: 150px; padding-left: 10px;"></el-date-picker>
            </el-row>
            <el-row class="el_row_s">
              肿瘤类型
              <el-select v-model="tumor_type" placeholder="请选择" class="input">
                <el-option v-for="item in tumor_type_option" :key="item.value" :label="item.label" :value="item.value"></el-option>
              </el-select>
            </el-row>
            <el-row class="el_row_s">
              肿瘤分期
              <el-select v-model="tumor_state" placeholder="请选择" class="input">
                <el-option v-for="item in tumor_state_option" :key="item.value" :label="item.label" :value="item.value"></el-option>
              </el-select>
            </el-row>
            <el-row class="el_row_s">
              <el-button :disabled="uploading" type="success" round>
                <el-upload :type="file" accept=".svs" :on-change="doHandleUpload" :auto-upload="false" :multiple="false" :show-file-list="false">
<!--                <el-upload :type="file" action="http://10.134.110.90:8000/fileManager/uploadc/" accept=".svs" :multiple="false" :show-file-list="false"-->
<!--                data="{}">-->
                  {{ buttonText }}
<!--                  {{ uploading ? "等待上传" : "上传文件" }}-->
                </el-upload>
              </el-button>
            </el-row>
            <el-row class="el_row_s">
              <el-button :disabled="resultFlag" type="success" round @click="getResult">
                {{ resultText }}
              </el-button>
            </el-row>
          </div>
        </div>
      </div>
    </div>
  </body>

</template>

<script>
import { handleUpload } from '~/composables/upload'
import { ElMessage } from "element-plus";
import 'vue-cropper/dist/index.css';
import axios from '~/api/axio'

export default {
  data() {
    return {
      result_case: "暂无结果",
      result_predict: "暂无结果",
      tumor_state: "",
      tumor_state_option: [{value: "选项1", label: "STAGEⅠ"}, {value: "选项2", label: "STAGEⅡ"}, {value: "选项3", label: "STAGEⅢ"}, {value: "选项4", label: "STAGEⅣ"}],
      tumor_type: "",
      tumor_type_option: [{value: "选项1", label: "直肠癌"}, {value: "选项2", label: "结肠癌"}],
      diagnosis_date: "",
      patient_name: "",
      patient_gender: "",
      gender_option: [{value: "选项1", label: "男"}, {value: "选项2", label: "女"}],
      uploadImg0: [],
      uploadImg1: [],
      schedule: "暂无结果",
      file: "",
      chooseFlag: false,
      imgUrl: null,
      resultFlag: true,
      uploading: false,
      buttonText: "上传文件",
      resultText: "等待结果",
      imageSrc: "/cancer_picture.jpg",
      option:{
        img: '/cancer_picture.jpg',             //裁剪图片的地址
        outputSize: 1,       //裁剪生成图片的质量(可选0.1 - 1)
        outputType: 'jpeg',  //裁剪生成图片的格式（jpeg || png || webp）
        info: true,          //图片大小信息
        canScale: false,      //图片是否允许滚轮缩放
        autoCrop: true,      //是否默认生成截图框
        autoCropWidth: 500,  //默认生成截图框宽度
        autoCropHeight: 500, //默认生成截图框高度
        fixed: true,         //是否开启截图框宽高固定比例
        fixedNumber: [1.53, 1], //截图框的宽高比例
        full: false,         //false按原比例裁切图片，不失真
        fixedBox: false,      //固定截图框大小，不允许改变
        canMove: false,      //上传图片是否可以移动
        canMoveBox: true,    //截图框能否拖动
        original: true,     //上传图片按照原始比例渲染
        centerBox: true,    //截图框是否被限制在图片里面
        height: true,        //是否按照设备的dpr 输出等比例图片
        infoTrue: false,     //true为展示真实输出图片宽高，false展示看到的截图框宽高
        maxImgSize: 3000,    //限制图片最大宽度和高度
        enlarge: 1,          //图片根据截图框输出比例倍数
      },
    };
  },
  mounted() {
    this.loadImage("/cancer_picture.jpg");
  },
  methods: {
    loadImage(url) {
      console.log("load image")
      fetch(url)
          .then(response => response.blob())
          .then(blob => {
            // 将获取到的 Blob 对象赋值给 imgSrc
            this.option.img = URL.createObjectURL(blob);
          })
          .catch(error => {
            console.error('发生错误：', error);
          });
    },
    async doHandleUpload(file, fileList) {
      if (this.patient_name === "" || this.patient_gender === "" || this.diagnosis_date === "") {
        ElMessage.error("请输入患者信息！");
        console.log("请输入患者信息！")
        return;
      }

      this.uploading = true;
      this.buttonText = "请等待上传";
      await new Promise(resolve => setTimeout(resolve, 2000));
      this.buttonText = "上传完成";
      await new Promise(resolve => setTimeout(resolve, 3000));
      this.resultText = "查看结果";
      this.uploading = false;
      this.resultFlag = false;
      // handleUpload(file, fileList).then(response => {
      //   console.log("response: " + response)
      //   // this.uploading = false;
      //   // this.buttonText = "上传文件";
      //   // ElMessage.success("成功上传文件");
      //   //
      //   // const imageData = response.data;
      //   // const blob = new Blob([imageData], { type: 'image/jpeg'})
      //   // const reader = new FileReader();
      //   // reader.onload = () => {
      //   //   // 将读取到的数据转换为Base64格式
      //   //   this.option.img = reader.result;
      //   // };
      //   // reader.readAsDataURL(blob);
      // })
    },
    getResult() {
      axios.get("medicalCase/get_prediction/").then(
          response => {
            this.result_case = response.data['case']
            this.result_predict = response.data['prediction']
            console.log(this.result_predict)
          }
      )
    }


  },
};
</script>

<style scoped>
html {
  height:100%;
}

.el_row_s {
  margin-bottom: 20px
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
  width: 500px;
  height: 500px;
  margin: 30px auto;
  border: thick double #CAE2F5;
}

.result {
  flex: 1;
  margin-top: 20px;
  width: 60%;
}

.input {
  max-width: 150px;
  padding-left: 10px;
}

.upload-button-wrapper {
  position: relative;
}

.button-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  margin-top: 50px;
  max-width: 400px;
}

.cropper-content{
  display: flex;
  display: -webkit-flex;
  justify-content: flex-end;
  .cropper-box{
    flex: 1;
    width: 100%;
    .cropper{
      width: auto;
      height: 300px;
    }
  }

  .show-preview{
    flex: 1;
    -webkit-flex: 1;
    display: flex;
    display: -webkit-flex;
    justify-content: center;
    .preview{
      overflow: hidden;
      border:1px solid #67c23a;
      background: #cccccc;
    }
  }
}

</style>
