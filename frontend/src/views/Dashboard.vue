<template>
  <div class="dashboard-container">
    <el-container>
      <el-aside width="200px">
        <el-menu
          :default-active="activeMenu"
          class="el-menu-vertical"
          @select="handleSelect"
        >
          <el-menu-item index="data">
            <el-icon><Document /></el-icon>
            <span>数据管理</span>
          </el-menu-item>
          <el-menu-item index="analysis">
            <el-icon><DataAnalysis /></el-icon>
            <span>数据分析</span>
          </el-menu-item>
          <el-menu-item index="reports">
            <el-icon><Files /></el-icon>
            <span>报告管理</span>
          </el-menu-item>
          <el-menu-item index="system">
            <el-icon><Setting /></el-icon>
            <span>系统管理</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      
      <el-container>
        <el-header>
          <div class="header-content">
            <h2>数据分析报告系统</h2>
            <el-dropdown @command="handleCommand">
              <span class="user-info">
                {{ username }}
                <el-icon><ArrowDown /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="logout">退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </el-header>
        
        <el-main>
          <!-- 数据管理 -->
          <div v-if="activeMenu === 'data'" class="section">
            <h3>数据管理</h3>
            <el-upload
              class="upload-demo"
              drag
              action="http://localhost:8000/api/data/import"
              :headers="uploadHeaders"
              :on-success="handleUploadSuccess"
              :on-error="handleUploadError"
            >
              <el-icon class="el-icon--upload"><Upload /></el-icon>
              <div class="el-upload__text">
                将文件拖到此处，或<em>点击上传</em>
              </div>
              <template #tip>
                <div class="el-upload__tip">
                  支持 CSV、Excel、JSON 格式文件
                </div>
              </template>
            </el-upload>
            
            <el-table
              v-if="dataList.length"
              :data="dataList"
              style="width: 100%; margin-top: 20px"
            >
              <el-table-column prop="filename" label="文件名" />
              <el-table-column prop="size" label="大小" />
              <el-table-column prop="upload_time" label="上传时间" />
              <el-table-column label="操作">
                <template #default="scope">
                  <el-button
                    size="small"
                    @click="handlePreview(scope.row)"
                  >
                    预览
                  </el-button>
                  <el-button
                    size="small"
                    type="danger"
                    @click="handleDelete(scope.row)"
                  >
                    删除
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
          
          <!-- 数据分析 -->
          <div v-if="activeMenu === 'analysis'" class="section">
            <h3>数据分析</h3>
            <el-form :model="analysisForm" label-width="120px">
              <el-form-item label="分析类型">
                <el-select v-model="analysisForm.type">
                  <el-option label="描述性分析" value="descriptive" />
                  <el-option label="相关性分析" value="correlation" />
                  <el-option label="趋势分析" value="trend" />
                  <el-option label="预测分析" value="forecast" />
                </el-select>
              </el-form-item>
              
              <el-form-item label="数据文件">
                <el-select v-model="analysisForm.file">
                  <el-option
                    v-for="file in dataList"
                    :key="file.id"
                    :label="file.filename"
                    :value="file.id"
                  />
                </el-select>
              </el-form-item>
              
              <el-form-item>
                <el-button
                  type="primary"
                  @click="handleAnalysis"
                  :loading="analysisLoading"
                >
                  开始分析
                </el-button>
              </el-form-item>
            </el-form>
            
            <div v-if="analysisResults" class="analysis-results">
              <h4>分析结果</h4>
              <pre>{{ JSON.stringify(analysisResults, null, 2) }}</pre>
            </div>
          </div>
          
          <!-- 报告管理 -->
          <div v-if="activeMenu === 'reports'" class="section">
            <h3>报告管理</h3>
            <el-form :model="reportForm" label-width="120px">
              <el-form-item label="报告类型">
                <el-select v-model="reportForm.type">
                  <el-option label="可视化报告" value="visualization" />
                  <el-option label="分析报告" value="analysis" />
                </el-select>
              </el-form-item>
              
              <el-form-item label="数据文件">
                <el-select v-model="reportForm.file">
                  <el-option
                    v-for="file in dataList"
                    :key="file.id"
                    :label="file.filename"
                    :value="file.id"
                  />
                </el-select>
              </el-form-item>
              
              <el-form-item label="输出格式">
                <el-select v-model="reportForm.format">
                  <el-option label="HTML" value="html" />
                  <el-option label="PDF" value="pdf" />
                  <el-option label="Markdown" value="markdown" />
                  <el-option label="JSON" value="json" />
                </el-select>
              </el-form-item>
              
              <el-form-item>
                <el-button
                  type="primary"
                  @click="handleGenerateReport"
                  :loading="reportLoading"
                >
                  生成报告
                </el-button>
              </el-form-item>
            </el-form>
            
            <el-table
              v-if="reportList.length"
              :data="reportList"
              style="width: 100%; margin-top: 20px"
            >
              <el-table-column prop="name" label="报告名称" />
              <el-table-column prop="type" label="类型" />
              <el-table-column prop="format" label="格式" />
              <el-table-column prop="create_time" label="创建时间" />
              <el-table-column label="操作">
                <template #default="scope">
                  <el-button
                    size="small"
                    @click="handleDownload(scope.row)"
                  >
                    下载
                  </el-button>
                  <el-button
                    size="small"
                    type="danger"
                    @click="handleDeleteReport(scope.row)"
                  >
                    删除
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
          
          <!-- 系统管理 -->
          <div v-if="activeMenu === 'system'" class="section">
            <h3>系统管理</h3>
            <el-tabs>
              <el-tab-pane label="用户管理">
                <el-button
                  type="primary"
                  @click="showCreateUserDialog = true"
                >
                  创建用户
                </el-button>
                
                <el-table
                  :data="userList"
                  style="width: 100%; margin-top: 20px"
                >
                  <el-table-column prop="username" label="用户名" />
                  <el-table-column prop="role" label="角色" />
                  <el-table-column prop="create_time" label="创建时间" />
                  <el-table-column label="操作">
                    <template #default="scope">
                      <el-button
                        size="small"
                        type="danger"
                        @click="handleDeleteUser(scope.row)"
                      >
                        删除
                      </el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </el-tab-pane>
              
              <el-tab-pane label="系统日志">
                <el-table
                  :data="logList"
                  style="width: 100%"
                >
                  <el-table-column prop="timestamp" label="时间" />
                  <el-table-column prop="level" label="级别" />
                  <el-table-column prop="message" label="消息" />
                </el-table>
              </el-tab-pane>
              
              <el-tab-pane label="备份管理">
                <el-button
                  type="primary"
                  @click="handleBackup"
                >
                  创建备份
                </el-button>
                
                <el-button
                  type="warning"
                  @click="showRestoreDialog = true"
                >
                  恢复备份
                </el-button>
                
                <el-table
                  :data="backupList"
                  style="width: 100%; margin-top: 20px"
                >
                  <el-table-column prop="filename" label="文件名" />
                  <el-table-column prop="size" label="大小" />
                  <el-table-column prop="create_time" label="创建时间" />
                  <el-table-column label="操作">
                    <template #default="scope">
                      <el-button
                        size="small"
                        @click="handleDownloadBackup(scope.row)"
                      >
                        下载
                      </el-button>
                      <el-button
                        size="small"
                        type="danger"
                        @click="handleDeleteBackup(scope.row)"
                      >
                        删除
                      </el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </el-tab-pane>
            </el-tabs>
          </div>
        </el-main>
      </el-container>
    </el-container>
    
    <!-- 创建用户对话框 -->
    <el-dialog
      v-model="showCreateUserDialog"
      title="创建用户"
      width="500px"
    >
      <el-form
        :model="createUserForm"
        :rules="createUserRules"
        label-width="100px"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="createUserForm.username" />
        </el-form-item>
        
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="createUserForm.password"
            type="password"
            show-password
          />
        </el-form-item>
        
        <el-form-item label="角色" prop="role">
          <el-select v-model="createUserForm.role">
            <el-option label="管理员" value="admin" />
            <el-option label="普通用户" value="user" />
          </el-select>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="showCreateUserDialog = false">取消</el-button>
        <el-button
          type="primary"
          @click="handleCreateUser"
          :loading="createUserLoading"
        >
          创建
        </el-button>
      </template>
    </el-dialog>
    
    <!-- 恢复备份对话框 -->
    <el-dialog
      v-model="showRestoreDialog"
      title="恢复备份"
      width="500px"
    >
      <el-upload
        class="upload-demo"
        drag
        action="http://localhost:8000/api/system/restore"
        :headers="uploadHeaders"
        :on-success="handleRestoreSuccess"
        :on-error="handleRestoreError"
      >
        <el-icon class="el-icon--upload"><Upload /></el-icon>
        <div class="el-upload__text">
          将备份文件拖到此处，或<em>点击上传</em>
        </div>
      </el-upload>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Document,
  DataAnalysis,
  Files,
  Setting,
  ArrowDown,
  Upload
} from '@element-plus/icons-vue'
import axios from 'axios'

export default {
  name: 'Dashboard',
  components: {
    Document,
    DataAnalysis,
    Files,
    Setting,
    ArrowDown,
    Upload
  },
  setup() {
    const router = useRouter()
    const activeMenu = ref('data')
    const username = ref('')
    
    // 数据管理
    const dataList = ref([])
    const uploadHeaders = {
      Authorization: `Bearer ${localStorage.getItem('token')}`
    }
    
    // 数据分析
    const analysisForm = reactive({
      type: 'descriptive',
      file: ''
    })
    const analysisLoading = ref(false)
    const analysisResults = ref(null)
    
    // 报告管理
    const reportForm = reactive({
      type: 'visualization',
      file: '',
      format: 'html'
    })
    const reportLoading = ref(false)
    const reportList = ref([])
    
    // 系统管理
    const showCreateUserDialog = ref(false)
    const createUserForm = reactive({
      username: '',
      password: '',
      role: 'user'
    })
    const createUserLoading = ref(false)
    const createUserRules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' }
      ],
      role: [
        { required: true, message: '请选择角色', trigger: 'change' }
      ]
    }
    const userList = ref([])
    const logList = ref([])
    const showRestoreDialog = ref(false)
    const backupList = ref([])
    
    // 获取用户信息
    const getUserInfo = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/users/me')
        username.value = response.data.username
      } catch (error) {
        ElMessage.error('获取用户信息失败')
        router.push('/login')
      }
    }
    
    // 获取数据列表
    const getDataList = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/data')
        dataList.value = response.data
      } catch (error) {
        ElMessage.error('获取数据列表失败')
      }
    }
    
    // 获取报告列表
    const getReportList = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/reports')
        reportList.value = response.data
      } catch (error) {
        ElMessage.error('获取报告列表失败')
      }
    }
    
    // 获取用户列表
    const getUserList = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/users')
        userList.value = response.data
      } catch (error) {
        ElMessage.error('获取用户列表失败')
      }
    }
    
    // 获取日志列表
    const getLogList = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/system/logs')
        logList.value = response.data
      } catch (error) {
        ElMessage.error('获取日志列表失败')
      }
    }
    
    // 获取备份列表
    const getBackupList = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/system/backups')
        backupList.value = response.data
      } catch (error) {
        ElMessage.error('获取备份列表失败')
      }
    }
    
    // 处理菜单选择
    const handleSelect = (key) => {
      activeMenu.value = key
      if (key === 'data') {
        getDataList()
      } else if (key === 'reports') {
        getReportList()
      } else if (key === 'system') {
        getUserList()
        getLogList()
        getBackupList()
      }
    }
    
    // 处理退出登录
    const handleCommand = (command) => {
      if (command === 'logout') {
        localStorage.removeItem('token')
        router.push('/login')
      }
    }
    
    // 处理文件上传
    const handleUploadSuccess = (response) => {
      ElMessage.success('上传成功')
      getDataList()
    }
    
    const handleUploadError = () => {
      ElMessage.error('上传失败')
    }
    
    // 处理数据分析
    const handleAnalysis = async () => {
      if (!analysisForm.file) {
        ElMessage.warning('请选择数据文件')
        return
      }
      
      analysisLoading.value = true
      try {
        const response = await axios.post('http://localhost:8000/api/analysis', {
          type: analysisForm.type,
          file_id: analysisForm.file
        })
        analysisResults.value = response.data
        ElMessage.success('分析完成')
      } catch (error) {
        ElMessage.error('分析失败')
      } finally {
        analysisLoading.value = false
      }
    }
    
    // 处理报告生成
    const handleGenerateReport = async () => {
      if (!reportForm.file) {
        ElMessage.warning('请选择数据文件')
        return
      }
      
      reportLoading.value = true
      try {
        const response = await axios.post('http://localhost:8000/api/reports/generate', {
          type: reportForm.type,
          file_id: reportForm.file,
          format: reportForm.format
        })
        ElMessage.success('报告生成成功')
        getReportList()
      } catch (error) {
        ElMessage.error('报告生成失败')
      } finally {
        reportLoading.value = false
      }
    }
    
    // 处理创建用户
    const handleCreateUser = async () => {
      createUserLoading.value = true
      try {
        await axios.post('http://localhost:8000/api/users', createUserForm)
        ElMessage.success('创建用户成功')
        showCreateUserDialog.value = false
        getUserList()
      } catch (error) {
        ElMessage.error('创建用户失败')
      } finally {
        createUserLoading.value = false
      }
    }
    
    // 处理删除用户
    const handleDeleteUser = async (user) => {
      try {
        await ElMessageBox.confirm('确定要删除该用户吗？', '提示', {
          type: 'warning'
        })
        await axios.delete(`http://localhost:8000/api/users/${user.id}`)
        ElMessage.success('删除用户成功')
        getUserList()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('删除用户失败')
        }
      }
    }
    
    // 处理系统备份
    const handleBackup = async () => {
      try {
        await axios.post('http://localhost:8000/api/system/backup')
        ElMessage.success('创建备份成功')
        getBackupList()
      } catch (error) {
        ElMessage.error('创建备份失败')
      }
    }
    
    // 处理恢复备份
    const handleRestoreSuccess = () => {
      ElMessage.success('恢复备份成功')
      showRestoreDialog.value = false
      getBackupList()
    }
    
    const handleRestoreError = () => {
      ElMessage.error('恢复备份失败')
    }
    
    onMounted(() => {
      getUserInfo()
      getDataList()
    })
    
    return {
      activeMenu,
      username,
      dataList,
      uploadHeaders,
      analysisForm,
      analysisLoading,
      analysisResults,
      reportForm,
      reportLoading,
      reportList,
      showCreateUserDialog,
      createUserForm,
      createUserLoading,
      createUserRules,
      userList,
      logList,
      showRestoreDialog,
      backupList,
      handleSelect,
      handleCommand,
      handleUploadSuccess,
      handleUploadError,
      handleAnalysis,
      handleGenerateReport,
      handleCreateUser,
      handleDeleteUser,
      handleBackup,
      handleRestoreSuccess,
      handleRestoreError
    }
  }
}
</script>

<style scoped>
.dashboard-container {
  height: 100vh;
}

.el-header {
  background-color: #fff;
  border-bottom: 1px solid #dcdfe6;
  padding: 0 20px;
}

.header-content {
  height: 60px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.el-aside {
  background-color: #304156;
}

.el-menu {
  border-right: none;
}

.section {
  padding: 20px;
}

.analysis-results {
  margin-top: 20px;
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.analysis-results pre {
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style> 