<template>
  <div>
    <h1>用户管理</h1>
    <!-- 表格组件 -->
    <el-table
      :data="users"
      border
      style="width: 100%; margin-top: 20px;"
      v-loading="loading"
      stripe
    >
      <!-- ID 列 -->
      <el-table-column prop="id" label="ID" width="80" align="center" sortable/>

      <!-- 用户名列 -->
      <el-table-column prop="username" label="用户名" align="center">
        <template #default="scope">
          <!-- 显示用户名 -->
          <span>{{ scope.row.username }}</span>

          <!-- Edit 图标与 Popover -->
          <el-popover
            :visible="visiblePopover.id === scope.row.id && visiblePopover.type === 'username'"
            title="修改用户名"
            width="200"
          >
            <div>
              <el-input
                v-model="newUsername"
                placeholder="请输入新用户名"
                size="small"
                style="margin-bottom: 10px;"
              />
              <div style="text-align: right;">
                <el-button size="default" type="primary" @click="updateUsername(scope.row)">确认</el-button>
                <el-button size="default" @click="cancelPopover">返回</el-button>
              </div>
            </div>
            <template #reference>
              <el-icon class="edit-icon" @click.stop="showPopover(scope.row, 'username')">
                <Edit />
              </el-icon>
            </template>
          </el-popover>
        </template>
      </el-table-column>

      <!-- 邮箱列 -->
      <el-table-column prop="email" label="邮箱" align="center">
        <template #default="scope">
          <span>{{ scope.row.email }}</span>
          <el-popover
            :visible="visiblePopover.id === scope.row.id && visiblePopover.type === 'email'"
            title="修改邮箱"
            width="200"
          >
            <div>
              <el-input
                v-model="newEmail"
                placeholder="请输入新邮箱"
                size="small"
                style="margin-bottom: 10px;"
              />
              <div style="text-align: right;">
                <el-button size="default" type="primary" @click="updateEmail(scope.row)">确认</el-button>
                <el-button size="default" @click="cancelPopover">返回</el-button>
              </div>
            </div>
            <template #reference>
              <el-icon class="edit-icon" @click.stop="showPopover(scope.row, 'email')">
                <Edit />
              </el-icon>
            </template>
          </el-popover>
        </template>
      </el-table-column>

      <!-- 密码列 -->
      <el-table-column prop="password" label="加密密码" align="center">
        <template #default="scope">
          <el-tooltip
            class="item"
            effect="light"
            placement="top"
            :content="scope.row.password"
          >
            <span class="password-overflow">
              {{ scope.row.password }}
            </span>
          </el-tooltip>
          <el-popover
            :visible="visiblePopover.id === scope.row.id && visiblePopover.type === 'password'"
            title="修改密码"
            width="300"
          >
            <div>
              <el-input
                v-model="newPassword"
                type="password"
                placeholder="请输入新密码"
                size="small"
                style="margin-bottom: 10px;"
              />
              <div style="text-align: right;">
                <el-button size="default" type="primary" @click="updatePassword(scope.row)">确认</el-button>
                <el-button size="default" @click="cancelPopover">返回</el-button>
              </div>
            </div>
            <template #reference>
              <el-icon class="edit-icon" @click.stop="showPopover(scope.row, 'password')">
                <Edit />
              </el-icon>
            </template>
          </el-popover>
        </template>
      </el-table-column>

      <!-- 角色列 -->
      <el-table-column
        prop="role"
        label="角色"
        align="center"
        :filters="[
          { text: '教师', value: '教师' },
          { text: '学生', value: '学生' }
        ]"
        :filter-method="filterRole"
      >
        <template #default="scope">
          <el-tag
            :type="scope.row.role === '教师' ? 'success' : 'info'"
            effect="light"
          >
            {{ scope.row.role }}
          </el-tag>

          <!-- 编辑角色 Popover -->
          <el-popover
            :visible="visiblePopover.id === scope.row.id && visiblePopover.type === 'role'"
            title="修改角色"
            width="200"
          >
            <div>
              <p>是否将角色替换为 {{ scope.row.role === '教师' ? '学生' : '教师' }}？</p>
              <div style="text-align: right;">
                <el-button size="default" type="primary" @click="updateRole(scope.row)">确认</el-button>
                <el-button size="default" @click="cancelPopover">取消</el-button>
              </div>
            </div>
            <template #reference>
              <el-icon class="edit-icon" @click.stop="showPopover(scope.row, 'role')">
                <Edit />
              </el-icon>
            </template>
          </el-popover>
        </template>
      </el-table-column>

      <!-- 操作列 -->
      <el-table-column label="操作" width="120" align="center">
        <template #default="scope">
          <!-- 删除按钮 -->
          <el-tooltip
            v-if="scope.row.username === currentUsername"
            content="不能删除自己的账户"
            effect="light"
            placement="top"
          >
            <el-button
              size="default"
              type="danger"
              :disabled="scope.row.username === currentUsername"
            >
              删除
            </el-button>
          </el-tooltip>
          <el-button
            v-else
            size="default"
            type="danger"
            @click="deleteUser(scope.row)"
          >
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页控件 -->
    <el-pagination
      background
      style="margin-top: 20px;"
      :current-page="pagination.currentPage"
      :page-size="pagination.pageSize"
      :total="pagination.total"
      :page-sizes="[10, 20, 50]"
      layout="total, sizes, prev, pager, next, jumper"
      @size-change="handleSizeChange"
      @current-change="handlePageChange"
    />
  </div>

  <!-- 确认删除对话框 -->
  <el-dialog
    title="确认删除"
    v-model:visible="deleteDialogVisible"
    width="400px"
    :close-on-click-modal="false"
  >
    <p>确定要删除用户 <b>{{ userToDelete.username }}</b> 吗？</p>
    <p style="color: orangered; font-weight: bold;">此操作不可撤销，请慎重！</p>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="deleteDialogVisible = false">取消</el-button>
        <el-button type="danger" @click="confirmDeleteUser">确认删除</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<style>
  .password-overflow {
    display: inline-block;
    max-width: 100px; /* 设置最大宽度 */
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis; /* 显示省略号 */
    vertical-align: middle; /* 对齐图标 */
  }

  .edit-icon {
    cursor: pointer;
    margin-left: 10px; /* 图标与文本的间距 */
    vertical-align: middle;
  }
</style>

<script>
import { Edit } from "@element-plus/icons-vue";
import axios from "axios";

export default {
  name: "StaffDashboard",
  components: { Edit },
  data() {
    return {
      users: [], // 用户数据
      loading: false, // 表格加载状态
      pagination: {
        currentPage: 1,
        pageSize: 10,
        total: 0, // 总数据量（需要从后端获取）
      },
      visiblePopover: {},
      newUsername: "", // 存储新用户名
      newEmail: "", // 存储新邮箱
      newPassword: "", // 存储新密码
      currentUsername: localStorage.getItem("username") || "", // 当前登录用户名
      deleteDialogVisible: false, // 删除对话框显示状态
      userToDelete: null, // 待删除的用户信息
    };
  },
  methods: {
    // 点击删除按钮时，弹出确认对话框
    deleteUser(user) {
      this.userToDelete = user; // 记录需要删除的用户
      this.deleteDialogVisible = true; // 显示确认对话框
    },

    // 确认删除用户
    confirmDeleteUser() {
      if (!this.userToDelete || !this.userToDelete.username) {
        this.$message.error("无法找到需要删除的用户！");
        return;
      }

      // 调用后端删除接口
      axios
        .delete(`http://127.0.0.1:8000/delete_user/${this.userToDelete.username}`)
        .then(() => {
          this.$message.success(`用户 ${this.userToDelete.username} 已成功删除！`);
          this.fetchUsers(); // 重新加载用户数据
        })
        .catch((error) => {
          console.error("删除用户失败:", error);
          this.$message.error("删除失败，请稍后重试！");
        })
        .finally(() => {
          this.deleteDialogVisible = false; // 关闭对话框
          this.userToDelete = null; // 清空待删除用户信息
        });
    },

    // 页数变化
    handlePageChange(page) {
      this.pagination.currentPage = page;
      this.fetchUsers(); // 更新表格数据
    },

    // 每页大小变化
    handleSizeChange(size) {
      this.pagination.pageSize = size;
      this.fetchUsers(); // 更新表格数据
    },

    // 获取用户数据
    fetchUsers() {
      this.loading = true;
      setTimeout(() => {
        // 调用后端接口
        axios
        .get("http://127.0.0.1:8000/users", {
          params: {
            page: this.pagination.currentPage,
            page_size: this.pagination.pageSize,
          },
        })
        .then((response) => {
          const { users, total } = response.data;

          // 更新表格数据和分页总数
          this.users = users;
          this.pagination.total = total;
        })
        .catch((error) => {
          console.error("获取用户数据失败:", error);
          this.$message.error("无法获取用户数据，请稍后重试！");
        })
        .finally(() => {
          this.loading = false;
        });
      }, 500);
    },

    // 角色筛选逻辑
    filterRole(value, row) {
      return row.role === value;
    },

    // 显示指定行的 Popover
    showPopover(row, type) {
      console.log("当前行数据:", row); // 调试输出当前行数据
      this.visiblePopover = { id: row.id, type: type }; // 设置当前行和类型
      if (type === "username") {
        this.newUsername = row.username || ""; // 初始化用户名
      } else if (type === "email") {
        this.newEmail = row.email || ""; // 初始化邮箱
      } else if (type === "role") {
        this.currentRow = row; // 设置当前行，供角色切换使用
      }
    },

    // 关闭 Popover
    cancelPopover() {
      this.visiblePopover = {}; // 清空状态
    },

    // 确认用户名修改
    async updateUsername(row) {
      if (!this.newUsername || this.newUsername.trim() === "") {
        this.$message.error("用户名不能为空！");
        return;
      }

      try {
        const response = await axios.put("http://127.0.0.1:8000/update_username", {
          current_username: row.username, // 当前用户名
          new_username: this.newUsername, // 新用户名
        });
        this.$message.success(response.data.message || "用户名更新成功！");
        this.cancelPopover(); // 关闭 Popover
        this.fetchUsers(); // 刷新用户数据
      } catch (error) {
        console.error("用户名更新失败:", error.response?.data || error);
        this.$message.error(
          error.response?.data?.error || "用户名更新失败，请稍后重试！"
        );
      }
    },

    // 确认邮箱修改
    async updateEmail(row) {
      if (!this.newEmail || this.newEmail.trim() === "") {
        this.$message.error("邮箱不能为空！");
        return;
      }

      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(this.newEmail)) {
        this.$message.error("请输入有效的邮箱地址！");
        return;
      }

      try {
        const response = await axios.put("http://127.0.0.1:8000/update_email", {
          current_username: row.username, // 当前用户名
          new_email: this.newEmail, // 新邮箱
        });
        this.$message.success(response.data.message || "邮箱更新成功！");
        this.cancelPopover(); // 关闭 Popover
        this.fetchUsers(); // 刷新用户数据
      } catch (error) {
        console.error("邮箱更新失败:", error.response?.data || error);
        this.$message.error(
          error.response?.data?.error || "邮箱更新失败，请稍后重试！"
        );
      }
    },

    // 更新角色
    async updateRole(row) {
      const newRole = row.role === "教师" ? "学生" : "教师"; // 切换角色

      try {
        const response = await axios.put("http://127.0.0.1:8000/update_role", {
          current_username: row.username, // 当前用户名
          role: newRole, // 新角色
        });
        this.$message.success(response.data.message || "角色更新成功！");
        this.cancelPopover(); // 关闭 Popover
        this.fetchUsers(); // 刷新用户数据
      } catch (error) {
        console.error("角色更新失败:", error.response?.data || error);
        this.$message.error(
          error.response?.data?.error || "角色更新失败，请稍后重试！"
        );
      }
    },

    // 更新密码
    async updatePassword(row) {
      if (!this.newPassword || this.newPassword.trim() === "") {
        this.$message.error("密码不能为空！");
        return;
      }

      try {
        const response = await axios.put("http://127.0.0.1:8000/update_password", {
          current_username: row.username, // 当前用户名
          new_password: this.newPassword, // 新密码
        });
        this.$message.success(response.data.message || "密码更新成功！");
        this.cancelPopover(); // 关闭 Popover
        this.fetchUsers(); // 刷新用户数据
      } catch (error) {
        console.error("密码更新失败:", error.response?.data || error);
        this.$message.error(
          error.response?.data?.error || "密码更新失败，请稍后重试！"
        );
      }
    },
  },
  mounted() {
    this.fetchUsers(); // 初始化获取用户数据
  },
};
</script>

<style scoped>
h1 {
  color: #5a7f75;
}

.edit-icon {
  margin-left: 8px;
  cursor: pointer;
  color: #5a7f75;
}

.edit-icon:hover {
  color: #405650;
}
</style>