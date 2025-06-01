<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <h2>数据分析报告系统</h2>
      </template>
      
      <el-form
        ref="loginFormRef"
        :model="formModel"
        :rules="rules"
        label-width="80px"
        @submit.prevent="handleLogin"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="formModel.username"
            placeholder="请输入用户名"
          />
        </el-form-item>
        
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="formModel.password"
            type="password"
            placeholder="请输入密码"
            show-password
          />
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            native-type="submit"
            :loading="loading"
            class="login-button"
          >
            登录
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import axios from 'axios'

export default {
  name: 'Login',
  setup() {
    const router = useRouter()
    const loginFormRef = ref(null)
    const formModel = ref({
      username: '',
      password: ''
    })
    const loading = ref(false)
    
    const rules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' }
      ]
    }
    
    const handleLogin = () => {
      loginFormRef.value.validate(async (valid) => {
        if (!valid) return
        loading.value = true
        try {
          const response = await axios.post('http://localhost:8000/api/auth/token', {
            username: formModel.value.username,
            password: formModel.value.password
          })
          const { access_token } = response.data
          localStorage.setItem('token', access_token)
          axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
          ElMessage.success('登录成功')
          router.push('/dashboard')
        } catch (error) {
          ElMessage.error(error.response?.data?.detail || '登录失败')
        } finally {
          loading.value = false
        }
      })
    }
    
    return {
      loginFormRef,
      formModel,
      loading,
      rules,
      handleLogin
    }
  }
}
</script>

<style scoped>
.login-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f5f7fa;
}

.login-card {
  width: 400px;
}

.login-card :deep(.el-card__header) {
  text-align: center;
}

.login-button {
  width: 100%;
}
</style> 