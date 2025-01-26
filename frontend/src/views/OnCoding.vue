<template>
  <div class="on-coding-page">
    <!-- 返回按钮 -->
    <el-button color="#5a7f75" plain class="back-button" @click="goBack">
      <el-icon><ArrowLeft /></el-icon> 返回
    </el-button>

    <!-- 标题与问题描述 -->
    <h2 class="page-title">代码编写</h2>
    <h3 class="question-title"><el-icon><Compass /></el-icon>问题1-1</h3>
    <p class="question-description">问题描述：请在左侧输入代码，右侧查看结果。</p>

    <!-- 两栏布局 -->
    <div class="two-columns">
      <!-- 左侧：代码输入区域 -->
      <div class="left-panel">
        <h3 class="panel-title"><el-icon><EditPen /></el-icon>代码输入</h3>
        <!--TODO: 换成高亮语法的-->
        <el-input
          v-model="codeInput"
          :rows="15"
          type="textarea"
          placeholder="请输入Python代码"
          class="code-input"
        />
        <div class="buttons">
          <el-button-group>
            <el-button color="#5a7f75" @click="handleRun" round>
              <el-icon><CaretRight /></el-icon>运行
            </el-button>
            <el-button color="#5a7f75" plain @click="handleReset" round>
              <el-icon><RefreshLeft /></el-icon>重置
            </el-button>
          </el-button-group>
        </div>
      </div>

      <!-- 右侧：输出区域 -->
      <div class="right-panel">
        <h3 class="panel-title"><el-icon><Tickets /></el-icon>运行结果</h3>
        <el-card>
          <pre class="output">{{ output }}</pre>
        </el-card>
      </div>
    </div>

    <!-- 询问AI区域 -->
    <div>
      <h3 class="panel-title">
        <el-icon><HelpFilled /></el-icon>询问AI
        <el-popover
          placement="top"
          width="400"
          trigger="click"
          title="提示"
        >
          <template #reference>
            <el-icon class="help-icon" style="cursor: pointer; margin-left: 5px;">
              <QuestionFilled />
            </el-icon>
          </template>
          请先选择你需要的帮助类别，再输入一些具体问题（如“为什么这里必须用半角”等；当然也可以不输），点击提交即可获取答案。
        </el-popover>
      </h3>
      <div class="ai-input-row">
        <el-select size="large" placeholder="选择功能" style="width: 200px"></el-select>
        <el-input size="large" placeholder="请输入向AI提问的补充信息（可选）"></el-input>
        <el-button size="large" color="#5a7f75">提交</el-button>
      </div>
    </div>
  </div>
</template>

<script>
import {
  ArrowLeft,
  CaretRight,
  Compass,
  EditPen,
  HelpFilled,
  QuestionFilled,
  RefreshLeft,
  Tickets
} from "@element-plus/icons-vue";

export default {
  name: "OnCoding",
  components: {QuestionFilled, HelpFilled, Compass, EditPen, Tickets, ArrowLeft, CaretRight, RefreshLeft },
  data() {
    return {
      codeInput: "", // 用户输入的代码
      output: "运行结果将在此显示。", // 运行结果
    };
  },
  methods: {
    async handleRun() {
      try {
        this.output = "正在运行代码...";
        const response = await fetch("http://127.0.0.1:8000/run_code", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ code: this.codeInput }),
        });
        const result = await response.json();
        if (response.ok) {
          if (!result.output || result.output.trim() === "") {
            this.output = "运行完成，无输出"; // 如果输出为空，则显示提示信息
          } else {
            this.output = result.output;
          }
        } else {
          this.output = `运行错误: ${result.error}`;
        }
      } catch (error) {
        this.output = `运行错误: ${error.message}`;
      }
    },
    handleReset() {
      this.codeInput = ""; // 清空代码输入框
      this.output = "运行结果将在此显示。";
    },
    goBack() {
      this.$router.push("/mainpage/coding");
    },
  },
};
</script>

<style scoped>
.on-coding-page {
  padding: 20px;
}

.page-title {
  font-size: 24px;
  margin-bottom: 20px;
  color: #333;
}

.two-columns {
  display: flex;
  gap: 10px;
  height: 100%;
}

.left-panel,
.right-panel {
  flex: 1;
}

.left-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 500px; /* 设置最小宽度 */
  max-width: 100%;
  overflow: hidden; /* 防止内容溢出 */
}

.panel-title {
  font-size: 18px;
  margin-bottom: 10px;
  color: #5a7f75;
}

.buttons {
  padding: 10px 0 10px 0;
}

.code-input {
  font-family: Consolas, monospace;
}

.output {
  font-family: monospace;
  font-size: 14px;
  color: #333;
}

.help-icon {
  font-size: 16px;
  color: #5a7f75;
}

.ai-input-row {
  display: flex; /* 使用 Flex 布局 */
  align-items: center; /* 垂直居中 */
  gap: 10px; /* 控件之间的间距 */
}
</style>