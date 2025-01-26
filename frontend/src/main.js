import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';
import * as ElementPlusIconsVue from '@element-plus/icons-vue';
const app = createApp(App);

// 注册所有图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component);
}

app.use(ElementPlus);
app.use(router);
app.mount('#app');

const resizeObserverError = /ResizeObserver loop limit exceeded/;

// 捕获所有 ResizeObserver 错误
window.addEventListener('error', (e) => {
  if (resizeObserverError.test(e.message)) {
    console.warn('ResizeObserver 警告被忽略');
    e.stopImmediatePropagation();
  }
});

// 防止未处理的 promise 错误
window.addEventListener('unhandledrejection', (event) => {
  if (event.reason && event.reason.message && event.reason.message.includes('ResizeObserver')) {
    console.warn('未处理的 ResizeObserver 异常被捕获');
    event.preventDefault();
  }
});

if (!window.MonacoEnvironment) {
  window.MonacoEnvironment = {
    getWorkerUrl: function () {
      return URL.createObjectURL(new Blob(
        [
          `self.MonacoEnvironment = { baseUrl: '/' }; importScripts('/monaco-editor/esm/vs/base/worker/workerMain.js');`
        ],
        { type: 'text/javascript' }
      ));
    },
  };
}