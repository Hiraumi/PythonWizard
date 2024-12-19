<template>
  <router-view />
</template>

<script>
export default {
  name: 'App',
  created() {
    document.documentElement.lang = 'zh-CN';
  },
};
</script>

<style>
/* 设置全局字体样式 */
body {
  font-family: Helvetica, "PingFang SC", "Microsoft YaHei", Arial, sans-serif;
  margin: 0;
  padding: 0;
}
</style>