<script setup lang="ts">

</script>

<template>
  <div class="contain">
    <div class="left-panel">
      <!-- 左侧内容 -->
      <div class="intro-item">
        <img src="https://pic.imgdb.cn/item/65ab4329871b83018a958c6b.png" alt="介绍图片1" class="item-image-left">
      </div>
      <div class="intro-item">
        <div class="item-title-left">
          标题
        </div>
        <div class="item-content-left">
          内容。。。。。。。。。。
        </div>
      </div>

    </div>
    <div class="vertical-line"></div>
    <div class="right-panel">
      <!-- 右侧内容 -->
      <div class="intro-item">
        <div class="item-title-right">
          标题
        </div>
        <div class="item-content-right">
          内容。。。。。。。。。。
        </div>
      </div>
      <div class="intro-item">
        <img src="https://pic.imgdb.cn/item/65ab4329871b83018a958c6b.png" alt="介绍图片1" class="item-image-right">
      </div>
    </div>
  </div>
</template>

<style scoped>

body {
  margin: 0;
  padding: 0;
  font-family: Arial, sans-serif;
}

.contain {
  display: flex;
  align-items: center;
  height: 100vh; /* 100% viewport height */
}

.left-panel,
.right-panel {
  flex: 1;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: stretch;
}

.vertical-line {
  width: 1px;
  background-color: #ccc;
  height: 100%;
  display: flex;
  align-items: center;
}

.intro-item {
  height: 300px;
  padding: 20px;
}

.item-title-right {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
  text-align: left;
  padding: 20px;
}

.item-content-right {
  font-size: 16px;
  color: #666;
  text-align: left;
}

.item-title-left {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
  text-align: right;
  padding: 20px;
}

.item-content-left {
  font-size: 16px;
  color: #666;
  text-align: right;
}

.item-image-left {
  width: auto; /* 设置图片宽度为父元素宽度 */
  height: 100%; /* 保持宽高比，自动计算高度 */
  display: block; /* 使图片成为块级元素，避免可能的垂直间距问题 */
  margin-left: auto; /* 将左外边距设置为 auto，实现靠右对齐 */
}

.item-image-right {
  width: auto; /* 设置图片宽度为父元素宽度（占据整个左侧内容宽度） */
  height: 100%; /* 保持宽高比，自动计算高度 */
  display: block; /* 使图片成为块级元素，避免可能的垂直间距问题 */
}



</style>