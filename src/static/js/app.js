import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import axios from 'axios'
import * as echarts from 'echarts'

// 创建Vue应用
const app = createApp({
    data() {
        return {
            // 用户状态
            user: null,
            token: localStorage.getItem('token'),
            
            // 数据状态
            data: null,
            analysisResults: null,
            reports: [],
            
            // UI状态
            loading: false,
            activeTab: 'data',
            
            // 表单数据
            loginForm: {
                username: '',
                password: ''
            },
            uploadForm: {
                file: null
            },
            analysisForm: {
                type: 'descriptive',
                options: {}
            }
        }
    },
    
    methods: {
        // 用户认证
        async login() {
            try {
                this.loading = true
                const formData = new FormData()
                formData.append('username', this.loginForm.username)
                formData.append('password', this.loginForm.password)
                
                const response = await axios.post('/token', formData)
                this.token = response.data.access_token
                localStorage.setItem('token', this.token)
                
                // 获取用户信息
                await this.getUserInfo()
                
                this.$message.success('登录成功')
            } catch (error) {
                this.$message.error(error.response?.data?.detail || '登录失败')
            } finally {
                this.loading = false
            }
        },
        
        async logout() {
            this.token = null
            this.user = null
            localStorage.removeItem('token')
            this.$message.success('已退出登录')
        },
        
        async getUserInfo() {
            try {
                const response = await axios.get('/api/users/me', {
                    headers: { Authorization: `Bearer ${this.token}` }
                })
                this.user = response.data
            } catch (error) {
                this.$message.error('获取用户信息失败')
            }
        },
        
        // 数据处理
        async handleFileUpload() {
            try {
                this.loading = true
                const formData = new FormData()
                formData.append('file', this.uploadForm.file)
                
                const response = await axios.post('/api/data/import', formData, {
                    headers: {
                        Authorization: `Bearer ${this.token}`,
                        'Content-Type': 'multipart/form-data'
                    }
                })
                
                this.data = response.data.data
                this.$message.success('数据导入成功')
            } catch (error) {
                this.$message.error(error.response?.data?.detail || '数据导入失败')
            } finally {
                this.loading = false
            }
        },
        
        // 数据分析
        async runAnalysis() {
            try {
                this.loading = true
                const response = await axios.post('/api/analysis', {
                    analysis_type: this.analysisForm.type,
                    data: this.data,
                    options: this.analysisForm.options
                }, {
                    headers: { Authorization: `Bearer ${this.token}` }
                })
                
                this.analysisResults = response.data.results
                this.$message.success('分析完成')
            } catch (error) {
                this.$message.error(error.response?.data?.detail || '分析失败')
            } finally {
                this.loading = false
            }
        },
        
        // 报告生成
        async generateReport(type) {
            try {
                this.loading = true
                const response = await axios.post('/api/reports/generate', {
                    report_type: type,
                    data: type === 'visualization' ? this.data : this.analysisResults
                }, {
                    headers: { Authorization: `Bearer ${this.token}` }
                })
                
                this.reports.push({
                    type,
                    path: response.data.report_path,
                    created_at: new Date().toISOString()
                })
                
                this.$message.success('报告生成成功')
            } catch (error) {
                this.$message.error(error.response?.data?.detail || '报告生成失败')
            } finally {
                this.loading = false
            }
        },
        
        // 系统管理
        async createUser(userData) {
            try {
                this.loading = true
                await axios.post('/api/users', userData, {
                    headers: { Authorization: `Bearer ${this.token}` }
                })
                
                this.$message.success('用户创建成功')
            } catch (error) {
                this.$message.error(error.response?.data?.detail || '用户创建失败')
            } finally {
                this.loading = false
            }
        },
        
        async deleteUser(username) {
            try {
                this.loading = true
                await axios.delete(`/api/users/${username}`, {
                    headers: { Authorization: `Bearer ${this.token}` }
                })
                
                this.$message.success('用户删除成功')
            } catch (error) {
                this.$message.error(error.response?.data?.detail || '用户删除失败')
            } finally {
                this.loading = false
            }
        },
        
        async getSystemLogs() {
            try {
                this.loading = true
                const response = await axios.get('/api/logs', {
                    headers: { Authorization: `Bearer ${this.token}` }
                })
                
                return response.data.logs
            } catch (error) {
                this.$message.error(error.response?.data?.detail || '获取日志失败')
                return []
            } finally {
                this.loading = false
            }
        },
        
        async backupSystem() {
            try {
                this.loading = true
                const response = await axios.post('/api/system/backup', {}, {
                    headers: { Authorization: `Bearer ${this.token}` }
                })
                
                this.$message.success('系统备份成功')
                return response.data.backup_file
            } catch (error) {
                this.$message.error(error.response?.data?.detail || '系统备份失败')
                return null
            } finally {
                this.loading = false
            }
        },
        
        async restoreSystem(backupFile) {
            try {
                this.loading = true
                await axios.post('/api/system/restore', {
                    backup_file: backupFile
                }, {
                    headers: { Authorization: `Bearer ${this.token}` }
                })
                
                this.$message.success('系统恢复成功')
            } catch (error) {
                this.$message.error(error.response?.data?.detail || '系统恢复失败')
            } finally {
                this.loading = false
            }
        }
    },
    
    mounted() {
        // 如果有token，获取用户信息
        if (this.token) {
            this.getUserInfo()
        }
        
        // 配置axios
        axios.defaults.baseURL = 'http://localhost:8000'
        axios.interceptors.request.use(config => {
            if (this.token) {
                config.headers.Authorization = `Bearer ${this.token}`
            }
            return config
        })
    }
})

// 使用Element Plus
app.use(ElementPlus)

// 挂载应用
app.mount('#app') 