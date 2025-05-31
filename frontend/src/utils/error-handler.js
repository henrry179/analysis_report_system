import { ElMessage } from 'element-plus'
import router from '@/router'

// 错误类型
const ErrorTypes = {
  NETWORK_ERROR: 'NETWORK_ERROR',
  AUTH_ERROR: 'AUTH_ERROR',
  VALIDATION_ERROR: 'VALIDATION_ERROR',
  SERVER_ERROR: 'SERVER_ERROR',
  UNKNOWN_ERROR: 'UNKNOWN_ERROR'
}

// 错误消息映射
const ErrorMessages = {
  [ErrorTypes.NETWORK_ERROR]: '网络连接失败，请检查网络设置',
  [ErrorTypes.AUTH_ERROR]: '认证失败，请重新登录',
  [ErrorTypes.VALIDATION_ERROR]: '输入数据验证失败',
  [ErrorTypes.SERVER_ERROR]: '服务器错误，请稍后重试',
  [ErrorTypes.UNKNOWN_ERROR]: '发生未知错误，请稍后重试'
}

// 处理 HTTP 错误
const handleHttpError = (error) => {
  if (!error.response) {
    return {
      type: ErrorTypes.NETWORK_ERROR,
      message: '网络连接失败，请检查网络设置'
    }
  }

  const { status } = error.response

  switch (status) {
    case 400:
      return {
        type: ErrorTypes.VALIDATION_ERROR,
        message: error.response.data.detail || ErrorMessages[ErrorTypes.VALIDATION_ERROR]
      }
    case 401:
      return {
        type: ErrorTypes.AUTH_ERROR,
        message: ErrorMessages[ErrorTypes.AUTH_ERROR]
      }
    case 403:
      return {
        type: ErrorTypes.AUTH_ERROR,
        message: '没有权限执行此操作'
      }
    case 404:
      return {
        type: ErrorTypes.SERVER_ERROR,
        message: '请求的资源不存在'
      }
    case 500:
      return {
        type: ErrorTypes.SERVER_ERROR,
        message: ErrorMessages[ErrorTypes.SERVER_ERROR]
      }
    default:
      return {
        type: ErrorTypes.UNKNOWN_ERROR,
        message: ErrorMessages[ErrorTypes.UNKNOWN_ERROR]
      }
  }
}

// 处理业务错误
const handleBusinessError = (error) => {
  if (error.code && error.message) {
    return {
      type: ErrorTypes.SERVER_ERROR,
      message: error.message
    }
  }
  return {
    type: ErrorTypes.UNKNOWN_ERROR,
    message: ErrorMessages[ErrorTypes.UNKNOWN_ERROR]
  }
}

// 处理错误
const handleError = (error, showMessage = true) => {
  let errorInfo

  if (error.response) {
    errorInfo = handleHttpError(error)
  } else if (error.code) {
    errorInfo = handleBusinessError(error)
  } else {
    errorInfo = {
      type: ErrorTypes.UNKNOWN_ERROR,
      message: ErrorMessages[ErrorTypes.UNKNOWN_ERROR]
    }
  }

  // 显示错误消息
  if (showMessage) {
    ElMessage.error(errorInfo.message)
  }

  // 处理认证错误
  if (errorInfo.type === ErrorTypes.AUTH_ERROR) {
    // 清除本地存储的认证信息
    localStorage.removeItem('token')
    // 重定向到登录页面
    router.push('/login')
  }

  return errorInfo
}

// 创建错误处理装饰器
const withErrorHandling = (fn) => {
  return async (...args) => {
    try {
      return await fn(...args)
    } catch (error) {
      return handleError(error)
    }
  }
}

export {
  ErrorTypes,
  ErrorMessages,
  handleError,
  withErrorHandling
} 