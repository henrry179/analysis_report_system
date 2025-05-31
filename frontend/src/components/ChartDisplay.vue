<template>
  <div class="chart-display">
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
        <div class="chart-container">
          <!-- 描述性统计图表 -->
          <div v-if="type === 'descriptive'" class="chart-section">
            <h3>描述性统计</h3>
            <div class="chart-grid">
              <div v-for="(chart, index) in descriptiveCharts" :key="index" class="chart-item">
                <div ref="chartRefs" class="chart"></div>
              </div>
            </div>
          </div>
          
          <!-- 相关性分析图表 -->
          <div v-if="type === 'correlation'" class="chart-section">
            <h3>相关性分析</h3>
            <div class="chart-grid">
              <div class="chart-item full-width">
                <div ref="correlationChartRef" class="chart"></div>
              </div>
            </div>
          </div>
          
          <!-- 趋势分析图表 -->
          <div v-if="type === 'trend'" class="chart-section">
            <h3>趋势分析</h3>
            <div class="chart-grid">
              <div v-for="(chart, index) in trendCharts" :key="index" class="chart-item">
                <div ref="chartRefs" class="chart"></div>
              </div>
            </div>
          </div>
          
          <!-- 预测分析图表 -->
          <div v-if="type === 'forecast'" class="chart-section">
            <h3>预测分析</h3>
            <div class="chart-grid">
              <div v-for="(chart, index) in forecastCharts" :key="index" class="chart-item">
                <div ref="chartRefs" class="chart"></div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="chart-actions">
          <el-button type="primary" @click="handleExport">
            导出图表
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted, watch, nextTick } from 'vue'
import * as echarts from 'echarts'
import { ElMessage } from 'element-plus'

export default {
  name: 'ChartDisplay',
  props: {
    visible: {
      type: Boolean,
      default: false
    },
    title: {
      type: String,
      default: '图表展示'
    },
    type: {
      type: String,
      required: true,
      validator: (value) => ['descriptive', 'correlation', 'trend', 'forecast'].includes(value)
    },
    data: {
      type: Object,
      required: true
    }
  },
  emits: ['update:visible'],
  setup(props, { emit }) {
    const loading = ref(false)
    const chartRefs = ref([])
    const correlationChartRef = ref(null)
    let charts = []
    
    // 初始化图表
    const initCharts = async () => {
      await nextTick()
      
      // 销毁现有图表
      charts.forEach(chart => chart.dispose())
      charts = []
      
      if (props.type === 'correlation') {
        const chart = echarts.init(correlationChartRef.value)
        charts.push(chart)
        renderCorrelationChart(chart)
      } else {
        chartRefs.value.forEach((el, index) => {
          const chart = echarts.init(el)
          charts.push(chart)
          
          switch (props.type) {
            case 'descriptive':
              renderDescriptiveChart(chart, index)
              break
            case 'trend':
              renderTrendChart(chart, index)
              break
            case 'forecast':
              renderForecastChart(chart, index)
              break
          }
        })
      }
    }
    
    // 渲染描述性统计图表
    const renderDescriptiveChart = (chart, index) => {
      const { data } = props
      const column = Object.keys(data.descriptive)[index]
      const stats = data.descriptive[column]
      
      const option = {
        title: {
          text: column,
          left: 'center'
        },
        tooltip: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'category',
          data: ['最小值', '最大值', '平均值', '中位数', '标准差']
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            type: 'bar',
            data: [
              stats.min,
              stats.max,
              stats.mean,
              stats.median,
              stats.std
            ]
          }
        ]
      }
      
      chart.setOption(option)
    }
    
    // 渲染相关性分析图表
    const renderCorrelationChart = (chart) => {
      const { data } = props
      const { correlation_matrix, columns } = data.correlation
      
      const option = {
        title: {
          text: '相关性热力图',
          left: 'center'
        },
        tooltip: {
          position: 'top'
        },
        grid: {
          height: '50%',
          top: '10%'
        },
        xAxis: {
          type: 'category',
          data: columns,
          splitArea: {
            show: true
          }
        },
        yAxis: {
          type: 'category',
          data: columns,
          splitArea: {
            show: true
          }
        },
        visualMap: {
          min: -1,
          max: 1,
          calculable: true,
          orient: 'horizontal',
          left: 'center',
          bottom: '15%'
        },
        series: [
          {
            type: 'heatmap',
            data: correlation_matrix.flatMap((row, i) =>
              row.map((value, j) => [i, j, value])
            ),
            label: {
              show: true
            },
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      }
      
      chart.setOption(option)
    }
    
    // 渲染趋势分析图表
    const renderTrendChart = (chart, index) => {
      const { data } = props
      const column = Object.keys(data.trend)[index]
      const { values, moving_average } = data.trend[column]
      
      const option = {
        title: {
          text: column,
          left: 'center'
        },
        tooltip: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'category',
          data: Array.from({ length: values.length }, (_, i) => i + 1)
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            name: '原始数据',
            type: 'line',
            data: values
          },
          {
            name: '移动平均',
            type: 'line',
            data: moving_average
          }
        ]
      }
      
      chart.setOption(option)
    }
    
    // 渲染预测分析图表
    const renderForecastChart = (chart, index) => {
      const { data } = props
      const column = Object.keys(data.forecast)[index]
      const { actual, predicted, confidence_interval } = data.forecast[column]
      
      const option = {
        title: {
          text: column,
          left: 'center'
        },
        tooltip: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'category',
          data: Array.from({ length: actual.length }, (_, i) => i + 1)
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            name: '实际值',
            type: 'line',
            data: actual
          },
          {
            name: '预测值',
            type: 'line',
            data: predicted
          },
          {
            name: '置信区间',
            type: 'line',
            data: confidence_interval.upper,
            lineStyle: {
              opacity: 0
            },
            stack: 'confidence',
            areaStyle: {
              opacity: 0.3
            }
          },
          {
            name: '置信区间',
            type: 'line',
            data: confidence_interval.lower,
            lineStyle: {
              opacity: 0
            },
            areaStyle: {
              opacity: 0.3
            }
          }
        ]
      }
      
      chart.setOption(option)
    }
    
    // 处理导出
    const handleExport = () => {
      try {
        charts.forEach((chart, index) => {
          const url = chart.getDataURL()
          const link = document.createElement('a')
          link.download = `chart_${index + 1}.png`
          link.href = url
          link.click()
        })
        ElMessage.success('导出成功')
      } catch (error) {
        ElMessage.error('导出失败')
      }
    }
    
    // 处理关闭
    const handleClose = () => {
      emit('update:visible', false)
    }
    
    // 监听数据变化
    watch(() => props.data, () => {
      if (props.visible) {
        initCharts()
      }
    }, { deep: true })
    
    // 监听可见性变化
    watch(() => props.visible, (newVisible) => {
      if (newVisible) {
        initCharts()
      }
    })
    
    // 监听窗口大小变化
    const handleResize = () => {
      charts.forEach(chart => chart.resize())
    }
    
    onMounted(() => {
      window.addEventListener('resize', handleResize)
    })
    
    return {
      loading,
      chartRefs,
      correlationChartRef,
      handleExport,
      handleClose
    }
  }
}
</script>

<style scoped>
.chart-display {
  width: 100%;
}

.loading-container {
  padding: 20px;
}

.chart-container {
  padding: 20px;
}

.chart-section {
  margin-bottom: 40px;
}

.chart-section h3 {
  margin-bottom: 20px;
  text-align: center;
}

.chart-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 20px;
}

.chart-item {
  background-color: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.chart-item.full-width {
  grid-column: 1 / -1;
}

.chart {
  width: 100%;
  height: 300px;
}

.chart-actions {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}
</style> 