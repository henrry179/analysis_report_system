<template>
  <div class="settings-page">
    <div class="page-header">
      <h1>⚙️ 系统设置</h1>
      <div class="header-actions">
        <el-button @click="refreshSettings" :loading="loading">
          <el-icon><Refresh /></el-icon> 刷新
        </el-button>
        <el-button type="primary" @click="saveAllSettings" :loading="saving">
          <el-icon><Check /></el-icon> 保存全部
        </el-button>
      </div>
    </div>

    <el-tabs v-model="activeTab" class="settings-tabs">
      <!-- 基础设置 -->
      <el-tab-pane label="基础设置" name="basic">
        <el-card class="settings-card">
          <template #header>
            <div class="card-header">
              <span>系统基础配置</span>
            </div>
          </template>
          
          <el-form :model="basicSettings" label-width="120px">
            <el-form-item label="系统名称">
              <el-input v-model="basicSettings.system_name" placeholder="请输入系统名称"></el-input>
            </el-form-item>
            
            <el-form-item label="系统版本">
              <el-input v-model="basicSettings.system_version" disabled></el-input>
            </el-form-item>
            
            <el-form-item label="管理员邮箱">
              <el-input v-model="basicSettings.admin_email" placeholder="请输入管理员邮箱"></el-input>
            </el-form-item>
            
            <el-form-item label="时区设置">
              <el-select v-model="basicSettings.timezone" style="width: 100%">
                <el-option label="北京时间 (UTC+8)" value="Asia/Shanghai"></el-option>
                <el-option label="纽约时间 (UTC-5)" value="America/New_York"></el-option>
                <el-option label="伦敦时间 (UTC+0)" value="Europe/London"></el-option>
                <el-option label="东京时间 (UTC+9)" value="Asia/Tokyo"></el-option>
              </el-select>
            </el-form-item>
            
            <el-form-item label="语言设置">
              <el-select v-model="basicSettings.language" style="width: 100%">
                <el-option label="简体中文" value="zh-CN"></el-option>
                <el-option label="English" value="en-US"></el-option>
              </el-select>
            </el-form-item>
            
            <el-form-item label="调试模式">
              <el-switch v-model="basicSettings.debug_mode"></el-switch>
            </el-form-item>
          </el-form>
        </el-card>
      </el-tab-pane>

      <!-- 数据库设置 -->
      <el-tab-pane label="数据库设置" name="database">
        <el-card class="settings-card">
          <template #header>
            <div class="card-header">
              <span>数据库连接配置</span>
            </div>
          </template>
          
          <el-form :model="databaseSettings" label-width="120px">
            <el-form-item label="数据库类型">
              <el-select v-model="databaseSettings.db_type" style="width: 100%">
                <el-option label="SQLite" value="sqlite"></el-option>
                <el-option label="MySQL" value="mysql"></el-option>
                <el-option label="PostgreSQL" value="postgresql"></el-option>
              </el-select>
            </el-form-item>
            
            <el-form-item label="数据库主机" v-if="databaseSettings.db_type !== 'sqlite'">
              <el-input v-model="databaseSettings.db_host" placeholder="localhost"></el-input>
            </el-form-item>
            
            <el-form-item label="端口" v-if="databaseSettings.db_type !== 'sqlite'">
              <el-input-number v-model="databaseSettings.db_port" :min="1" :max="65535"></el-input-number>
            </el-form-item>
            
            <el-form-item label="数据库名称">
              <el-input v-model="databaseSettings.db_name" placeholder="analysis_system"></el-input>
            </el-form-item>
            
            <el-form-item label="用户名" v-if="databaseSettings.db_type !== 'sqlite'">
              <el-input v-model="databaseSettings.db_user" placeholder="请输入用户名"></el-input>
            </el-form-item>
            
            <el-form-item label="密码" v-if="databaseSettings.db_type !== 'sqlite'">
              <el-input v-model="databaseSettings.db_password" type="password" show-password placeholder="请输入密码"></el-input>
            </el-form-item>
            
            <el-form-item>
              <el-button @click="testDatabaseConnection" :loading="testingDb">
                测试连接
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-tab-pane>

      <!-- 性能设置 -->
      <el-tab-pane label="性能设置" name="performance">
        <el-card class="settings-card">
          <template #header>
            <div class="card-header">
              <span>系统性能配置</span>
            </div>
          </template>
          
          <el-form :model="performanceSettings" label-width="150px">
            <el-form-item label="最大并发处理数">
              <el-input-number v-model="performanceSettings.max_workers" :min="1" :max="20"></el-input-number>
              <div class="form-tip">建议设置为CPU核心数的2倍</div>
            </el-form-item>
            
            <el-form-item label="内存使用限制(MB)">
              <el-input-number v-model="performanceSettings.memory_limit" :min="512" :max="8192"></el-input-number>
            </el-form-item>
            
            <el-form-item label="文件上传大小限制(MB)">
              <el-input-number v-model="performanceSettings.upload_limit" :min="1" :max="500"></el-input-number>
            </el-form-item>
            
            <el-form-item label="缓存过期时间(小时)">
              <el-input-number v-model="performanceSettings.cache_ttl" :min="1" :max="168"></el-input-number>
            </el-form-item>
            
            <el-form-item label="启用数据压缩">
              <el-switch v-model="performanceSettings.enable_compression"></el-switch>
            </el-form-item>
            
            <el-form-item label="启用请求日志">
              <el-switch v-model="performanceSettings.enable_request_log"></el-switch>
            </el-form-item>
          </el-form>
        </el-card>
      </el-tab-pane>

      <!-- 安全设置 -->
      <el-tab-pane label="安全设置" name="security">
        <el-card class="settings-card">
          <template #header>
            <div class="card-header">
              <span>系统安全配置</span>
            </div>
          </template>
          
          <el-form :model="securitySettings" label-width="150px">
            <el-form-item label="JWT密钥">
              <el-input v-model="securitySettings.jwt_secret" type="password" show-password readonly>
                <template #append>
                  <el-button @click="regenerateJwtSecret">重新生成</el-button>
                </template>
              </el-input>
            </el-form-item>
            
            <el-form-item label="Token过期时间(小时)">
              <el-input-number v-model="securitySettings.token_expire_hours" :min="1" :max="168"></el-input-number>
            </el-form-item>
            
            <el-form-item label="密码最小长度">
              <el-input-number v-model="securitySettings.password_min_length" :min="6" :max="20"></el-input-number>
            </el-form-item>
            
            <el-form-item label="最大登录尝试次数">
              <el-input-number v-model="securitySettings.max_login_attempts" :min="3" :max="10"></el-input-number>
            </el-form-item>
            
            <el-form-item label="账户锁定时间(分钟)">
              <el-input-number v-model="securitySettings.lockout_duration" :min="5" :max="60"></el-input-number>
            </el-form-item>
            
            <el-form-item label="启用两步验证">
              <el-switch v-model="securitySettings.enable_2fa"></el-switch>
            </el-form-item>
            
            <el-form-item label="允许的IP地址">
              <el-input v-model="securitySettings.allowed_ips" type="textarea" :rows="3" placeholder="留空表示允许所有IP，多个IP用逗号分隔"></el-input>
            </el-form-item>
          </el-form>
        </el-card>
      </el-tab-pane>

      <!-- 备份设置 -->
      <el-tab-pane label="备份与恢复" name="backup">
        <el-card class="settings-card">
          <template #header>
            <div class="card-header">
              <span>数据备份与恢复</span>
            </div>
          </template>
          
          <el-form :model="backupSettings" label-width="150px">
            <el-form-item label="自动备份">
              <el-switch v-model="backupSettings.auto_backup"></el-switch>
            </el-form-item>
            
            <el-form-item label="备份频率" v-if="backupSettings.auto_backup">
              <el-select v-model="backupSettings.backup_frequency" style="width: 100%">
                <el-option label="每天" value="daily"></el-option>
                <el-option label="每周" value="weekly"></el-option>
                <el-option label="每月" value="monthly"></el-option>
              </el-select>
            </el-form-item>
            
            <el-form-item label="备份时间" v-if="backupSettings.auto_backup">
              <el-time-picker v-model="backupSettings.backup_time" format="HH:mm"></el-time-picker>
            </el-form-item>
            
            <el-form-item label="保留备份数量">
              <el-input-number v-model="backupSettings.backup_retention" :min="1" :max="30"></el-input-number>
            </el-form-item>
            
            <el-form-item label="备份路径">
              <el-input v-model="backupSettings.backup_path" placeholder="./backups"></el-input>
            </el-form-item>
            
            <el-form-item>
              <el-button @click="createBackup" :loading="creatingBackup">
                立即创建备份
              </el-button>
              <el-button @click="showRestoreDialog">
                恢复备份
              </el-button>
            </el-form-item>
          </el-form>
          
          <!-- 备份列表 -->
          <el-divider content-position="left">备份历史</el-divider>
          <el-table :data="backupHistory" style="width: 100%">
            <el-table-column prop="filename" label="文件名"></el-table-column>
            <el-table-column prop="size" label="大小">
              <template #default="scope">
                {{ formatFileSize(scope.row.size) }}
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="创建时间">
              <template #default="scope">
                {{ formatDate(scope.row.created_at) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="200">
              <template #default="scope">
                <el-button size="small" @click="downloadBackup(scope.row)">下载</el-button>
                <el-button size="small" type="warning" @click="restoreBackup(scope.row)">恢复</el-button>
                <el-button size="small" type="danger" @click="deleteBackup(scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-tab-pane>
    </el-tabs>

    <!-- 恢复备份对话框 -->
    <el-dialog
      title="恢复备份"
      v-model="restoreDialogVisible"
      width="500px"
    >
      <el-alert
        title="警告"
        type="warning"
        description="恢复备份将覆盖当前所有数据，此操作不可撤销！"
        show-icon
        :closable="false"
      />
      
      <el-upload
        ref="uploadRef"
        :auto-upload="false"
        :on-change="handleBackupFile"
        :accept="'.sql,.zip'"
        drag
        :limit="1"
        style="margin-top: 20px;"
      >
        <el-icon class="el-icon--upload"><Upload /></el-icon>
        <div class="el-upload__text">
          将备份文件拖到此处，或<em>点击上传</em>
        </div>
        <div class="el-upload__tip">
          支持 .sql 和 .zip 格式的备份文件
        </div>
      </el-upload>
      
      <template #footer>
        <el-button @click="restoreDialogVisible = false">取消</el-button>
        <el-button type="danger" @click="confirmRestore" :loading="restoring">
          确认恢复
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Refresh,
  Check,
  Upload
} from '@element-plus/icons-vue'
import axios from 'axios'

export default {
  name: 'Settings',
  components: {
    Refresh,
    Check,
    Upload
  },
  setup() {
    const loading = ref(false)
    const saving = ref(false)
    const testingDb = ref(false)
    const creatingBackup = ref(false)
    const restoring = ref(false)
    const restoreDialogVisible = ref(false)
    const activeTab = ref('basic')
    
    const basicSettings = reactive({
      system_name: '业务分析报告系统',
      system_version: 'v4.0 Optimized',
      admin_email: 'admin@example.com',
      timezone: 'Asia/Shanghai',
      language: 'zh-CN',
      debug_mode: false
    })
    
    const databaseSettings = reactive({
      db_type: 'sqlite',
      db_host: 'localhost',
      db_port: 3306,
      db_name: 'analysis_system',
      db_user: '',
      db_password: ''
    })
    
    const performanceSettings = reactive({
      max_workers: 4,
      memory_limit: 2048,
      upload_limit: 100,
      cache_ttl: 24,
      enable_compression: true,
      enable_request_log: true
    })
    
    const securitySettings = reactive({
      jwt_secret: '****************************',
      token_expire_hours: 24,
      password_min_length: 8,
      max_login_attempts: 5,
      lockout_duration: 15,
      enable_2fa: false,
      allowed_ips: ''
    })
    
    const backupSettings = reactive({
      auto_backup: true,
      backup_frequency: 'daily',
      backup_time: new Date(),
      backup_retention: 7,
      backup_path: './backups'
    })
    
    const backupHistory = ref([])
    const backupFile = ref(null)
    
    // 加载设置
    const loadSettings = async () => {
      loading.value = true
      try {
        const response = await axios.get('/api/settings/')
        Object.assign(basicSettings, response.data.basic || {})
        Object.assign(databaseSettings, response.data.database || {})
        Object.assign(performanceSettings, response.data.performance || {})
        Object.assign(securitySettings, response.data.security || {})
        Object.assign(backupSettings, response.data.backup || {})
      } catch (error) {
        ElMessage.error('加载设置失败')
      } finally {
        loading.value = false
      }
    }
    
    // 保存所有设置
    const saveAllSettings = async () => {
      saving.value = true
      try {
        await axios.put('/api/settings/', {
          basic: basicSettings,
          database: databaseSettings,
          performance: performanceSettings,
          security: securitySettings,
          backup: backupSettings
        })
        ElMessage.success('设置保存成功')
      } catch (error) {
        ElMessage.error('保存设置失败')
      } finally {
        saving.value = false
      }
    }
    
    // 测试数据库连接
    const testDatabaseConnection = async () => {
      testingDb.value = true
      try {
        await axios.post('/api/settings/test-db', databaseSettings)
        ElMessage.success('数据库连接测试成功')
      } catch (error) {
        ElMessage.error('数据库连接测试失败')
      } finally {
        testingDb.value = false
      }
    }
    
    // 重新生成JWT密钥
    const regenerateJwtSecret = async () => {
      try {
        await ElMessageBox.confirm(
          '重新生成JWT密钥将使所有现有token失效，用户需要重新登录。确定继续？',
          '确认操作',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        const response = await axios.post('/api/settings/regenerate-jwt')
        securitySettings.jwt_secret = response.data.secret
        ElMessage.success('JWT密钥重新生成成功')
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('重新生成JWT密钥失败')
        }
      }
    }
    
    // 创建备份
    const createBackup = async () => {
      creatingBackup.value = true
      try {
        await axios.post('/api/settings/create-backup')
        ElMessage.success('备份创建成功')
        loadBackupHistory()
      } catch (error) {
        ElMessage.error('创建备份失败')
      } finally {
        creatingBackup.value = false
      }
    }
    
    // 加载备份历史
    const loadBackupHistory = async () => {
      try {
        const response = await axios.get('/api/settings/backup-history')
        backupHistory.value = response.data
      } catch (error) {
        console.error('加载备份历史失败:', error)
      }
    }
    
    // 下载备份
    const downloadBackup = (backup) => {
      const link = document.createElement('a')
      link.href = `/api/settings/download-backup/${backup.id}`
      link.download = backup.filename
      link.click()
    }
    
    // 恢复备份
    const restoreBackup = async (backup) => {
      try {
        await ElMessageBox.confirm(
          `确定要恢复备份"${backup.filename}"吗？此操作将覆盖当前所有数据且不可撤销！`,
          '恢复确认',
          {
            confirmButtonText: '确定恢复',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        await axios.post(`/api/settings/restore-backup/${backup.id}`)
        ElMessage.success('备份恢复成功，系统将在3秒后刷新')
        setTimeout(() => window.location.reload(), 3000)
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('备份恢复失败')
        }
      }
    }
    
    // 删除备份
    const deleteBackup = async (backup) => {
      try {
        await ElMessageBox.confirm(
          `确定要删除备份"${backup.filename}"吗？`,
          '删除确认',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        await axios.delete(`/api/settings/backup/${backup.id}`)
        ElMessage.success('备份删除成功')
        loadBackupHistory()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('删除备份失败')
        }
      }
    }
    
    // 显示恢复对话框
    const showRestoreDialog = () => {
      backupFile.value = null
      restoreDialogVisible.value = true
    }
    
    // 处理备份文件
    const handleBackupFile = (file) => {
      backupFile.value = file.raw
    }
    
    // 确认恢复
    const confirmRestore = async () => {
      if (!backupFile.value) {
        ElMessage.error('请选择备份文件')
        return
      }
      
      restoring.value = true
      try {
        const formData = new FormData()
        formData.append('file', backupFile.value)
        
        await axios.post('/api/settings/restore-backup', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })
        
        ElMessage.success('备份恢复成功，系统将在3秒后刷新')
        restoreDialogVisible.value = false
        setTimeout(() => window.location.reload(), 3000)
      } catch (error) {
        ElMessage.error('备份恢复失败')
      } finally {
        restoring.value = false
      }
    }
    
    // 刷新设置
    const refreshSettings = () => {
      loadSettings()
      loadBackupHistory()
    }
    
    // 格式化文件大小
    const formatFileSize = (bytes) => {
      if (!bytes) return '0 B'
      const k = 1024
      const sizes = ['B', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    }
    
    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return '-'
      return new Date(dateString).toLocaleString('zh-CN')
    }
    
    onMounted(() => {
      loadSettings()
      loadBackupHistory()
    })
    
    return {
      loading,
      saving,
      testingDb,
      creatingBackup,
      restoring,
      restoreDialogVisible,
      activeTab,
      basicSettings,
      databaseSettings,
      performanceSettings,
      securitySettings,
      backupSettings,
      backupHistory,
      saveAllSettings,
      testDatabaseConnection,
      regenerateJwtSecret,
      createBackup,
      downloadBackup,
      restoreBackup,
      deleteBackup,
      showRestoreDialog,
      handleBackupFile,
      confirmRestore,
      refreshSettings,
      formatFileSize,
      formatDate
    }
  }
}
</script>

<style scoped>
.settings-page {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h1 {
  margin: 0;
  color: #303133;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.settings-tabs {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.settings-card {
  margin-bottom: 20px;
  border: none;
  box-shadow: none;
}

.card-header {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.form-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}

.el-divider {
  margin: 30px 0 20px 0;
}
</style> 