<template>
  <div>
    <!-- 大标题 -->
    <h2>程序编写</h2>
    <el-alert title="请注意不要将浏览器宽度调太窄(；´Д｀)" type="warning" show-icon />

    <!-- 聚焦部分 -->
    <section style="margin-top: 20px;">
      <h3>
        <el-icon style="margin-right: 8px;">
          <Aim/>
        </el-icon>
        聚焦
      </h3>

      <!-- 卡片容器 -->
      <div class="card-container">
        <!-- 卡片 1 -->
        <el-card shadow="always" class="custom-card" @click="goToOnCoding">
          <el-icon style="font-size: 36px; color: #5a7f75; margin-bottom: 10px;">
            <Edit/>
          </el-icon>
          <h3>Wizard Playground</h3>
          <p>点击进入自由编程，无指定条件</p>
        </el-card>

        <!-- 卡片 2 -->
        <el-card shadow="always" class="custom-card">
          <!-- 完成百分比 -->
          <div style="font-size: 36px; color: #5a7f75; margin-bottom: 10px; font-weight: bold">
            <span>{{ Math.floor((27 / 50) * 100) }}</span>
            <span style="font-size: 24px;">%</span>
          </div>
          <!-- 说明文字 -->
          <h3>当前进度</h3>
          <p>练习进度：27/50，请继续加油ʕ•ᴥ•ʔ</p>
          <!-- 进度条 -->
          <el-progress
            :percentage="Math.floor((27 / 50) * 100)"
            striped
            status="success"
            :stroke-width="12"
            color="#5a7f75"
          />
        </el-card>

        <!-- 卡片 3 -->
        <el-card shadow="always" class="custom-card">
          <el-icon style="font-size: 36px; color: #5a7f75; margin-bottom: 10px;">
            <Guide/>
          </el-icon>
          <h3>快速继续</h3>
          <p>点击继续练习#28</p>
        </el-card>
      </div>
    </section>

    <!-- 练习列表 -->
    <section style="margin-top: 40px;">
      <h3>
        <el-icon style="margin-right: 8px;">
          <List/>
        </el-icon>
        全部练习
      </h3>
      <el-alert
        title="练习说明"
        type="info"
        description="【开始练习】是从题库中抽取问题练习，而【智能练习】由AI生成问题练习"
        show-icon
        style="margin-bottom: 15px;"
      />
      <el-table :data="exerciseList" style="width: 100%; max-width: 2000px;" border>
        <el-table-column prop="id" label="编号" width="80"/>
        <el-table-column prop="name" label="练习名"/>
        <el-table-column prop="tags" label="知识点" width="200">
          <template #default="scope">
            <el-tag type="info" v-for="tag in scope.row.tags" :key="tag" style="margin-right: 10px;">{{ tag }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <!-- 如果 status 为 1 -->
            <div v-if="scope.row.status === 1" style="display: flex; align-items: center;">
              <el-icon style="color: #67C23A; margin-right: 5px;">
                <CircleCheck />
              </el-icon>
              <span style="color: #000;">完成</span>
            </div>
            <!-- 如果 status 为 0 -->
            <div v-else style="display: flex; align-items: center;">
              <el-icon style="color: #E6A23C; margin-right: 5px;">
                <WarningFilled />
              </el-icon>
              <span style="color: #000; font-weight: bold;">未完成</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="300">
          <template #default="scope">
            <el-button type="primary" color="#5a7f75" @click="goToExercise(scope.row.id, 1)">
              <el-icon>
                <TopRight/>
              </el-icon>
              开始练习
            </el-button>
            <el-button type="primary" style="margin-left: 8px;" @click="goToExercise(scope.row.id, 2)">
              <el-icon>
                <MagicStick/>
              </el-icon>
              智能练习
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
          style="margin-top: 20px;"
          background
          layout="prev, pager, next"
          :current-page="currentPage"
          :page-size="pageSize"
          :total="exerciseTotal"
          @current-change="handlePageChange"
      />
    </section>
  </div>
</template>

<script>
import {Aim, CircleCheck, Edit, Guide, List, MagicStick, TopRight, WarningFilled} from '@element-plus/icons-vue';

export default {
  name: "AppCoding",
  components: {WarningFilled, CircleCheck, Guide, MagicStick, TopRight, Aim, Edit, List},
  data() {
    return {
      exerciseList: [
        // 示例练习数据
        {id: 1, name: "基础语法入门", tags: ["基础", "语法"], status: 1},
        {id: 2, name: "条件语句练习", tags: ["条件", "逻辑"], status: 1},
        {id: 3, name: "循环语句", tags: ["循环", "逻辑"], status: 1},
        {id: 4, name: "函数定义与调用", tags: ["函数", "封装"], status: 1},
        {id: 5, name: "字符串处理", tags: ["字符串", "操作"], status: 1},
        {id: 6, name: "文件操作基础", tags: ["文件", "基础"], status: 1},
        {id: 7, name: "数据结构", tags: ["数据结构", "算法"], status: 1},
        {id: 8, name: "排序算法", tags: ["算法", "排序"], status: 0},
        {id: 9, name: "面向对象编程", tags: ["面向对象", "设计"], status: 0},
        {id: 10, name: "异常处理", tags: ["错误", "异常"], status: 0},
      ],
      exerciseTotal: 50, // 总练习数
      currentPage: 1, // 当前页码
      pageSize: 10, // 每页练习数
    };
  },
  methods: {
    // 跳转到编程页面
    goToOnCoding() {
      this.$router.push("/mainpage/oncoding");
    },

    // 跳转到 Playground
    goToPlayground() {
      this.$message.info("跳转到 Playground！");
      // TODO: 添加实际跳转逻辑
    },
    // 跳转到练习
    goToExercise(id, type) {
      this.$message.success(`进入练习 ${type}（编号 ${id}）`);
      // TODO: 添加实际跳转逻辑
    },
    // 分页改变
    handlePageChange(page) {
      this.currentPage = page;
      // TODO: 更新当前页面练习数据
    },
  },
};
</script>

<style scoped>
h2 {
  font-size: 24px;
  color: #333;
}

h3 {
  font-size: 20px;
  color: #5a7f75;
  margin-bottom: 10px;
}

.card-container {
  display: flex;
  justify-content: space-between; /* 卡片均匀分布 */
  gap: 20px; /* 卡片之间的间距 */
  margin-top: 20px;
}

.custom-card {
  flex: 1; /* 让卡片自动均分宽度 */
  max-width: 400px;
  text-align: left;
  cursor: pointer;
  padding: 20px;
  transition: 0.3s;
}

.custom-card:hover {
  transform: translateY(-5px); /* 鼠标悬停动画 */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}
</style>