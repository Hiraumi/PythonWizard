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
                <el-button size="default" type="primary" @click="confirmUsernameChange">确认</el-button>
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
                <el-button size="default" type="primary" @click="confirmEmailChange">确认</el-button>
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
      <el-table-column prop="password" label="加密密码" align="center" show-overflow-tooltip/>

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
                <el-button size="default" type="primary" @click="confirmRoleChange">确认</el-button>
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
      currentUsername: localStorage.getItem("username") || "", // 当前登录用户名
      deleteDialogVisible: false, // 删除对话框显示状态
      userToDelete: null, // 待删除的用户信息
    };
  },
  methods: {
    // 编辑用户信息
    editUser(user, field) {
      if (field === "role") {
        // 弹出对话框，显示当前角色
        this.$confirm(`修改用户 ${user.username} 的角色`, "确认修改", {
          confirmButtonText: "确认",
          cancelButtonText: "取消",
          type: "warning",
          inputPlaceholder: "请选择新角色",
          inputType: "radio",
          inputValidator: (value) => {
            if (value === "") {
              return "请选择一个角色";
            }
            return true;
          },
          inputOptions: {
            teacher: "教师",
            student: "学生",
          },
        })
          .then(({ value }) => {
            // 确认修改时调用后端接口
            axios
              .put("http://127.0.0.1:8000/update_user", {
                current_username: user.username, // 当前用户的用户名
                role: value, // 新角色
              })
              .then(() => {
                this.$message.success(`用户 ${user.username} 的角色已修改为 ${value}`);
                this.fetchUsers(); // 重新获取用户数据
              })
              .catch((error) => {
                console.error("修改角色失败:", error);
                this.$message.error("修改角色失败，请稍后重试！");
              });
          })
          .catch(() => {
            this.$message.info("已取消修改角色操作");
          });
      } else {
        this.$message.warning("暂不支持修改其他字段！");
      }
    },

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
      this.visiblePopover = { id: row.id, username: row.username, type: type }; // 唯一标识符
      this.currentRow = row; // 赋值当前行数据
      this.newUsername = row.username || "";
      this.newEmail = row.email || "";
    },

    // 关闭 Popover
    cancelPopover() {
      this.visiblePopover = {}; // 清空状态
    },

    // 确认用户名修改
    confirmUsernameChange() {
      if (!this.currentRow || !this.currentRow.username) {
        console.log("当前行数据:", this.currentRow); // 调试输出
        this.$message.error("操作失败，未找到用户信息！");
        return;
      }

      if (!this.newUsername.trim()) {
        this.$message.error("新用户名不能为空！");
        return;
      }
      // 发送请求到后端
      axios
        .put("http://127.0.0.1:8000/update_user", {
          current_username: this.currentRow.username,    // 用户ID
          new_username: this.newUsername // 新用户名
        })
        .then(() => {
          this.$message.success("用户名更新成功！");
          this.cancelPopover(); // 关闭 Popover
          this.fetchUsers();    // 重新获取用户数据
        })
        .catch((error) => {
          console.error("用户名更新失败:", error);
          this.$message.error("更新失败，请稍后再试！");
        });
    },

    // 确认邮箱修改
    confirmEmailChange() {
        if (!this.currentRow || !this.currentRow.username) {
          console.log("当前行数据:", this.currentRow); // 调试输出
          this.$message.error("操作失败，未找到用户信息！");
          return;
        }

      if (!this.newEmail.trim()) {
        this.$message.error("新邮箱不能为空！");
        return;
      }
      // 发送请求到后端
      axios
        .put("http://127.0.0.1:8000/update_user", {
          current_username: this.currentRow.username,
          new_email: this.newEmail     // 新邮箱
        })
        .then(() => {
          this.$message.success("邮箱更新成功！");
          this.cancelPopover(); // 关闭 Popover
          this.fetchUsers();    // 重新获取用户数据
        })
        .catch((error) => {
          console.error("邮箱更新失败:", error);
          this.$message.error("更新失败，请稍后再试！");
        });
    },

    confirmRoleChange() {
      if (!this.currentRow || !this.currentRow.username) {
        console.log("当前行数据:", this.currentRow); // 调试输出
        this.$message.error("操作失败，未找到用户信息！");
        return;
      }

      // 判断角色是否需要修改
      const newRole = this.currentRow.role === "教师" ? "学生" : "教师";
      if (!newRole) {
        this.$message.error("未选择新的角色！");
        return;
      }

      // 发送请求到后端
      axios
        .put("http://127.0.0.1:8000/update_user", {
          current_username: this.currentRow.username, // 当前用户名
          role: newRole, // 新角色
        })
        .then(() => {
          this.$message.success(`角色更新成功！${this.currentRow.username} 的新角色为 ${newRole}`);
          this.cancelPopover(); // 关闭 Popover
          this.fetchUsers(); // 重新获取用户数据
        })
        .catch((error) => {
          console.error("角色更新失败:", error);
          this.$message.error("更新失败，请稍后再试！");
        });
    }
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