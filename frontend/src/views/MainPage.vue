<template>
  <el-container class="main-page">
    <!-- 顶部标题栏 -->
    <el-header class="header">
      <div class="header-left">
        <img src="@/assets/logo_mini.png" alt="Logo" class="logo" />
      </div>
      <div class="header-right">
        <span class="username">你好，{{ username }}同学！</span>
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
          <el-menu-item index="/mainpage/dashboard">
            <el-icon><Grid /></el-icon>
            <span>Dashboard</span>
          </el-menu-item>
          <el-menu-item index="/mainpage/courses">
            <el-icon><Notebook /></el-icon>
            <span>课程学习</span>
          </el-menu-item>
          <el-menu-item index="/mainpage/coding">
            <el-icon><Edit /></el-icon>
            <span>程序编写</span>
          </el-menu-item>
          <el-menu-item index="/mainpage/exams">
            <el-icon><Document /></el-icon>
            <span>考试内容</span>
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
import { Grid, Notebook, Edit, Document } from '@element-plus/icons-vue';

export default {
  name: 'MainPage',
  components: {
    Grid,
    Notebook,
    Edit,
    Document,
  },
  data() {
    return {
      username: localStorage.getItem("username"),
      isCollapse: false, // 侧边栏折叠状态
      activeMenu: '/dashboard', // 默认选中的菜单
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
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  background-color: #5a7f75;
  color: #fff;
  font-size: 16px;
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
  background-color: #E5EDEB;
  color: #333;
  position: relative;
}

.collapse-btn {
  position: absolute;
  bottom: 10px;
  left: 50%;
  transform: translateX(-50%);
}

.main {
  background-color: #f0f2f5;
  padding: 20px;
}
</style>