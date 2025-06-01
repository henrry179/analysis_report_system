<template>
  <div class="analytics">
    <div class="page-header">
      <h1>数据分析中心</h1>
      <div class="header-actions">
        <el-button @click="refreshOverview" :loading="loading">
          <i class="el-icon-refresh"></i> 刷新
        </el-button>
        <el-button type="primary" @click="showUploadDialog">
          <i class="el-icon-upload"></i> 上传数据
        </el-button>
      </div>
    </div>

    <!-- 分析概览 -->
    <div class="overview-section">
      <h2>📊 分析概览</h2>
      <div class="overview-cards">
        <el-card class="overview-card">
          <div class="card-content">
            <div class="card-value">{{ overview.summary.total_analyses }}</div>
            <div class="card-label">总分析数</div>
          </div>
          <i class="el-icon-data-analysis card-icon"></i>
        </el-card>
        
        <el-card class="overview-card">
          <div class="card-content">
            <div class="card-value">{{ overview.summary.active_datasets }}</div>
            <div class="card-label">活跃数据集</div>
          </div>
          <i class="el-icon-files card-icon"></i>
        </el-card>
        
        <el-card class="overview-card">
          <div class="card-content">
            <div class="card-value">{{ overview.summary.recent_reports }}</div>
            <div class="card-label">最近报告</div>
          </div>
          <i class="el-icon-document card-icon"></i>
        </el-card>
        
        <el-card class="overview-card">
          <div class="card-content">
            <div class="card-value">{{ overview.summary.avg_processing_time }}</div>
            <div class="card-label">平均处理时间</div>
          </div>
          <i class="el-icon-timer card-icon"></i>
        </el-card>
      </div>
    </div>

    <!-- 快速分析工具 -->
    <div class="quick-tools-section">
      <h2>⚡ 快速分析工具</h2>
      <div class="tools-grid">
        <el-card class="tool-card" @click="openBasicAnalysis">
          <div class="tool-content">
            <i class="el-icon-pie-chart tool-icon"></i>
            <h3>基础分析</h3>
            <p>描述性统计、数据概览</p>
          </div>
        </el-card>
        
        <el-card class="tool-card" @click="openAdvancedAnalysis">
          <div class="tool-content">
            <i class="el-icon-data-line tool-icon"></i>
            <h3>高级分析</h3>
            <p>相关性分析、模式识别</p>
          </div>
        </el-card>
        
        <el-card class="tool-card" @click="openTrendAnalysis">
          <div class="tool-content">
            <i class="el-icon-trend-charts tool-icon"></i>
            <h3>趋势分析</h3>
            <p>时间序列、预测分析</p>
          </div>
        </el-card>
        
        <el-card class="tool-card" @click="openMetricsCalculation">
          <div class="tool-content">
            <i class="el-icon-s-data tool-icon"></i>
            <h3>指标计算</h3>
            <p>KPI计算、业务指标</p>
          </div>
        </el-card>
      </div>
    </div>

    <!-- 分析历史 -->
    <div class="history-section">
      <div class="section-header">
        <h2>📈 分析历史</h2>
        <el-select
          v-model="historyFilter"
          placeholder="筛选分析类型"
          style="width: 150px"
          @change="fetchAnalysisHistory"
        >
          <el-option label="全部类型" value=""></el-option>
          <el-option label="基础分析" value="basic"></el-option>
          <el-option label="高级分析" value="advanced"></el-option>
          <el-option label="趋势分析" value="trend"></el-option>
          <el-option label="相关性分析" value="correlation"></el-option>
        </el-select>
      </div>
      
      <el-table
        :data="analysisHistory"
        v-loading="historyLoading"
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="analysis_type" label="分析类型" width="120">
          <template #default="scope">
            <el-tag :type="getAnalysisTypeColor(scope.row.analysis_type)">
              {{ getAnalysisTypeText(scope.row.analysis_type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="data_source" label="数据源" width="150"></el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getStatusColor(scope.row.status)">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="duration" label="耗时" width="100"></el-table-column>
        <el-table-column prop="analyst" label="分析师" width="120"></el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="160">
          <template #default="scope">
            {{ formatDate(scope.row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120">
          <template #default="scope">
            <el-button
              size="small"
              @click="viewAnalysisResult(scope.row)"
              :disabled="scope.row.status !== 'completed'"
            >
              查看结果
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="pagination-wrapper">
        <el-pagination
          @current-change="handleHistoryPageChange"
          :current-page="historyPagination.page"
          :page-size="historyPagination.size"
          layout="prev, pager, next, total"
          :total="historyPagination.total"
        >
        </el-pagination>
      </div>
    </div>

    <!-- 数据上传对话框 -->
    <el-dialog
      title="上传数据文件"
      v-model="uploadDialogVisible"
      width="600px"
    >
      <div class="upload-section">
        <el-upload
          ref="uploadRef"
          :auto-upload="false"
          :on-change="handleFileChange"
          :accept="'.csv,.xlsx,.json'"
          drag
          multiple
          :limit="1"
        >
          <i class="el-icon-upload"></i>
          <div class="el-upload__text">
            将文件拖到此处，或<em>点击上传</em>
          </div>
          <div class="el-upload__tip" slot="tip">
            支持 CSV、Excel、JSON 格式文件，文件大小不超过 100MB
          </div>
        </el-upload>
        
        <div v-if="uploadFile" class="file-info">
          <h4>文件信息：</h4>
          <p>文件名: {{ uploadFile.name }}</p>
          <p>文件大小: {{ formatFileSize(uploadFile.size) }}</p>
          <p>文件类型: {{ uploadFile.name.split('.').pop().toUpperCase() }}</p>
        </div>
        
        <div class="analysis-options">
          <h4>分析选项：</h4>
          <el-radio-group v-model="uploadAnalysisType">
            <el-radio label="basic">基础分析</el-radio>
            <el-radio label="advanced">高级分析</el-radio>
            <el-radio label="descriptive">描述性分析</el-radio>
          </el-radio-group>
        </div>
      </div>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="uploadDialogVisible = false">取消</el-button>
          <el-button
            type="primary"
            @click="handleUploadAnalysis"
            :loading="uploading"
            :disabled="!uploadFile"
          >
            开始分析
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 基础分析对话框 -->
    <el-dialog
      title="基础数据分析"
      v-model="basicAnalysisDialogVisible"
      width="500px"
    >
      <el-form :model="basicAnalysisForm" label-width="100px">
        <el-form-item label="数据源">
          <el-input v-model="basicAnalysisForm.data_source" placeholder="请输入数据源名称"></el-input>
        </el-form-item>
        <el-form-item label="分析类型">
          <el-select v-model="basicAnalysisForm.analysis_type" style="width: 100%">
            <el-option label="描述性分析" value="descriptive"></el-option>
            <el-option label="趋势分析" value="trend"></el-option>
            <el-option label="相关性分析" value="correlation"></el-option>
            <el-option label="综合分析" value="comprehensive"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="basicAnalysisDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="runBasicAnalysis" :loading="analyzing">
            开始分析
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 趋势分析对话框 -->
    <el-dialog
      title="趋势分析"
      v-model="trendAnalysisDialogVisible"
      width="500px"
    >
      <el-form :model="trendAnalysisForm" label-width="100px">
        <el-form-item label="指标名称">
          <el-input v-model="trendAnalysisForm.metric" placeholder="请输入要分析的指标"></el-input>
        </el-form-item>
        <el-form-item label="分析周期">
          <el-select v-model="trendAnalysisForm.period" style="width: 100%">
            <el-option label="最近30天" value="30d"></el-option>
            <el-option label="最近90天" value="90d"></el-option>
            <el-option label="最近1年" value="365d"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="trendAnalysisDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="runTrendAnalysis" :loading="analyzing">
            开始分析
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

export default {
  name: 'Analytics',
  setup() {
    const loading = ref(false)
    const historyLoading = ref(false)
    const uploading = ref(false)
    const analyzing = ref(false)
    
    const uploadDialogVisible = ref(false)
    const basicAnalysisDialogVisible = ref(false)
    const trendAnalysisDialogVisible = ref(false)
    
    const historyFilter = ref('')
    const uploadFile = ref(null)
    const uploadAnalysisType = ref('basic')
    
    const overview = ref({
      summary: {
        total_analyses: 0,
        active_datasets: 0,
        recent_reports: 0,
        avg_processing_time: '0秒'
      },
      quick_stats: {
        data_quality_score: 0,
        model_accuracy: 0,
        processing_efficiency: 0
      }
    })
    
    const analysisHistory = ref([])
    const historyPagination = reactive({
      page: 1,
      size: 10,
      total: 0
    })
    
    const basicAnalysisForm = reactive({
      data_source: '',
      analysis_type: 'descriptive',
      parameters: {}
    })
    
    const trendAnalysisForm = reactive({
      metric: '',
      period: '30d'
    })
    
    // 获取分析概览
    const fetchOverview = async () => {
      loading.value = true
      try {
        const response = await axios.get('/api/analytics/overview')
        overview.value = response.data.overview
      } catch (error) {
        ElMessage.error('获取分析概览失败: ' + (error.response?.data?.detail || error.message))
      } finally {
        loading.value = false
      }
    }
    
    // 获取分析历史
    const fetchAnalysisHistory = async () => {
      historyLoading.value = true
      try {
        const params = {
          page: historyPagination.page,
          size: historyPagination.size,
          analysis_type: historyFilter.value || undefined
        }
        
        const response = await axios.get('/api/analytics/analysis-history', { params })
        analysisHistory.value = response.data.result.history
        historyPagination.total = response.data.result.pagination.total
      } catch (error) {
        ElMessage.error('获取分析历史失败: ' + (error.response?.data?.detail || error.message))
      } finally {
        historyLoading.value = false
      }
    }
    
    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return '-'
      return new Date(dateString).toLocaleString('zh-CN')
    }
    
    // 格式化文件大小
    const formatFileSize = (bytes) => {
      if (bytes === 0) return '0 Bytes'
      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    }
    
    // 获取分析类型颜色
    const getAnalysisTypeColor = (type) => {
      const colors = {
        basic: 'info',
        advanced: 'warning',
        trend: 'success',
        correlation: 'primary'
      }
      return colors[type] || 'info'
    }
    
    // 获取分析类型文本
    const getAnalysisTypeText = (type) => {
      const texts = {
        basic: '基础分析',
        advanced: '高级分析',
        trend: '趋势分析',
        correlation: '相关性分析'
      }
      return texts[type] || type
    }
    
    // 获取状态颜色
    const getStatusColor = (status) => {
      const colors = {
        completed: 'success',
        failed: 'danger',
        in_progress: 'warning'
      }
      return colors[status] || 'info'
    }
    
    // 获取状态文本
    const getStatusText = (status) => {
      const texts = {
        completed: '已完成',
        failed: '失败',
        in_progress: '进行中'
      }
      return texts[status] || status
    }
    
    // 刷新概览
    const refreshOverview = () => {
      fetchOverview()
      fetchAnalysisHistory()
    }
    
    // 显示上传对话框
    const showUploadDialog = () => {
      uploadFile.value = null
      uploadAnalysisType.value = 'basic'
      uploadDialogVisible.value = true
    }
    
    // 处理文件变化
    const handleFileChange = (file) => {
      uploadFile.value = file.raw
    }
    
    // 处理文件上传分析
    const handleUploadAnalysis = async () => {
      if (!uploadFile.value) {
        ElMessage.error('请先选择文件')
        return
      }
      
      uploading.value = true
      try {
        const formData = new FormData()
        formData.append('file', uploadFile.value)
        
        const response = await axios.post(
          `/api/analytics/upload-data?analysis_type=${uploadAnalysisType.value}`,
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          }
        )
        
        ElMessage.success('文件上传分析成功')
        uploadDialogVisible.value = false
        fetchAnalysisHistory()
      } catch (error) {
        ElMessage.error('文件上传分析失败: ' + (error.response?.data?.detail || error.message))
      } finally {
        uploading.value = false
      }
    }
    
    // 打开基础分析
    const openBasicAnalysis = () => {
      basicAnalysisForm.data_source = ''
      basicAnalysisForm.analysis_type = 'descriptive'
      basicAnalysisDialogVisible.value = true
    }
    
    // 打开高级分析
    const openAdvancedAnalysis = () => {
      ElMessage.info('高级分析功能开发中...')
    }
    
    // 打开趋势分析
    const openTrendAnalysis = () => {
      trendAnalysisForm.metric = ''
      trendAnalysisForm.period = '30d'
      trendAnalysisDialogVisible.value = true
    }
    
    // 打开指标计算
    const openMetricsCalculation = () => {
      ElMessage.info('指标计算功能开发中...')
    }
    
    // 运行基础分析
    const runBasicAnalysis = async () => {
      if (!basicAnalysisForm.data_source) {
        ElMessage.error('请输入数据源名称')
        return
      }
      
      analyzing.value = true
      try {
        const response = await axios.post('/api/analytics/basic-analysis', basicAnalysisForm)
        ElMessage.success('基础分析完成')
        basicAnalysisDialogVisible.value = false
        fetchAnalysisHistory()
      } catch (error) {
        ElMessage.error('基础分析失败: ' + (error.response?.data?.detail || error.message))
      } finally {
        analyzing.value = false
      }
    }
    
    // 运行趋势分析
    const runTrendAnalysis = async () => {
      if (!trendAnalysisForm.metric) {
        ElMessage.error('请输入要分析的指标')
        return
      }
      
      analyzing.value = true
      try {
        const response = await axios.get('/api/analytics/trend-analysis', {
          params: trendAnalysisForm
        })
        ElMessage.success('趋势分析完成')
        trendAnalysisDialogVisible.value = false
        fetchAnalysisHistory()
      } catch (error) {
        ElMessage.error('趋势分析失败: ' + (error.response?.data?.detail || error.message))
      } finally {
        analyzing.value = false
      }
    }
    
    // 查看分析结果
    const viewAnalysisResult = (analysis) => {
      ElMessage.info(`查看分析结果功能开发中... (分析ID: ${analysis.id})`)
    }
    
    // 处理历史分页变化
    const handleHistoryPageChange = (page) => {
      historyPagination.page = page
      fetchAnalysisHistory()
    }
    
    onMounted(() => {
      refreshOverview()
    })
    
    return {
      loading,
      historyLoading,
      uploading,
      analyzing,
      uploadDialogVisible,
      basicAnalysisDialogVisible,
      trendAnalysisDialogVisible,
      historyFilter,
      uploadFile,
      uploadAnalysisType,
      overview,
      analysisHistory,
      historyPagination,
      basicAnalysisForm,
      trendAnalysisForm,
      formatDate,
      formatFileSize,
      getAnalysisTypeColor,
      getAnalysisTypeText,
      getStatusColor,
      getStatusText,
      refreshOverview,
      showUploadDialog,
      handleFileChange,
      handleUploadAnalysis,
      openBasicAnalysis,
      openAdvancedAnalysis,
      openTrendAnalysis,
      openMetricsCalculation,
      runBasicAnalysis,
      runTrendAnalysis,
      viewAnalysisResult,
      handleHistoryPageChange,
      fetchAnalysisHistory
    }
  }
}
</script>

<style scoped>
.analytics {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.page-header h1 {
  margin: 0;
  color: #303133;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.overview-section,
.quick-tools-section,
.history-section {
  margin-bottom: 30px;
}

.overview-section h2,
.quick-tools-section h2,
.history-section h2 {
  margin-bottom: 20px;
  color: #303133;
  font-size: 18px;
}

.overview-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.overview-card {
  border: none;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.overview-card :deep(.el-card__body) {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
}

.card-content {
  flex: 1;
}

.card-value {
  font-size: 24px;
  font-weight: bold;
  color: #409EFF;
  margin-bottom: 5px;
}

.card-label {
  font-size: 14px;
  color: #909399;
}

.card-icon {
  font-size: 32px;
  color: #409EFF;
  opacity: 0.8;
}

.tools-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.tool-card {
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.tool-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.15);
}

.tool-content {
  text-align: center;
  padding: 20px;
}

.tool-icon {
  font-size: 48px;
  color: #409EFF;
  margin-bottom: 15px;
}

.tool-content h3 {
  margin: 0 0 10px 0;
  color: #303133;
}

.tool-content p {
  margin: 0;
  color: #909399;
  font-size: 14px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.pagination-wrapper {
  margin-top: 20px;
  text-align: right;
}

.upload-section {
  margin-bottom: 20px;
}

.file-info {
  margin: 20px 0;
  padding: 15px;
  background: #f5f7fa;
  border-radius: 4px;
}

.file-info h4 {
  margin: 0 0 10px 0;
  color: #303133;
}

.file-info p {
  margin: 5px 0;
  color: #606266;
}

.analysis-options {
  margin: 20px 0;
}

.analysis-options h4 {
  margin: 0 0 10px 0;
  color: #303133;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

:deep(.el-upload-dragger) {
  width: 100%;
}
</style> 