<template>
  <el-container class="main-page">
    <!-- 顶部标题栏 -->
    <el-header class="header">
      <div class="header-left">
        <img src="@/assets/logo_mini.png" alt="Logo" class="logo" />
      </div>
      <div class="header-right">
        <span class="username">你好，{{ username }}老师！</span>
        <el-button color="#fff" size="small" @click="logout">退出登录</el-button>
      </div>
    </el-header>

    <!-- 主体部分 -->
    <el-container>
      <!-- 左侧侧边栏 -->
      <el-aside :width="isCollapse ? '64px' : '200px'" class="aside">
        <el-menu
          :default-active="activeMenu"
          class="el-menu-vertical-demo"
          background-color="#E5EDEB"
          text-color="#333"
          active-text-color="#5a7f75"
          :collapse="isCollapse"
          router
        >
          <el-menu-item index="/mainpage-staff/dashboard">
            <el-icon><Grid /></el-icon>
            <span>Dashboard</span>
          </el-menu-item>
          <el-menu-item index="/mainpage-staff/user-management">
            <el-icon><User /></el-icon>
            <span>用户管理</span>
          </el-menu-item>
        </el-menu>
        <!-- 折叠按钮 -->
        <el-button
          class="collapse-btn"
          size="small"
          circle
          @click="toggleCollapse"
        >
          <el-icon>
            <template v-if="isCollapse">
              <Expand />
            </template>
            <template v-else>
              <Fold />
            </template>
          </el-icon>
        </el-button>
      </el-aside>

      <!-- 右侧主区域 -->
      <el-main class="main">
        <router-view /> <!-- 根据路由显示不同的子页面 -->
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import { Grid, User, Expand, Fold } from '@element-plus/icons-vue';

export default {
  name: 'MainPageStaff',
  components: {
    Grid,
    User,
    Expand,
    Fold,
  },
  data() {
    return {
      username: localStorage.getItem("username"),
      isCollapse: false, // 侧边栏折叠状态
      activeMenu: '/mainpage-staff/dashboard', // 默认选中的菜单
    };
  },
  methods: {
    toggleCollapse() {
      this.isCollapse = !this.isCollapse;
    },
    logout() {
      this.$message.success('成功登出');
      this.$router.push('/'); // 返回登录页面
    },
  },
};
</script>

<style scoped>
.main-page {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 64px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  background-color: #5a7f75;
  color: #fff;
  font-size: 16px;
  z-index: 1000;
}

.header-left {
  display: flex;
  align-items: center;
}

.logo {
  height: 50px;
  margin-right: 10px;
}

.header-right {
  display: flex;
  align-items: center;
}

.username {
  margin-right: 20px;
}

.aside {
  position: fixed;
  top: 64px;
  left: 0;
  height: calc(100vh - 64px);
  width: 200px;
  background-color: #E5EDEB;
  color: #333;
  z-index: 999;
  transition: width 0.3s;
}

.aside[style*='64px'] {
  width: 64px;
}

.collapse-btn {
  position: absolute;
  bottom: 10px;
  left: 50%;
  transform: translateX(-50%);
}

.main {
  margin-top: 64px;
  margin-left: 200px;
  background-color: #f0f2f5;
  padding: 20px;
  min-height: calc(100vh - 64px);
  transition: margin-left 0.3s;
}

.aside[style*='64px'] + .main{
  margin-top: 64px;
}
</style>