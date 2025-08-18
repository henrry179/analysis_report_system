/**
 * 移动端主要JavaScript文件
 * 处理导航、页面切换、手势等移动端特有功能
 */

class MobileApp {
    constructor() {
        this.currentPage = 'dashboardPage';
        this.menuOpen = false;
        this.touchStartX = 0;
        this.touchStartY = 0;
        this.isRefreshing = false;
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.setupGestures();
        this.setupPullToRefresh();
        this.loadInitialData();
        
        // 防止页面缩放
        this.preventZoom();
        
        // 设置视口高度
        this.setViewportHeight();
    }
    
    setupEventListeners() {
        // 菜单按钮
        document.getElementById('menuBtn').addEventListener('click', () => {
            this.toggleMenu();
        });
        
        // 菜单覆盖层
        document.getElementById('menuOverlay').addEventListener('click', () => {
            this.closeMenu();
        });
        
        // 底部导航
        document.querySelectorAll('.tab-item').forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                const pageId = item.getAttribute('data-page');
                this.switchPage(pageId);
                this.setActiveTab(item);
            });
        });
        
        // 侧边菜单项
        document.querySelectorAll('.menu-item').forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                const href = item.getAttribute('href');
                const pageId = href.substring(1) + 'Page';
                this.switchPage(pageId);
                this.setActiveMenuItem(item);
                this.closeMenu();
                
                // 更新底部导航
                const tabItem = document.querySelector(`[data-page="${pageId}"]`);
                if (tabItem) {
                    this.setActiveTab(tabItem);
                }
            });
        });
        
        // 通知按钮
        document.getElementById('notificationBtn').addEventListener('click', () => {
            this.showNotifications();
        });
        
        // 退出登录
        document.getElementById('logoutBtn').addEventListener('click', () => {
            this.logout();
        });
        
        // 窗口大小变化
        window.addEventListener('resize', () => {
            this.setViewportHeight();
        });
        
        // 页面可见性变化
        document.addEventListener('visibilitychange', () => {
            if (!document.hidden) {
                this.refreshData();
            }
        });
    }
    
    setupGestures() {
        // 滑动手势
        document.addEventListener('touchstart', (e) => {
            this.touchStartX = e.touches[0].clientX;
            this.touchStartY = e.touches[0].clientY;
        }, { passive: true });
        
        document.addEventListener('touchmove', (e) => {
            if (this.menuOpen) return;
            
            const touchX = e.touches[0].clientX;
            const touchY = e.touches[0].clientY;
            const diffX = touchX - this.touchStartX;
            const diffY = touchY - this.touchStartY;
            
            // 水平滑动距离大于垂直滑动距离
            if (Math.abs(diffX) > Math.abs(diffY) && Math.abs(diffX) > 50) {
                // 从左边缘滑动打开菜单
                if (this.touchStartX < 20 && diffX > 100) {
                    this.openMenu();
                }
            }
        }, { passive: true });
        
        document.addEventListener('touchend', () => {
            // 重置触摸坐标
            this.touchStartX = 0;
            this.touchStartY = 0;
        }, { passive: true });
    }
    
    setupPullToRefresh() {
        let startY = 0;
        let currentY = 0;
        let pulling = false;
        
        const main = document.querySelector('main');
        
        main.addEventListener('touchstart', (e) => {
            if (main.scrollTop === 0) {
                startY = e.touches[0].clientY;
                pulling = false;
            }
        }, { passive: true });
        
        main.addEventListener('touchmove', (e) => {
            if (main.scrollTop > 0) return;
            
            currentY = e.touches[0].clientY;
            const diff = currentY - startY;
            
            if (diff > 0 && diff < 150) {
                pulling = true;
                // 可以添加视觉反馈
            }
        }, { passive: true });
        
        main.addEventListener('touchend', () => {
            if (pulling && currentY - startY > 100) {
                this.refreshData();
            }
            pulling = false;
        }, { passive: true });
    }
    
    preventZoom() {
        // 防止双击缩放
        let lastTouchEnd = 0;
        document.addEventListener('touchend', (e) => {
            const now = (new Date()).getTime();
            if (now - lastTouchEnd <= 300) {
                e.preventDefault();
            }
            lastTouchEnd = now;
        }, false);
        
        // 防止捏合缩放
        document.addEventListener('gesturestart', (e) => {
            e.preventDefault();
        });
        
        document.addEventListener('gesturechange', (e) => {
            e.preventDefault();
        });
        
        document.addEventListener('gestureend', (e) => {
            e.preventDefault();
        });
    }
    
    setViewportHeight() {
        // 设置CSS自定义属性用于100vh的替代方案
        const vh = window.innerHeight * 0.01;
        document.documentElement.style.setProperty('--vh', `${vh}px`);
    }
    
    toggleMenu() {
        if (this.menuOpen) {
            this.closeMenu();
        } else {
            this.openMenu();
        }
    }
    
    openMenu() {
        const menu = document.getElementById('sideMenu');
        menu.classList.remove('-translate-x-full');
        menu.classList.add('translate-x-0');
        this.menuOpen = true;
        
        // 防止背景滚动
        document.body.style.overflow = 'hidden';
    }
    
    closeMenu() {
        const menu = document.getElementById('sideMenu');
        menu.classList.remove('translate-x-0');
        menu.classList.add('-translate-x-full');
        this.menuOpen = false;
        
        // 恢复背景滚动
        document.body.style.overflow = '';
    }
    
    switchPage(pageId) {
        // 隐藏当前页面
        document.querySelectorAll('.page').forEach(page => {
            page.classList.remove('active');
            page.classList.add('hidden');
        });
        
        // 显示目标页面
        const targetPage = document.getElementById(pageId);
        if (targetPage) {
            targetPage.classList.remove('hidden');
            targetPage.classList.add('active');
            this.currentPage = pageId;
            
            // 滚动到顶部
            targetPage.scrollTop = 0;
            
            // 加载页面数据
            this.loadPageData(pageId);
        }
    }
    
    setActiveTab(activeTab) {
        document.querySelectorAll('.tab-item').forEach(tab => {
            tab.classList.remove('active');
        });
        activeTab.classList.add('active');
    }
    
    setActiveMenuItem(activeItem) {
        document.querySelectorAll('.menu-item').forEach(item => {
            item.classList.remove('active');
        });
        activeItem.classList.add('active');
    }
    
    showLoading() {
        document.getElementById('loadingIndicator').classList.remove('hidden');
    }
    
    hideLoading() {
        document.getElementById('loadingIndicator').classList.add('hidden');
    }
    
    showToast(message, type = 'success') {
        const toast = document.getElementById('toast');
        const toastMessage = document.getElementById('toastMessage');
        
        toastMessage.textContent = message;
        
        // 设置样式
        toast.className = `fixed top-20 left-4 right-4 p-4 rounded-lg shadow-lg transform transition-transform duration-300 z-50`;
        
        switch (type) {
            case 'success':
                toast.classList.add('bg-green-500', 'text-white');
                break;
            case 'error':
                toast.classList.add('bg-red-500', 'text-white');
                break;
            case 'warning':
                toast.classList.add('bg-yellow-500', 'text-white');
                break;
            case 'info':
                toast.classList.add('bg-blue-500', 'text-white');
                break;
        }
        
        // 显示
        toast.classList.remove('-translate-y-full');
        toast.classList.add('translate-y-0');
        
        // 自动隐藏
        setTimeout(() => {
            this.hideToast();
        }, 3000);
    }
    
    hideToast() {
        const toast = document.getElementById('toast');
        toast.classList.remove('translate-y-0');
        toast.classList.add('-translate-y-full');
    }
    
    loadInitialData() {
        this.showLoading();
        
        // 模拟加载数据
        setTimeout(() => {
            this.updateDashboardStats();
            this.loadRecentActivities();
            this.updateSystemStatus();
            this.hideLoading();
        }, 1000);
    }
    
    loadPageData(pageId) {
        switch (pageId) {
            case 'dashboardPage':
                this.updateDashboardStats();
                break;
            case 'reportsPage':
                this.loadReports();
                break;
            case 'analyticsPage':
                this.loadAnalytics();
                break;
            case 'chartsPage':
                this.loadCharts();
                break;
            case 'dataPage':
                this.loadData();
                break;
        }
    }
    
    updateDashboardStats() {
        // 模拟数据
        const stats = {
            totalReports: Math.floor(Math.random() * 100) + 50,
            onlineUsers: Math.floor(Math.random() * 20) + 5,
            systemStatus: '正常',
            dataCount: Math.floor(Math.random() * 1000) + 500
        };
        
        document.getElementById('totalReports').textContent = stats.totalReports;
        document.getElementById('onlineUsers').textContent = stats.onlineUsers;
        document.getElementById('systemStatus').textContent = stats.systemStatus;
        document.getElementById('dataCount').textContent = stats.dataCount.toLocaleString();
    }
    
    loadRecentActivities() {
        const activities = [
            { time: '2分钟前', action: '生成了月度销售报告', user: '张三' },
            { time: '5分钟前', action: '上传了数据文件', user: '李四' },
            { time: '10分钟前', action: '查看了图表分析', user: '王五' },
            { time: '15分钟前', action: '导出了数据报表', user: '赵六' },
            { time: '20分钟前', action: '修改了系统设置', user: '管理员' }
        ];
        
        const container = document.getElementById('recentActivities');
        container.innerHTML = activities.map(activity => `
            <div class="p-4 hover:bg-gray-50">
                <div class="flex items-center justify-between">
                    <div class="flex-1">
                        <p class="text-sm font-medium text-gray-900">${activity.user} ${activity.action}</p>
                        <p class="text-xs text-gray-500">${activity.time}</p>
                    </div>
                    <i class="fas fa-chevron-right text-gray-400"></i>
                </div>
            </div>
        `).join('');
    }
    
    updateSystemStatus() {
        // 模拟系统状态
        const cpu = Math.floor(Math.random() * 30) + 20;
        const memory = Math.floor(Math.random() * 40) + 30;
        const disk = Math.floor(Math.random() * 20) + 40;
        
        document.getElementById('cpuUsage').style.width = cpu + '%';
        document.getElementById('cpuText').textContent = cpu + '%';
        
        document.getElementById('memoryUsage').style.width = memory + '%';
        document.getElementById('memoryText').textContent = memory + '%';
        
        document.getElementById('diskUsage').style.width = disk + '%';
        document.getElementById('diskText').textContent = disk + '%';
    }
    
    loadReports() {
        const reports = [
            {
                id: 1,
                title: '月度销售报告',
                type: 'PDF',
                date: '2025-08-18',
                status: '已完成',
                size: '2.5MB'
            },
            {
                id: 2,
                title: '季度分析报告',
                type: 'HTML',
                date: '2025-08-17',
                status: '处理中',
                size: '1.8MB'
            },
            {
                id: 3,
                title: '年度总结报告',
                type: 'Excel',
                date: '2025-08-16',
                status: '已完成',
                size: '3.2MB'
            }
        ];
        
        const container = document.getElementById('reportsList');
        container.innerHTML = reports.map(report => `
            <div class="bg-white rounded-lg shadow p-4">
                <div class="flex items-center justify-between mb-2">
                    <h3 class="font-semibold text-gray-900">${report.title}</h3>
                    <span class="status-indicator ${report.status === '已完成' ? 'status-success' : 'status-warning'}">
                        ${report.status}
                    </span>
                </div>
                <div class="flex items-center justify-between text-sm text-gray-600">
                    <div class="flex items-center space-x-4">
                        <span><i class="fas fa-file-${report.type.toLowerCase()} mr-1"></i>${report.type}</span>
                        <span><i class="fas fa-calendar mr-1"></i>${report.date}</span>
                        <span><i class="fas fa-hdd mr-1"></i>${report.size}</span>
                    </div>
                    <div class="flex items-center space-x-2">
                        <button class="p-2 text-blue-600 hover:bg-blue-50 rounded" onclick="downloadReport(${report.id})">
                            <i class="fas fa-download"></i>
                        </button>
                        <button class="p-2 text-gray-600 hover:bg-gray-50 rounded" onclick="viewReport(${report.id})">
                            <i class="fas fa-eye"></i>
                        </button>
                        <button class="p-2 text-red-600 hover:bg-red-50 rounded" onclick="deleteReport(${report.id})">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
            </div>
        `).join('');
    }
    
    loadAnalytics() {
        // 分析页面数据加载
        console.log('Loading analytics data...');
    }
    
    loadCharts() {
        // 图表页面数据加载
        console.log('Loading charts data...');
    }
    
    loadData() {
        // 数据页面数据加载
        console.log('Loading data...');
    }
    
    refreshData() {
        if (this.isRefreshing) return;
        
        this.isRefreshing = true;
        this.showToast('正在刷新数据...', 'info');
        
        setTimeout(() => {
            this.loadPageData(this.currentPage);
            this.isRefreshing = false;
            this.showToast('数据刷新完成', 'success');
        }, 1500);
    }
    
    showNotifications() {
        const notifications = [
            { title: '系统更新', message: '系统将在今晚进行维护更新', time: '5分钟前' },
            { title: '报告完成', message: '月度销售报告已生成完成', time: '10分钟前' },
            { title: '数据同步', message: '数据同步已完成', time: '1小时前' }
        ];
        
        // 这里可以显示通知列表的模态框
        console.log('Showing notifications:', notifications);
        this.showToast('暂无新通知', 'info');
    }
    
    logout() {
        if (confirm('确定要退出登录吗？')) {
            this.showLoading();
            setTimeout(() => {
                window.location.href = '/login';
            }, 1000);
        }
    }
}

// 全局函数
function quickAction(action) {
    const app = window.mobileApp;
    
    switch (action) {
        case 'generate-report':
            app.showToast('开始生成报告...', 'info');
            break;
        case 'upload-data':
            app.showToast('打开文件上传...', 'info');
            break;
        case 'view-charts':
            app.switchPage('chartsPage');
            app.setActiveTab(document.querySelector('[data-page="chartsPage"]'));
            break;
        case 'export-data':
            app.showToast('开始导出数据...', 'info');
            break;
    }
}

function createNewReport() {
    window.mobileApp.showToast('打开报告创建页面...', 'info');
}

function filterReports() {
    window.mobileApp.showToast('应用筛选条件...', 'info');
}

function downloadReport(id) {
    window.mobileApp.showToast(`下载报告 ${id}...`, 'info');
}

function viewReport(id) {
    window.mobileApp.showToast(`查看报告 ${id}...`, 'info');
}

function deleteReport(id) {
    if (confirm('确定要删除这个报告吗？')) {
        window.mobileApp.showToast(`删除报告 ${id}`, 'success');
    }
}

function hideToast() {
    window.mobileApp.hideToast();
}

// 初始化应用
document.addEventListener('DOMContentLoaded', () => {
    window.mobileApp = new MobileApp();
});