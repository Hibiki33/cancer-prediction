<template>
  <div id="app">
    <el-upload
        action=""
        :before-upload="postFile"
        :limit="1"
        :auto-upload="false"
        :show-file-list="false"
    >
      <el-button size="small" type="primary">点击上传</el-button>
    </el-upload>
  </div>
</template>

<script>
import {postMerge, doUpload} from "~/api/api";
import {ElMessage} from "element-plus";
export default {
  data() {
    return {

    }
  },
  methods: {
    creatFileMd5(file) {
      return self.SparkMD5.hashBinary(file)
    },
    sliceFile(file, chunkSize) {
      const chunks = [];
      let offset = 0;
      while (offset < file.size) {
        const chunk = file.slice(offset, offset + chunkSize);
        chunks.push(chunk);
        offset += chunkSize;
      }
      return chunks;
    },
    createFileChunks(file, slices) {
      if (!slices?.length) return [];

      return slices.map((slice, index) => ({
        index: index,
        chunk: slice,
        hash: index,
        fileName: file.name,
      }));
    },
    postFile(file) {
      console.log('test')
      ElMessage.error('test')
      const slice_size = 5 * 1024 * 1024;
      const file_list = this.sliceFile(file, slice_size)
      const chunks = this.createFileChunks(file, file_list)
      this.uploadFileChunks(chunks, [])

      return false  // 不使用 el 的默认上传
    },
    uploadFileChunks(chunks, upLoadedChunks) {
      if (!chunks?.length) return;

      const requests = chunks.filter(({ hash }) => !upLoadedChunks.includes(hash)).map((item) => {
        const { chunk, hash, fileName, index } = item;
        const data = new FormData();
        data.append('chunk', chunk)
        data.append('hash', hash)
        data.append('fileName', fileName)

        return doUpload(data);
      })

      Promise.all(requests).then(res => {
        postMerge({
          fileName: chunks[0].fileName,
          hash: chunks[0].hash,
          size: 5 * 1024 * 1024
        })
      }).catch(err => {
        console.log(err)
        ElMessage.error('Oops, it failed')
      })
    }
  },
  destroyed() {
  },
}
</script>

<style lang="scss" scoped>
.video-box {
  width: 400px;
  height: 250px;
  video {
    width: 100%;
    height: 100%;
  }
}
</style>
