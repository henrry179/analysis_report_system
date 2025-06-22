<template>
  <div id="app">
    <!-- 登录页面 -->
    <template v-if="isLoginPage">
      <router-view></router-view>
    </template>
    
    <!-- 主布局 -->
    <template v-else>
      <el-container class="app-container">
        <!-- 顶部导航栏 -->
        <el-header class="app-header">
          <div class="header-content">
            <div class="logo-section">
              <div class="logo">📊</div>
              <h2 class="system-title">业务分析报告系统</h2>
            </div>
            
            <div class="header-actions">
              <!-- 通知 -->
              <el-badge :value="notificationCount" class="notification-badge">
                <el-button icon="Bell" circle @click="showNotifications = true"></el-button>
              </el-badge>
              
              <!-- 用户菜单 -->
              <el-dropdown @command="handleUserCommand" placement="bottom-end">
                <div class="user-info">
                  <el-avatar :size="32" :src="userAvatar">{{ userName?.charAt(0)?.toUpperCase() }}</el-avatar>
                  <span class="user-name">{{ userName }}</span>
                  <el-icon><ArrowDown /></el-icon>
                </div>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item command="profile">
                      <el-icon><User /></el-icon> 个人资料
                    </el-dropdown-item>
                    <el-dropdown-item command="settings">
                      <el-icon><Setting /></el-icon> 系统设置
                    </el-dropdown-item>
                    <el-dropdown-item divided command="logout">
                      <el-icon><SwitchButton /></el-icon> 退出登录
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
          </div>
        </el-header>
        
        <el-container>
          <!-- 侧边导航栏 -->
          <el-aside :width="sidebarCollapsed ? '64px' : '240px'" class="app-sidebar">
            <div class="sidebar-content">
              <div class="sidebar-toggle">
                <el-button
                  @click="toggleSidebar"
                  :icon="sidebarCollapsed ? 'Expand' : 'Fold'"
                  circle
                  size="small"
                ></el-button>
              </div>
              
              <el-menu
                :default-active="activeRoute"
                class="sidebar-menu"
                :collapse="sidebarCollapsed"
                router
                unique-opened
              >
                <el-menu-item index="/dashboard">
                  <el-icon><Odometer /></el-icon>
                  <span>仪表盘</span>
                </el-menu-item>
                
                <el-menu-item index="/analytics">
                  <el-icon><DataAnalysis /></el-icon>
                  <span>数据分析</span>
                </el-menu-item>
                
                <el-menu-item index="/reports">
                  <el-icon><Document /></el-icon>
                  <span>报告管理</span>
                </el-menu-item>
                
                <el-menu-item index="/users" v-if="isAdmin">
                  <el-icon><UserFilled /></el-icon>
                  <span>用户管理</span>
                </el-menu-item>
                
                <el-menu-item index="/settings" v-if="isAdmin">
                  <el-icon><Setting /></el-icon>
                  <span>系统设置</span>
                </el-menu-item>
              </el-menu>
            </div>
          </el-aside>
          
          <!-- 主内容区域 -->
          <el-main class="app-main">
            <div class="main-content">
              <!-- 面包屑导航 -->
              <el-breadcrumb class="breadcrumb" separator="/">
                <el-breadcrumb-item :to="{ path: '/dashboard' }">首页</el-breadcrumb-item>
                <el-breadcrumb-item v-for="breadcrumb in breadcrumbs" :key="breadcrumb.path">
                  {{ breadcrumb.title }}
                </el-breadcrumb-item>
              </el-breadcrumb>
              
              <!-- 路由视图 -->
              <div class="route-content">
                <router-view v-slot="{ Component }">
                  <transition name="fade" mode="out-in">
                    <component :is="Component" />
                  </transition>
                </router-view>
              </div>
            </div>
          </el-main>
        </el-container>
      </el-container>
      
      <!-- 通知抽屉 -->
      <el-drawer
        v-model="showNotifications"
        title="系统通知"
        direction="rtl"
        size="400px"
      >
        <div class="notifications-content">
          <el-empty v-if="notifications.length === 0" description="暂无通知"></el-empty>
          <div v-else>
            <div
              v-for="notification in notifications"
              :key="notification.id"
              class="notification-item"
              :class="{ 'unread': !notification.read }"
            >
              <el-icon :class="`notification-icon ${notification.type}`">
                <Bell v-if="notification.type === 'info'" />
                <Warning v-if="notification.type === 'warning'" />
                <CircleCheck v-if="notification.type === 'success'" />
                <CircleClose v-if="notification.type === 'error'" />
              </el-icon>
              <div class="notification-content">
                <div class="notification-title">{{ notification.title }}</div>
                <div class="notification-message">{{ notification.message }}</div>
                <div class="notification-time">{{ formatTime(notification.time) }}</div>
              </div>
            </div>
          </div>
        </div>
      </el-drawer>
    </template>
  </div>
</template>

<script>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  ArrowDown,
  User,
  Setting,
  SwitchButton,
  Odometer,
  DataAnalysis,
  Document,
  UserFilled,
  Bell,
  Warning,
  CircleCheck,
  CircleClose
} from '@element-plus/icons-vue'

export default {
  name: 'App',
  components: {
    ArrowDown,
    User,
    Setting,
    SwitchButton,
    Odometer,
    DataAnalysis,
    Document,
    UserFilled,
    Bell,
    Warning,
    CircleCheck,
    CircleClose
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    
    const sidebarCollapsed = ref(false)
    const showNotifications = ref(false)
    const userName = ref(localStorage.getItem('userName') || 'Admin')
    const userRole = ref(localStorage.getItem('userRole') || 'admin')
    const userAvatar = ref('')
    
    const notifications = ref([
      {
        id: 1,
        type: 'success',
        title: '报告生成完成',
        message: '零售分析报告已成功生成',
        time: new Date(),
        read: false
      },
      {
        id: 2,
        type: 'info',
        title: '系统更新',
        message: '系统已更新至v4.0版本',
        time: new Date(Date.now() - 86400000),
        read: true
      }
    ])
    
    // 计算属性
    const isLoginPage = computed(() => route.path === '/login')
    
    const activeRoute = computed(() => route.path)
    
    const isAdmin = computed(() => userRole.value === 'admin')
    
    const notificationCount = computed(() => 
      notifications.value.filter(n => !n.read).length
    )
    
    const breadcrumbs = computed(() => {
      const breadcrumbMap = {
        '/dashboard': { title: '仪表盘', path: '/dashboard' },
        '/analytics': { title: '数据分析', path: '/analytics' },
        '/reports': { title: '报告管理', path: '/reports' },
        '/users': { title: '用户管理', path: '/users' },
        '/settings': { title: '系统设置', path: '/settings' }
      }
      
      const current = breadcrumbMap[route.path]
      return current ? [current] : []
    })
    
    // 方法
    const toggleSidebar = () => {
      sidebarCollapsed.value = !sidebarCollapsed.value
      localStorage.setItem('sidebarCollapsed', sidebarCollapsed.value.toString())
    }
    
    const handleUserCommand = (command) => {
      switch (command) {
        case 'profile':
          // 跳转到个人资料页面
          ElMessage.info('个人资料功能开发中...')
          break
        case 'settings':
          router.push('/settings')
          break
        case 'logout':
          handleLogout()
          break
      }
    }
    
    const handleLogout = () => {
      localStorage.removeItem('token')
      localStorage.removeItem('userName')
      localStorage.removeItem('userRole')
      ElMessage.success('退出登录成功')
      router.push('/login')
    }
    
    const formatTime = (time) => {
      const now = new Date()
      const diff = now - new Date(time)
      const minutes = Math.floor(diff / 60000)
      const hours = Math.floor(diff / 3600000)
      const days = Math.floor(diff / 86400000)
      
      if (minutes < 1) return '刚刚'
      if (minutes < 60) return `${minutes}分钟前`
      if (hours < 24) return `${hours}小时前`
      return `${days}天前`
    }
    
    // 监听路由变化
    watch(route, (newRoute) => {
      // 更新页面标题
      if (newRoute.meta?.title) {
        document.title = `${newRoute.meta.title} - 业务分析报告系统`
      }
    })
    
    // 组件挂载时
    onMounted(() => {
      // 从localStorage恢复侧边栏状态
      const saved = localStorage.getItem('sidebarCollapsed')
      if (saved !== null) {
        sidebarCollapsed.value = saved === 'true'
      }
      
      // 检查登录状态
      const token = localStorage.getItem('token')
      if (!token && route.path !== '/login') {
        router.push('/login')
      }
    })
    
    return {
      sidebarCollapsed,
      showNotifications,
      userName,
      userRole,
      userAvatar,
      notifications,
      isLoginPage,
      activeRoute,
      isAdmin,
      notificationCount,
      breadcrumbs,
      toggleSidebar,
      handleUserCommand,
      handleLogout,
      formatTime
    }
  }
}
</script>

<style>
#app {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  height: 100vh;
  margin: 0;
  padding: 0;
}

.app-container {
  height: 100vh;
}

.app-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-bottom: 1px solid #e4e7ed;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  height: 60px !important;
  line-height: 60px;
  padding: 0 20px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo {
  width: 32px;
  height: 32px;
  font-size: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.system-title {
  color: white;
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.notification-badge {
  .el-button {
    color: white;
    border-color: rgba(255, 255, 255, 0.3);
  }
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.1);
  cursor: pointer;
  transition: background 0.3s;
  color: white;
}

.user-info:hover {
  background: rgba(255, 255, 255, 0.2);
}

.user-name {
  font-size: 14px;
  font-weight: 500;
}

.app-sidebar {
  background: #fff;
  border-right: 1px solid #e4e7ed;
  transition: width 0.3s;
  box-shadow: 2px 0 4px rgba(0, 0, 0, 0.1);
}

.sidebar-content {
  height: 100%;
  position: relative;
}

.sidebar-toggle {
  padding: 16px;
  text-align: center;
  border-bottom: 1px solid #e4e7ed;
}

.sidebar-menu {
  border: none;
  height: calc(100% - 64px);
}

.sidebar-menu .el-menu-item {
  height: 50px;
  line-height: 50px;
  color: #606266;
  transition: all 0.3s;
}

.sidebar-menu .el-menu-item:hover,
.sidebar-menu .el-menu-item.is-active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.app-main {
  background: #f5f7fa;
  padding: 0;
  overflow: auto;
}

.main-content {
  padding: 20px;
  min-height: calc(100vh - 60px);
}

.breadcrumb {
  margin-bottom: 20px;
  padding: 16px 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.route-content {
  min-height: calc(100vh - 160px);
}

/* 过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 通知样式 */
.notifications-content {
  padding: 16px;
}

.notification-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 12px;
  transition: background 0.3s;
}

.notification-item.unread {
  background: #f0f9ff;
  border-left: 3px solid #409eff;
}

.notification-item:hover {
  background: #f5f7fa;
}

.notification-icon {
  font-size: 18px;
  margin-top: 2px;
}

.notification-icon.success {
  color: #67c23a;
}

.notification-icon.info {
  color: #409eff;
}

.notification-icon.warning {
  color: #e6a23c;
}

.notification-icon.error {
  color: #f56c6c;
}

.notification-content {
  flex: 1;
}

.notification-title {
  font-weight: 600;
  color: #303133;
  margin-bottom: 4px;
}

.notification-message {
  color: #606266;
  font-size: 14px;
  margin-bottom: 4px;
}

.notification-time {
  color: #909399;
  font-size: 12px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .app-sidebar {
    position: absolute;
    z-index: 1000;
    height: 100%;
  }
  
  .header-content {
    padding: 0 16px;
  }
  
  .system-title {
    display: none;
  }
  
  .main-content {
    padding: 16px;
  }
}
</style> 