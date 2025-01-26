const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
})
module.exports = {
  publicPath: './',
  pages: {
    index: {
      entry: 'src/main.js',
      template: 'public/index.html',
      filename: 'index.html',
      title: 'Python Wizard', // 设置固定标题
    },
  },
  chainWebpack: config => {
    config.module
      .rule('js')
      .include.add(/monaco-editor/)
      .end();
  },
};