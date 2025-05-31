import { ref } from 'vue'
import { ElLoading } from 'element-plus'

// 全局加载状态
const loading = ref(false)
let loadingInstance = null

// 显示加载状态
const showLoading = (text = '加载中...') => {
  loading.value = true
  loadingInstance = ElLoading.service({
    lock: true,
    text,
    background: 'rgba(0, 0, 0, 0.7)'
  })
}

// 隐藏加载状态
const hideLoading = () => {
  loading.value = false
  if (loadingInstance) {
    loadingInstance.close()
    loadingInstance = null
  }
}

// 创建加载状态装饰器
const withLoading = (fn, loadingText = '加载中...') => {
  return async (...args) => {
    showLoading(loadingText)
    try {
      const result = await fn(...args)
      return result
    } finally {
      hideLoading()
    }
  }
}

// 创建加载状态组件
const useLoading = () => {
  return {
    loading,
    showLoading,
    hideLoading,
    withLoading
  }
}

export {
  loading,
  showLoading,
  hideLoading,
  withLoading,
  useLoading
} 