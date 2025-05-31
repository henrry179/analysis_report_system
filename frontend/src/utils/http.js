import axios from 'axios'
import { handleError } from './error-handler'
import { showLoading, hideLoading } from './loading'

// 创建 axios 实例
const http = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
http.interceptors.request.use(
  (config) => {
    // 从本地存储获取 token
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    // 显示加载状态
    if (!config.hideLoading) {
      showLoading(config.loadingText)
    }
    
    return config
  },
  (error) => {
    hideLoading()
    return Promise.reject(error)
  }
)

// 响应拦截器
http.interceptors.response.use(
  (response) => {
    hideLoading()
    return response.data
  },
  (error) => {
    hideLoading()
    return Promise.reject(handleError(error))
  }
)

// 封装 GET 请求
const get = (url, params = {}, config = {}) => {
  return http.get(url, { params, ...config })
}

// 封装 POST 请求
const post = (url, data = {}, config = {}) => {
  return http.post(url, data, config)
}

// 封装 PUT 请求
const put = (url, data = {}, config = {}) => {
  return http.put(url, data, config)
}

// 封装 DELETE 请求
const del = (url, config = {}) => {
  return http.delete(url, config)
}

// 封装文件上传请求
const upload = (url, file, onProgress = null, config = {}) => {
  const formData = new FormData()
  formData.append('file', file)

  return http.post(url, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    },
    onUploadProgress: (progressEvent) => {
      if (onProgress) {
        const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total)
        onProgress(progress)
      }
    },
    ...config
  })
}

// 封装文件下载请求
const download = (url, filename, config = {}) => {
  return http.get(url, {
    responseType: 'blob',
    ...config
  }).then((response) => {
    const url = window.URL.createObjectURL(new Blob([response]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', filename)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  })
}

export {
  http,
  get,
  post,
  put,
  del,
  upload,
  download
} 