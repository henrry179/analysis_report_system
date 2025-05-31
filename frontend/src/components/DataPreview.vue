<template>
  <div class="data-preview">
    <el-dialog
      v-model="visible"
      :title="title"
      width="80%"
      :before-close="handleClose"
    >
      <div v-if="loading" class="loading-container">
        <el-skeleton :rows="10" animated />
      </div>
      
      <template v-else>
        <div class="preview-container">
          <!-- 数据概览 -->
          <div class="preview-section">
            <h3>数据概览</h3>
            <el-descriptions :column="3" border>
              <el-descriptions-item label="文件大小">
                {{ formatFileSize(fileSize) }}
              </el-descriptions-item>
              <el-descriptions-item label="行数">
                {{ rowCount }}
              </el-descriptions-item>
              <el-descriptions-item label="列数">
                {{ columnCount }}
              </el-descriptions-item>
            </el-descriptions>
          </div>
          
          <!-- 数据预览 -->
          <div class="preview-section">
            <h3>数据预览</h3>
            <el-table
              :data="previewData"
              style="width: 100%"
              height="400"
              border
            >
              <el-table-column
                v-for="column in columns"
                :key="column"
                :prop="column"
                :label="column"
                show-overflow-tooltip
              />
            </el-table>
            
            <div class="pagination-container">
              <el-pagination
                v-model:current-page="currentPage"
                v-model:page-size="pageSize"
                :page-sizes="[10, 20, 50, 100]"
                :total="rowCount"
                layout="total, sizes, prev, pager, next"
                @size-change="handleSizeChange"
                @current-change="handleCurrentChange"
              />
            </div>
          </div>
          
          <!-- 数据统计 -->
          <div class="preview-section">
            <h3>数据统计</h3>
            <el-table
              :data="statistics"
              style="width: 100%"
              border
            >
              <el-table-column prop="column" label="列名" />
              <el-table-column prop="type" label="数据类型" />
              <el-table-column prop="nonNull" label="非空值数量" />
              <el-table-column prop="null" label="空值数量" />
              <el-table-column prop="unique" label="唯一值数量" />
            </el-table>
          </div>
        </div>
        
        <div class="preview-actions">
          <el-button type="primary" @click="handleExport">
            导出数据
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

export default {
  name: 'DataPreview',
  props: {
    visible: {
      type: Boolean,
      default: false
    },
    title: {
      type: String,
      default: '数据预览'
    },
    fileId: {
      type: String,
      required: true
    }
  },
  emits: ['update:visible'],
  setup(props, { emit }) {
    const loading = ref(false)
    const fileSize = ref(0)
    const rowCount = ref(0)
    const columnCount = ref(0)
    const columns = ref([])
    const previewData = ref([])
    const statistics = ref([])
    const currentPage = ref(1)
    const pageSize = ref(10)
    
    // 加载数据
    const loadData = async () => {
      loading.value = true
      try {
        // 获取数据概览
        const overviewResponse = await axios.get(`/api/data/${props.fileId}/overview`)
        const { file_size, row_count, column_count, columns: cols } = overviewResponse.data
        fileSize.value = file_size
        rowCount.value = row_count
        columnCount.value = column_count
        columns.value = cols
        
        // 获取数据预览
        await loadPreviewData()
        
        // 获取数据统计
        const statsResponse = await axios.get(`/api/data/${props.fileId}/statistics`)
        statistics.value = statsResponse.data
      } catch (error) {
        ElMessage.error('加载数据失败')
      } finally {
        loading.value = false
      }
    }
    
    // 加载预览数据
    const loadPreviewData = async () => {
      try {
        const response = await axios.get(`/api/data/${props.fileId}/preview`, {
          params: {
            page: currentPage.value,
            page_size: pageSize.value
          }
        })
        previewData.value = response.data
      } catch (error) {
        ElMessage.error('加载预览数据失败')
      }
    }
    
    // 处理分页大小变化
    const handleSizeChange = (val) => {
      pageSize.value = val
      loadPreviewData()
    }
    
    // 处理页码变化
    const handleCurrentChange = (val) => {
      currentPage.value = val
      loadPreviewData()
    }
    
    // 处理导出
    const handleExport = async () => {
      try {
        const response = await axios.get(`/api/data/${props.fileId}/export`, {
          responseType: 'blob'
        })
        
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `data_export_${props.fileId}.csv`)
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        
        ElMessage.success('导出成功')
      } catch (error) {
        ElMessage.error('导出失败')
      }
    }
    
    // 处理关闭
    const handleClose = () => {
      emit('update:visible', false)
    }
    
    // 格式化文件大小
    const formatFileSize = (bytes) => {
      if (bytes === 0) return '0 B'
      const k = 1024
      const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    }
    
    // 监听可见性变化
    watch(() => props.visible, (newVisible) => {
      if (newVisible) {
        loadData()
      }
    })
    
    return {
      loading,
      fileSize,
      rowCount,
      columnCount,
      columns,
      previewData,
      statistics,
      currentPage,
      pageSize,
      handleSizeChange,
      handleCurrentChange,
      handleExport,
      handleClose,
      formatFileSize
    }
  }
}
</script>

<style scoped>
.data-preview {
  width: 100%;
}

.loading-container {
  padding: 20px;
}

.preview-container {
  padding: 20px;
}

.preview-section {
  margin-bottom: 40px;
}

.preview-section h3 {
  margin-bottom: 20px;
  text-align: center;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.preview-actions {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}
</style> 