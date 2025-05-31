// 主题配置
export const theme = {
  // 颜色
  colors: {
    primary: '#409EFF',
    success: '#67C23A',
    warning: '#E6A23C',
    danger: '#F56C6C',
    info: '#909399',
    text: {
      primary: '#303133',
      regular: '#606266',
      secondary: '#909399',
      placeholder: '#C0C4CC'
    },
    border: {
      base: '#DCDFE6',
      light: '#E4E7ED',
      lighter: '#EBEEF5',
      extraLight: '#F2F6FC'
    },
    background: {
      base: '#F5F7FA',
      light: '#FFFFFF'
    }
  },
  
  // 字体
  font: {
    family: {
      base: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
      code: 'Consolas, Monaco, "Andale Mono", "Ubuntu Mono", monospace'
    },
    size: {
      xs: '12px',
      sm: '14px',
      base: '16px',
      lg: '18px',
      xl: '20px',
      xxl: '24px'
    },
    weight: {
      light: 300,
      regular: 400,
      medium: 500,
      bold: 600
    },
    lineHeight: {
      tight: 1.2,
      base: 1.5,
      loose: 1.8
    }
  },
  
  // 间距
  spacing: {
    xs: '4px',
    sm: '8px',
    base: '16px',
    lg: '24px',
    xl: '32px',
    xxl: '48px'
  },
  
  // 圆角
  borderRadius: {
    sm: '2px',
    base: '4px',
    lg: '8px',
    xl: '12px',
    circle: '50%'
  },
  
  // 阴影
  boxShadow: {
    base: '0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04)',
    light: '0 2px 12px 0 rgba(0, 0, 0, 0.1)',
    dark: '0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.12)'
  },
  
  // 过渡
  transition: {
    base: 'all 0.3s ease-in-out',
    fast: 'all 0.2s ease-in-out',
    slow: 'all 0.4s ease-in-out'
  },
  
  // 断点
  breakpoints: {
    xs: '480px',
    sm: '768px',
    md: '992px',
    lg: '1200px',
    xl: '1920px'
  }
} 