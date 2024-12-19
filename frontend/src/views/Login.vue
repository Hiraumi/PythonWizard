<template>
  <div class="login-page">
    <!-- 左侧 LOGO 区域 -->
    <div class="logo-container">
      <img src="@/assets/logo.png" alt="Python Wizard Logo" class="logo" />
    </div>

    <!-- 右侧登录区域 -->
    <div class="login-wrapper">
      <div class="login-container">
        <h2 class="login-title">登录</h2>
        <el-form ref="loginForm" :model="loginForm" class="login-form">
          <!-- 用户名输入框 -->
          <el-form-item>
            <el-input
              v-model="loginForm.username"
              placeholder="用户名"
              clearable
              size="large"
            >
              <template #prefix>
                <el-icon><User /></el-icon>
              </template>
            </el-input>
          </el-form-item>

          <!-- 密码输入框 -->
          <el-form-item>
            <el-input
              v-model="loginForm.password"
              placeholder="密码"
              show-password
              size="large"
            >
              <template #prefix>
                <el-icon><Lock /></el-icon>
              </template>
            </el-input>
          </el-form-item>

          <!-- 登录按钮 -->
          <el-button type="primary" class="login-button button-large" @click="handleLogin" :loading="loading">
            登录
          </el-button>
        </el-form>

        <!-- 底部操作提示 -->
        <div class="login-footer">
          <el-button text class="footer-link" @click="handleForgotPassword" color="#000">
            忘记密码
            <el-icon><TopRight /></el-icon>
          </el-button>
          <el-button text class="footer-link" @click="goToRegister" color="#000">
            账号注册
            <el-icon><TopRight /></el-icon>
          </el-button>
        </div>
      </div>
    </div>

    <!-- 底部信息 -->
    <div class="footer-info">
      Hiraumi Project 2024
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { User, Lock, TopRight } from "@element-plus/icons-vue";

export default {
  name: "LoginPage",
  components: { User, Lock, TopRight },
  data() {
    return {
      loginForm: {
        username: "",
        password: "",
      },
      loading: false,
    };
  },
  methods: {
    async handleLogin() {
      if (!this.loginForm.username || !this.loginForm.password) {
        this.$message.error("请输入用户名和密码！");
        return;
      }

      // 开启加载状态
      this.loading = true;

      try {
        // 发送登录请求到后端
        const response = await axios.post("http://127.0.0.1:8000/login", {
          email: this.loginForm.username, // 注意后端使用 email 字段
          password: this.loginForm.password,
        });

        console.log("后端返回的数据:", response.data);
        const { username, role } = response.data; // 获取用户名和角色信息

        // 登录成功
        this.$message.success("登录成功，欢迎回来！");
        console.log("用户名:", response.data.username);

        // 存储用户名和角色到 localStorage
        localStorage.setItem("username", username);
        localStorage.setItem("userId", response.data.id);
        localStorage.setItem("role", role);

        // 清空表单数据
        this.loginForm.username = "";
        this.loginForm.password = "";

        // 根据角色跳转页面
        if (role === "教师") {
          this.$router.push("/mainpage-staff");
        } else {
          this.$router.push("/mainpage");
        }
      } catch (error) {
        // 登录失败的处理
        if (error.response) {
          const status = error.response.status;
          if (status === 404) {
            this.$message.error("用户不存在，请注册后再尝试！");
          } else if (status === 401) {
            this.$message.error("密码错误，请重新输入！");
          } else {
            this.$message.error(error.response.data.error || "登录失败，请稍后重试！");
          }
        } else {
          this.$message.error("无法连接到服务器，请检查网络连接！");
        }
      } finally {
        // 关闭加载状态
        this.loading = false;
      }
    },
    handleForgotPassword() {
      this.$message.info("忘记密码功能待实现");
      console.log("点击了忘记密码");
    },
    goToRegister() {
      // 跳转到注册页面
      this.$router.push("/register");
    },
  },
};
</script>

<style scoped>
/* 页面背景 */
.login-page {
  display: flex;
  flex-direction: row;
  height: 100vh;
  background-color: #5a7f75; /* 页面整体背景色 */
  font-family: "PingFang SC", "Microsoft YaHei", Helvetica, Arial, sans-serif;
  color: #fff;
  position: relative;
}

/* 左侧 LOGO 样式 */
.logo-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.logo {
  max-width: 450px;
  margin-bottom: 10px;
}

/* 登录区域包裹层 */
.login-wrapper {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 右侧登录区域 */
.login-container {
  width: 400px; /* 登录框宽度 */
  padding: 40px;
  background-color: #2d3a3a; /* 登录框背景色 */
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.login-title {
  font-size: 24px;
  margin-bottom: 20px;
  text-align: left;
}

.login-form {
  width: 100%;
}


.login-button {
  width: 100%;
  background-color: #5a7f75;
  border-color: #5a7f75;
}

.login-button:hover {
  background-color: #4d6c66;
}

.button-large {
  height: 50px; /* 按钮高度 */
  font-size: 16px; /* 按钮字体大小 */
  line-height: 50px;
}

.login-footer {
  margin-top: 20px;
  display: flex;
  justify-content: left;
  gap: 20px;
}

.footer-link {
  color: #ffffff;
  text-decoration: none;
  font-size: 14px;
}

.footer-link:hover {
  color: #5a7f75;
}

.footer-info {
  position: absolute;
  bottom: 20px; /* 距离底部距离 */
  left: 50%;
  transform: translateX(-50%);
  font-size: 12px;
  color: #ffffff;
  text-align: center;
}
</style>