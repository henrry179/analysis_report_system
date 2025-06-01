<template>
  <div class="user-management">
    <div class="header">
      <h1>用户管理</h1>
      <div class="header-actions">
        <el-button @click="refreshUsers" :loading="loading">
          <i class="el-icon-refresh"></i> 刷新
        </el-button>
        <el-button type="primary" @click="showCreateUserDialog">
          <i class="el-icon-plus"></i> 新增用户
        </el-button>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-cards">
      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-number">{{ userStats.total_users }}</div>
          <div class="stat-label">总用户数</div>
        </div>
        <i class="el-icon-user stat-icon"></i>
      </el-card>
      
      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-number">{{ userStats.active_users }}</div>
          <div class="stat-label">活跃用户</div>
        </div>
        <i class="el-icon-check stat-icon"></i>
      </el-card>
      
      <el-card class="stat-card">
        <div class="stat-content">
          <div class="stat-number">{{ userStats.recent_logins }}</div>
          <div class="stat-label">最近登录</div>
        </div>
        <i class="el-icon-time stat-icon"></i>
      </el-card>
    </div>

    <!-- 搜索和过滤 -->
    <el-card class="filter-card">
      <div class="filter-row">
        <el-input
          v-model="searchQuery"
          placeholder="搜索用户名或姓名"
          style="width: 300px"
          @change="handleSearch"
        >
          <template #prefix>
            <i class="el-icon-search"></i>
          </template>
        </el-input>
        
        <el-select
          v-model="selectedRole"
          placeholder="选择角色"
          style="width: 150px; margin-left: 10px"
          @change="handleRoleFilter"
        >
          <el-option label="全部角色" value=""></el-option>
          <el-option label="管理员" value="admin"></el-option>
          <el-option label="分析师" value="analyst"></el-option>
          <el-option label="查看者" value="viewer"></el-option>
        </el-select>
      </div>
    </el-card>

    <!-- 用户列表 -->
    <el-card class="table-card">
      <el-table
        :data="users"
        v-loading="loading"
        style="width: 100%"
        @sort-change="handleSortChange"
      >
        <el-table-column prop="id" label="ID" width="80" sortable="custom"></el-table-column>
        <el-table-column prop="username" label="用户名" width="120"></el-table-column>
        <el-table-column prop="full_name" label="姓名" width="150"></el-table-column>
        <el-table-column prop="email" label="邮箱" width="200"></el-table-column>
        <el-table-column prop="role" label="角色" width="100">
          <template #default="scope">
            <el-tag :type="getRoleTagType(scope.row.role)">
              {{ getRoleText(scope.row.role) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="is_active" label="状态" width="80">
          <template #default="scope">
            <el-tag :type="scope.row.is_active ? 'success' : 'danger'">
              {{ scope.row.is_active ? '活跃' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="login_count" label="登录次数" width="100"></el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="160" sortable="custom">
          <template #default="scope">
            {{ formatDate(scope.row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column prop="last_login" label="最后登录" width="160">
          <template #default="scope">
            {{ scope.row.last_login ? formatDate(scope.row.last_login) : '从未登录' }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <el-button size="small" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button
              size="small"
              type="danger"
              @click="handleDelete(scope.row)"
              :disabled="scope.row.username === currentUser.username"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-wrapper">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="pagination.page"
          :page-sizes="[10, 20, 50, 100]"
          :page-size="pagination.size"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pagination.total"
        >
        </el-pagination>
      </div>
    </el-card>

    <!-- 创建/编辑用户对话框 -->
    <el-dialog
      :title="editingUser ? '编辑用户' : '创建用户'"
      v-model="dialogVisible"
      width="500px"
    >
      <el-form :model="userForm" :rules="userFormRules" ref="userFormRef" label-width="80px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="userForm.username" :disabled="editingUser"></el-input>
        </el-form-item>
        <el-form-item label="姓名" prop="full_name">
          <el-input v-model="userForm.full_name"></el-input>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="userForm.email"></el-input>
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <el-select v-model="userForm.role" style="width: 100%">
            <el-option label="管理员" value="admin"></el-option>
            <el-option label="分析师" value="analyst"></el-option>
            <el-option label="查看者" value="viewer"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item v-if="!editingUser" label="密码" prop="password">
          <el-input v-model="userForm.password" type="password" show-password></el-input>
        </el-form-item>
        <el-form-item v-if="editingUser" label="状态" prop="is_active">
          <el-switch v-model="userForm.is_active"></el-switch>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit" :loading="submitting">
            {{ editingUser ? '更新' : '创建' }}
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from 'axios'

export default {
  name: 'UserManagement',
  setup() {
    const loading = ref(false)
    const submitting = ref(false)
    const dialogVisible = ref(false)
    const editingUser = ref(null)
    const searchQuery = ref('')
    const selectedRole = ref('')
    
    const users = ref([])
    const userStats = ref({
      total_users: 0,
      active_users: 0,
      recent_logins: 0,
      admin_count: 0,
      analyst_count: 0,
      viewer_count: 0
    })
    
    const pagination = reactive({
      page: 1,
      size: 10,
      total: 0
    })
    
    const userForm = reactive({
      username: '',
      full_name: '',
      email: '',
      role: 'viewer',
      password: '',
      is_active: true
    })
    
    const userFormRules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
      ],
      full_name: [
        { required: true, message: '请输入姓名', trigger: 'blur' }
      ],
      email: [
        { required: true, message: '请输入邮箱地址', trigger: 'blur' },
        { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
      ],
      role: [
        { required: true, message: '请选择角色', trigger: 'change' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
      ]
    }
    
    const currentUser = computed(() => {
      // 这里应该从store或其他地方获取当前用户信息
      return { username: 'admin' }
    })
    
    // 获取用户列表
    const fetchUsers = async () => {
      loading.value = true
      try {
        const params = {
          page: pagination.page,
          size: pagination.size,
          search: searchQuery.value || undefined,
          role: selectedRole.value || undefined
        }
        
        const response = await axios.get('/api/users/', { params })
        users.value = response.data.users
        pagination.total = response.data.total
      } catch (error) {
        ElMessage.error('获取用户列表失败: ' + (error.response?.data?.detail || error.message))
      } finally {
        loading.value = false
      }
    }
    
    // 获取用户统计
    const fetchUserStats = async () => {
      try {
        const response = await axios.get('/api/users/stats')
        userStats.value = response.data
      } catch (error) {
        console.error('获取用户统计失败:', error)
      }
    }
    
    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return '-'
      return new Date(dateString).toLocaleString('zh-CN')
    }
    
    // 获取角色标签类型
    const getRoleTagType = (role) => {
      const types = {
        admin: 'danger',
        analyst: 'warning',
        viewer: 'info'
      }
      return types[role] || 'info'
    }
    
    // 获取角色文本
    const getRoleText = (role) => {
      const texts = {
        admin: '管理员',
        analyst: '分析师',
        viewer: '查看者'
      }
      return texts[role] || role
    }
    
    // 处理搜索
    const handleSearch = () => {
      pagination.page = 1
      fetchUsers()
    }
    
    // 处理角色过滤
    const handleRoleFilter = () => {
      pagination.page = 1
      fetchUsers()
    }
    
    // 处理排序
    const handleSortChange = ({ column, prop, order }) => {
      // 这里可以实现排序逻辑
      console.log('排序:', prop, order)
    }
    
    // 处理页面大小变化
    const handleSizeChange = (val) => {
      pagination.size = val
      pagination.page = 1
      fetchUsers()
    }
    
    // 处理当前页变化
    const handleCurrentChange = (val) => {
      pagination.page = val
      fetchUsers()
    }
    
    // 刷新用户列表
    const refreshUsers = () => {
      fetchUsers()
      fetchUserStats()
    }
    
    // 显示创建用户对话框
    const showCreateUserDialog = () => {
      editingUser.value = null
      Object.assign(userForm, {
        username: '',
        full_name: '',
        email: '',
        role: 'viewer',
        password: '',
        is_active: true
      })
      dialogVisible.value = true
    }
    
    // 处理编辑
    const handleEdit = (user) => {
      editingUser.value = user
      Object.assign(userForm, {
        username: user.username,
        full_name: user.full_name,
        email: user.email,
        role: user.role,
        is_active: user.is_active
      })
      dialogVisible.value = true
    }
    
    // 处理删除
    const handleDelete = async (user) => {
      try {
        await ElMessageBox.confirm(
          `确定要删除用户 "${user.username}" 吗？此操作不可撤销。`,
          '删除确认',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        await axios.delete(`/api/users/${user.id}`)
        ElMessage.success('用户删除成功')
        refreshUsers()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('删除用户失败: ' + (error.response?.data?.detail || error.message))
        }
      }
    }
    
    // 处理提交
    const handleSubmit = async () => {
      // 表单验证逻辑需要通过ref访问
      // 这里简化处理
      if (!userForm.username || !userForm.full_name || !userForm.email) {
        ElMessage.error('请填写完整信息')
        return
      }
      
      submitting.value = true
      try {
        if (editingUser.value) {
          // 更新用户
          await axios.put(`/api/users/${editingUser.value.id}`, {
            full_name: userForm.full_name,
            email: userForm.email,
            role: userForm.role,
            is_active: userForm.is_active
          })
          ElMessage.success('用户更新成功')
        } else {
          // 创建用户
          await axios.post('/api/users/create', userForm)
          ElMessage.success('用户创建成功')
        }
        
        dialogVisible.value = false
        refreshUsers()
      } catch (error) {
        ElMessage.error(
          (editingUser.value ? '更新' : '创建') + '用户失败: ' + 
          (error.response?.data?.detail || error.message)
        )
      } finally {
        submitting.value = false
      }
    }
    
    onMounted(() => {
      refreshUsers()
    })
    
    return {
      loading,
      submitting,
      dialogVisible,
      editingUser,
      searchQuery,
      selectedRole,
      users,
      userStats,
      pagination,
      userForm,
      userFormRules,
      currentUser,
      formatDate,
      getRoleTagType,
      getRoleText,
      handleSearch,
      handleRoleFilter,
      handleSortChange,
      handleSizeChange,
      handleCurrentChange,
      refreshUsers,
      showCreateUserDialog,
      handleEdit,
      handleDelete,
      handleSubmit
    }
  }
}
</script>

<style scoped>
.user-management {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header h1 {
  margin: 0;
  color: #303133;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.stat-card {
  border: none;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.stat-card :deep(.el-card__body) {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
}

.stat-content {
  flex: 1;
}

.stat-number {
  font-size: 24px;
  font-weight: bold;
  color: #409EFF;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 14px;
  color: #909399;
}

.stat-icon {
  font-size: 32px;
  color: #409EFF;
  opacity: 0.8;
}

.filter-card {
  margin-bottom: 20px;
}

.filter-row {
  display: flex;
  align-items: center;
}

.table-card {
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.pagination-wrapper {
  margin-top: 20px;
  text-align: right;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style> 