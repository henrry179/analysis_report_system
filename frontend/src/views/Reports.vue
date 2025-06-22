<template>
  <div class="reports-page">
    <div class="page-header">
      <h1>📊 报告管理</h1>
      <div class="header-actions">
        <el-button @click="refreshReports" :loading="loading">
          <el-icon><Refresh /></el-icon> 刷新
        </el-button>
        <el-button type="primary" @click="showCreateReportDialog">
          <el-icon><Plus /></el-icon> 生成新报告
        </el-button>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-section">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-number">{{ reportStats.total_reports }}</div>
              <div class="stat-label">总报告数</div>
            </div>
            <el-icon class="stat-icon"><Document /></el-icon>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-number">{{ reportStats.today_reports }}</div>
              <div class="stat-label">今日生成</div>
            </div>
            <el-icon class="stat-icon"><Calendar /></el-icon>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-number">{{ reportStats.processing_reports }}</div>
              <div class="stat-label">处理中</div>
            </div>
            <el-icon class="stat-icon"><Loading /></el-icon>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-content">
              <div class="stat-number">{{ formatFileSize(reportStats.total_size) }}</div>
              <div class="stat-label">总大小</div>
            </div>
            <el-icon class="stat-icon"><Folder /></el-icon>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 过滤器 -->
    <el-card class="filter-card">
      <el-row :gutter="20">
        <el-col :span="8">
          <el-input
            v-model="searchQuery"
            placeholder="搜索报告名称"
            @input="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </el-col>
        <el-col :span="4">
          <el-select v-model="filterType" placeholder="报告类型" @change="handleFilter">
            <el-option label="全部类型" value=""></el-option>
            <el-option label="零售分析" value="retail"></el-option>
            <el-option label="金融分析" value="financial"></el-option>
            <el-option label="跨行业分析" value="cross_industry"></el-option>
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-select v-model="filterStatus" placeholder="状态" @change="handleFilter">
            <el-option label="全部状态" value=""></el-option>
            <el-option label="已完成" value="completed"></el-option>
            <el-option label="处理中" value="processing"></el-option>
            <el-option label="失败" value="failed"></el-option>
          </el-select>
        </el-col>
        <el-col :span="8">
          <el-date-picker
            v-model="dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            @change="handleFilter"
          />
        </el-col>
      </el-row>
    </el-card>

    <!-- 报告列表 -->
    <el-card class="reports-table">
      <el-table
        :data="reports"
        v-loading="loading"
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="name" label="报告名称" min-width="200">
          <template #default="scope">
            <div class="report-name">
              <el-icon><Document /></el-icon>
              <span>{{ scope.row.name }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="type" label="类型" width="120">
          <template #default="scope">
            <el-tag :type="getTypeColor(scope.row.type)">
              {{ getTypeText(scope.row.type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getStatusColor(scope.row.status)">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="format" label="格式" width="80"></el-table-column>
        <el-table-column prop="size" label="大小" width="100">
          <template #default="scope">
            {{ formatFileSize(scope.row.size) }}
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="160">
          <template #default="scope">
            {{ formatDate(scope.row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column prop="duration" label="耗时" width="100"></el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <el-button
              size="small"
              @click="viewReport(scope.row)"
              :disabled="scope.row.status !== 'completed'"
            >
              预览
            </el-button>
            <el-button
              size="small"
              type="primary"
              @click="downloadReport(scope.row)"
              :disabled="scope.row.status !== 'completed'"
            >
              下载
            </el-button>
            <el-button
              size="small"
              type="danger"
              @click="deleteReport(scope.row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-wrapper">
        <el-pagination
          @current-change="handlePageChange"
          :current-page="pagination.page"
          :page-size="pagination.size"
          layout="total, prev, pager, next"
          :total="pagination.total"
        />
      </div>
    </el-card>

    <!-- 创建报告对话框 -->
    <el-dialog
      title="生成新报告"
      v-model="createDialogVisible"
      width="600px"
    >
      <el-form :model="reportForm" label-width="100px">
        <el-form-item label="报告类型">
          <el-select v-model="reportForm.industries" multiple placeholder="选择行业类型">
            <el-option label="零售分析" value="retail"></el-option>
            <el-option label="金融交易" value="financial"></el-option>
            <el-option label="社区团购" value="community"></el-option>
            <el-option label="智能体" value="ai_agent"></el-option>
            <el-option label="跨行业分析" value="cross_industry"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="报告名称">
          <el-input v-model="reportForm.name" placeholder="请输入报告名称"></el-input>
        </el-form-item>
        <el-form-item label="描述">
          <el-input
            v-model="reportForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入报告描述"
          ></el-input>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="createDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="generateReport" :loading="generating">
          生成报告
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Document,
  Calendar,
  Loading,
  Folder,
  Search,
  Refresh,
  Plus
} from '@element-plus/icons-vue'
import axios from 'axios'

export default {
  name: 'Reports',
  components: {
    Document,
    Calendar,
    Loading,
    Folder,
    Search,
    Refresh,
    Plus
  },
  setup() {
    const loading = ref(false)
    const generating = ref(false)
    const createDialogVisible = ref(false)
    
    const searchQuery = ref('')
    const filterType = ref('')
    const filterStatus = ref('')
    const dateRange = ref([])
    
    const reports = ref([])
    const reportStats = ref({
      total_reports: 0,
      today_reports: 0,
      processing_reports: 0,
      total_size: 0
    })
    
    const pagination = reactive({
      page: 1,
      size: 10,
      total: 0
    })
    
    const reportForm = reactive({
      industries: [],
      name: '',
      description: ''
    })
    
    // 获取报告列表
    const fetchReports = async () => {
      loading.value = true
      try {
        const response = await axios.get('/api/reports/')
        reports.value = response.data.reports || []
        pagination.total = response.data.total || 0
      } catch (error) {
        ElMessage.error('获取报告列表失败')
      } finally {
        loading.value = false
      }
    }
    
    // 获取报告统计
    const fetchReportStats = async () => {
      try {
        const response = await axios.get('/api/reports/stats')
        reportStats.value = response.data
      } catch (error) {
        console.error('获取报告统计失败:', error)
      }
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
    
    // 获取类型颜色
    const getTypeColor = (type) => {
      const colors = {
        retail: 'primary',
        financial: 'success',
        community: 'warning',
        ai_agent: 'info',
        cross_industry: 'danger'
      }
      return colors[type] || 'info'
    }
    
    // 获取类型文本
    const getTypeText = (type) => {
      const texts = {
        retail: '零售分析',
        financial: '金融交易',
        community: '社区团购',
        ai_agent: '智能体',
        cross_industry: '跨行业'
      }
      return texts[type] || type
    }
    
    // 获取状态颜色
    const getStatusColor = (status) => {
      const colors = {
        completed: 'success',
        processing: 'warning',
        failed: 'danger'
      }
      return colors[status] || 'info'
    }
    
    // 获取状态文本
    const getStatusText = (status) => {
      const texts = {
        completed: '已完成',
        processing: '处理中',
        failed: '失败'
      }
      return texts[status] || status
    }
    
    // 处理搜索
    const handleSearch = () => {
      // 实现搜索逻辑
      fetchReports()
    }
    
    // 处理过滤
    const handleFilter = () => {
      // 实现过滤逻辑
      fetchReports()
    }
    
    // 处理分页
    const handlePageChange = (page) => {
      pagination.page = page
      fetchReports()
    }
    
    // 刷新报告列表
    const refreshReports = () => {
      fetchReports()
      fetchReportStats()
    }
    
    // 显示创建报告对话框
    const showCreateReportDialog = () => {
      reportForm.industries = []
      reportForm.name = ''
      reportForm.description = ''
      createDialogVisible.value = true
    }
    
    // 生成报告
    const generateReport = async () => {
      if (!reportForm.industries.length) {
        ElMessage.error('请选择至少一个行业类型')
        return
      }
      
      generating.value = true
      try {
        const response = await axios.post('/api/reports/multi-industry/generate', {
          industries: reportForm.industries,
          name: reportForm.name,
          description: reportForm.description
        })
        
        ElMessage.success('报告生成任务已启动')
        createDialogVisible.value = false
        refreshReports()
      } catch (error) {
        ElMessage.error('生成报告失败: ' + (error.response?.data?.detail || error.message))
      } finally {
        generating.value = false
      }
    }
    
    // 查看报告
    const viewReport = (report) => {
      window.open(`/api/reports/${report.id}/view`, '_blank')
    }
    
    // 下载报告
    const downloadReport = (report) => {
      const link = document.createElement('a')
      link.href = `/api/reports/${report.id}/download`
      link.download = report.name
      link.click()
    }
    
    // 删除报告
    const deleteReport = async (report) => {
      try {
        await ElMessageBox.confirm(
          `确定要删除报告 "${report.name}" 吗？`,
          '删除确认',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        )
        
        await axios.delete(`/api/reports/${report.id}`)
        ElMessage.success('报告删除成功')
        refreshReports()
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('删除报告失败')
        }
      }
    }
    
    onMounted(() => {
      refreshReports()
    })
    
    return {
      loading,
      generating,
      createDialogVisible,
      searchQuery,
      filterType,
      filterStatus,
      dateRange,
      reports,
      reportStats,
      pagination,
      reportForm,
      formatFileSize,
      formatDate,
      getTypeColor,
      getTypeText,
      getStatusColor,
      getStatusText,
      handleSearch,
      handleFilter,
      handlePageChange,
      refreshReports,
      showCreateReportDialog,
      generateReport,
      viewReport,
      downloadReport,
      deleteReport
    }
  }
}
</script>

<style scoped>
.reports-page {
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

.stats-section {
  margin-bottom: 20px;
}

.stat-card {
  border: none;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
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
  font-weight: 600;
  color: #409EFF;
  margin-bottom: 4px;
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

.reports-table .report-name {
  display: flex;
  align-items: center;
  gap: 8px;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}
</style> 