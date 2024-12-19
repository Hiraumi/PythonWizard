<template>
  <div class="register-page">
    <!-- 左侧 LOGO 区域 -->
    <div class="logo-container">
      <img src="@/assets/logo.png" alt="Python Wizard Logo" class="logo" />
    </div>

    <!-- 右侧注册区域 -->
    <div class="register-wrapper">
      <div class="register-container">
        <h2 class="register-title">注册</h2>
        <el-form
            ref="registerForm"
            :model="registerForm"
            :rules="rules"
            class="register-form"
            inline-message
        >
          <!-- 用户名输入框 -->
          <el-form-item prop="username">
            <el-input
              v-model="registerForm.username"
              placeholder="用户名"
              clearable
              size="large"
            >
              <template #prefix>
                <el-icon><User /></el-icon>
              </template>
            </el-input>
          </el-form-item>

          <!-- 电子邮箱输入框 -->
          <el-form-item prop="email">
            <el-input
              v-model="registerForm.email"
              placeholder="电子邮箱"
              clearable
              size="large"
            >
              <template #prefix>
                <el-icon><Message /></el-icon>
              </template>
            </el-input>
          </el-form-item>

          <!-- 密码输入框 -->
          <el-form-item prop="password">
            <el-input
              v-model="registerForm.password"
              placeholder="密码"
              clearable
              type="password"
              show-password
              size="large"
            >
              <template #prefix>
                <el-icon><Key /></el-icon>
              </template>
            </el-input>
          </el-form-item>

          <!-- 确认密码输入框 -->
          <el-form-item prop="confirmPassword">
            <el-input
              v-model="registerForm.confirmPassword"
              placeholder="密码确认"
              clearable
              type="password"
              show-password
              size="large"
            >
              <template #prefix>
                <el-icon><Key /></el-icon>
              </template>
            </el-input>
          </el-form-item>

          <!-- 身份选择 -->
          <el-form-item prop="role">
            <el-select
              v-model="registerForm.role"
              placeholder="身份"
              size="large"
            >
              <el-option label="学生" value="学生"></el-option>
              <el-option label="教师" value="教师"></el-option>
              <!-- 实际使用时在上面标签增加属性 disabled -->
            </el-select>
          </el-form-item>

          <!-- 注册按钮 -->
          <el-button type="primary" class="register-button button-large" @click="handleRegister">
            注册
          </el-button>
        </el-form>

        <!-- 返回登录页按钮 -->
        <div>
          <el-button class="back-to-login" text @click="goToLogin" color="#000">
            <el-icon><Back /></el-icon>返回登录页
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
import { User, Message, Key, Back } from "@element-plus/icons-vue";

export default {
  name: "RegisterPage",
  components: { User, Message, Key, Back },
  data() {
    return {
      registerForm: {
        username: "",
        email: "",
        password: "",
        confirmPassword: "",
        role: "",
      },
      rules: {
        username: [{ required: true, message: "请输入用户名", trigger: "blur" }],
        email: [
          { required: true, message: "请输入电子邮箱", trigger: "blur" },
          { type: "email", message: "电子邮箱格式不正确", trigger: ["blur", "change"] },
        ],
        password: [{ required: true, message: "请输入密码", trigger: "blur" }],
        confirmPassword: [
          { required: true, message: "请确认密码", trigger: "blur" },
          {
            validator: (rule, value, callback) => {
              if (value !== this.registerForm.password) {
                callback(new Error("两次密码输入不一致"));
              } else {
                callback();
              }
            },
            trigger: "blur",
          },
        ],
        role: [{ required: true, message: "请选择身份", trigger: "change" }],
      },
    };
  },
  methods: {
    async handleRegister() {
      this.$refs.registerForm.validate(async (valid) => {
        if (valid) {
          try {
            // 发送注册请求到后端
            const response = await axios.post("http://127.0.0.1:8000/register", {
              username: this.registerForm.username,
              email: this.registerForm.email,
              password: this.registerForm.password,
              role: this.registerForm.role,
            });
            this.$message.success(response.data.message);
            this.$router.push("/"); // 跳转到登录页
          } catch (error) {
            const errorMessage = error.response?.data?.error || "注册失败";
            this.$message.error(errorMessage);
          }
        } else {
          this.$message.error("请填写完整的注册信息");
        }
      });
    },
    goToLogin() {
      this.$router.push("/"); // 返回登录页，需路由配置
    },
  },
};
</script>

<style scoped>
/* 页面背景 */
.register-page {
  display: flex;
  height: 100vh;
  background-color: #5a7f75;
  font-family: "PingFang SC", "Microsoft YaHei", Helvetica, Arial, sans-serif;
  color: #fff;
  position: relative;
}

/* 左侧 LOGO 区域 */
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

/* 右侧注册区域 */
.register-wrapper {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.register-container {
  width: 400px;
  padding: 40px;
  background-color: #2d3a3a;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.register-title {
  font-size: 24px;
  margin-bottom: 20px;
  text-align: left;
}

.register-form {
  width: 100%;
}

/* 调整输入框与标签的间距 */
.register-form .el-form-item {
  margin-bottom: 10px; /* 减小间距 */
}

.register-form .el-form-item .el-form-item__label {
  color: #ffffff; /* 标签文字颜色设为白色 */
  margin-bottom: 5px; /* 标签与文本框之间的间距 */
  font-size: 14px; /* 可根据需要调整字体大小 */
}

.register-button {
  width: 100%;
  background-color: #5a7f75;
  border-color: #5a7f75;
}

.register-button:hover {
  background-color: #4d6c66;
}

.button-large {
  height: 50px; /* 按钮高度 */
  font-size: 16px; /* 按钮字体大小 */
  line-height: 50px;
}

.back-to-login {
  text-align: left;
  margin-top: 20px;
  text-decoration: none;
  font-size: 14px;
}

.back-to-login:hover {
  color: #5a7f75;
}

.back-to-login .el-button {
  color: #ffffff; /* 文字颜色设为白色 */
  font-size: 14px;
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