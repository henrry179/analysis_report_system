/**
 * API调用工具 - 业务分析报告自动化系统
 * 提供统一的API调用接口和错误处理
 */

(function(app) {
    'use strict';

    // API配置
    const API_CONFIG = {
        baseURL: app.config.apiBaseUrl,
        timeout: 30000,
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    };

    // HTTP状态码映射
    const HTTP_STATUS = {
        200: 'OK',
        201: 'Created',
        400: 'Bad Request',
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Not Found',
        422: 'Unprocessable Entity',
        500: 'Internal Server Error',
        502: 'Bad Gateway',
        503: 'Service Unavailable'
    };

    /**
     * API客户端类
     */
    class ApiClient {
        constructor(config = {}) {
            this.config = { ...API_CONFIG, ...config };
            this.interceptors = {
                request: [],
                response: []
            };
            
            // 添加默认拦截器
            this.addRequestInterceptor(this.defaultRequestInterceptor.bind(this));
            this.addResponseInterceptor(this.defaultResponseInterceptor.bind(this));
        }

        /**
         * 添加请求拦截器
         * @param {Function} interceptor 拦截器函数
         */
        addRequestInterceptor(interceptor) {
            this.interceptors.request.push(interceptor);
        }

        /**
         * 添加响应拦截器
         * @param {Function} interceptor 拦截器函数
         */
        addResponseInterceptor(interceptor) {
            this.interceptors.response.push(interceptor);
        }

        /**
         * 默认请求拦截器
         * @param {Object} config 请求配置
         * @returns {Object} 处理后的配置
         */
        defaultRequestInterceptor(config) {
            // 添加认证token
            const token = app.storage.get('auth_token');
            if (token) {
                config.headers = config.headers || {};
                config.headers['Authorization'] = `Bearer ${token}`;
            }

            // 添加CSRF token
            const csrfToken = document.querySelector('meta[name="csrf-token"]');
            if (csrfToken) {
                config.headers = config.headers || {};
                config.headers['X-CSRF-Token'] = csrfToken.getAttribute('content');
            }

            return config;
        }

        /**
         * 默认响应拦截器
         * @param {Response} response 响应对象
         * @returns {Promise} 处理后的响应
         */
        async defaultResponseInterceptor(response) {
            // 处理401未授权错误
            if (response.status === 401) {
                app.storage.remove('auth_token');
                app.storage.remove('user_info');
                app.events.emit('auth:unauthorized');
                
                // 重定向到登录页面
                if (window.location.pathname !== '/login') {
                    window.location.href = '/login';
                }
            }

            return response;
        }

        /**
         * 执行HTTP请求
         * @param {string} url 请求URL
         * @param {Object} options 请求选项
         * @returns {Promise} 请求结果
         */
        async request(url, options = {}) {
            // 构建完整URL
            const fullUrl = url.startsWith('http') ? url : `${this.config.baseURL}${url}`;
            
            // 合并配置
            let config = {
                method: 'GET',
                headers: { ...this.config.headers },
                ...options
            };

            // 应用请求拦截器
            for (const interceptor of this.interceptors.request) {
                config = await interceptor(config);
            }

            try {
                // 显示加载状态
                app.loading.show('请求中...');

                // 设置超时
                const controller = new AbortController();
                const timeoutId = setTimeout(() => controller.abort(), this.config.timeout);
                config.signal = controller.signal;

                // 发送请求
                let response = await fetch(fullUrl, config);
                clearTimeout(timeoutId);

                // 应用响应拦截器
                for (const interceptor of this.interceptors.response) {
                    response = await interceptor(response);
                }

                // 处理响应
                const result = await this.handleResponse(response);
                
                return result;

            } catch (error) {
                console.error('API请求错误:', error);
                
                if (error.name === 'AbortError') {
                    throw new Error('请求超时');
                }
                
                throw error;
            } finally {
                app.loading.hide();
            }
        }

        /**
         * 处理响应
         * @param {Response} response 响应对象
         * @returns {Promise} 处理结果
         */
        async handleResponse(response) {
            const contentType = response.headers.get('content-type');
            
            let data;
            if (contentType && contentType.includes('application/json')) {
                data = await response.json();
            } else {
                data = await response.text();
            }

            if (!response.ok) {
                const error = new Error(data.message || HTTP_STATUS[response.status] || '请求失败');
                error.status = response.status;
                error.data = data;
                throw error;
            }

            return {
                data,
                status: response.status,
                headers: response.headers,
                ok: response.ok
            };
        }

        // HTTP方法快捷方式
        get(url, params = {}, options = {}) {
            const queryString = new URLSearchParams(params).toString();
            const fullUrl = queryString ? `${url}?${queryString}` : url;
            
            return this.request(fullUrl, {
                method: 'GET',
                ...options
            });
        }

        post(url, data = {}, options = {}) {
            return this.request(url, {
                method: 'POST',
                body: JSON.stringify(data),
                ...options
            });
        }

        put(url, data = {}, options = {}) {
            return this.request(url, {
                method: 'PUT',
                body: JSON.stringify(data),
                ...options
            });
        }

        patch(url, data = {}, options = {}) {
            return this.request(url, {
                method: 'PATCH',
                body: JSON.stringify(data),
                ...options
            });
        }

        delete(url, options = {}) {
            return this.request(url, {
                method: 'DELETE',
                ...options
            });
        }

        /**
         * 上传文件
         * @param {string} url 上传URL
         * @param {FormData|File} data 文件数据
         * @param {Object} options 选项
         * @returns {Promise} 上传结果
         */
        upload(url, data, options = {}) {
            let formData;
            
            if (data instanceof FormData) {
                formData = data;
            } else if (data instanceof File) {
                formData = new FormData();
                formData.append('file', data);
            } else {
                throw new Error('不支持的文件数据类型');
            }

            return this.request(url, {
                method: 'POST',
                body: formData,
                headers: {
                    // 不设置Content-Type，让浏览器自动设置boundary
                },
                ...options
            });
        }

        /**
         * 下载文件
         * @param {string} url 下载URL
         * @param {string} filename 文件名
         * @param {Object} options 选项
         */
        async download(url, filename, options = {}) {
            try {
                const response = await this.request(url, {
                    ...options,
                    headers: {
                        ...options.headers,
                        'Accept': '*/*'
                    }
                });

                // 创建blob对象
                const blob = new Blob([response.data]);
                
                // 创建下载链接
                const downloadUrl = window.URL.createObjectURL(blob);
                const link = document.createElement('a');
                link.href = downloadUrl;
                link.download = filename || 'download';
                
                // 触发下载
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                
                // 清理URL对象
                window.URL.revokeObjectURL(downloadUrl);
                
                app.notify.success('文件下载完成');
                
            } catch (error) {
                console.error('文件下载失败:', error);
                app.notify.error('文件下载失败: ' + error.message);
                throw error;
            }
        }
    }

    // 创建默认API客户端实例
    const apiClient = new ApiClient();

    // API接口定义
    app.api = {
        client: apiClient,

        // 系统信息
        system: {
            info: () => apiClient.get('/info'),
            health: () => apiClient.get('/health'),
            metrics: () => apiClient.get('/metrics')
        },

        // 用户认证
        auth: {
            login: (credentials) => apiClient.post('/auth/login', credentials),
            logout: () => apiClient.post('/auth/logout'),
            refresh: () => apiClient.post('/auth/refresh'),
            profile: () => apiClient.get('/auth/profile'),
            updateProfile: (data) => apiClient.put('/auth/profile', data)
        },

        // 用户管理
        users: {
            list: (params = {}) => apiClient.get('/users', params),
            get: (id) => apiClient.get(`/users/${id}`),
            create: (data) => apiClient.post('/users', data),
            update: (id, data) => apiClient.put(`/users/${id}`, data),
            delete: (id) => apiClient.delete(`/users/${id}`)
        },

        // 报告管理
        reports: {
            list: (params = {}) => apiClient.get('/reports', params),
            get: (id) => apiClient.get(`/reports/${id}`),
            create: (data) => apiClient.post('/reports', data),
            update: (id, data) => apiClient.put(`/reports/${id}`, data),
            delete: (id) => apiClient.delete(`/reports/${id}`),
            generate: (data) => apiClient.post('/reports/generate', data),
            download: (id, format = 'pdf') => apiClient.download(`/reports/${id}/download?format=${format}`, `report_${id}.${format}`)
        },

        // 数据管理
        data: {
            upload: (file) => apiClient.upload('/data/upload', file),
            import: (data) => apiClient.post('/data/import', data),
            export: (params) => apiClient.get('/data/export', params),
            process: (data) => apiClient.post('/data/process', data),
            validate: (data) => apiClient.post('/data/validate', data)
        },

        // 分析功能
        analytics: {
            analyze: (data) => apiClient.post('/analytics/analyze', data),
            correlations: (data) => apiClient.post('/analytics/correlations', data),
            trends: (data) => apiClient.post('/analytics/trends', data),
            predictions: (data) => apiClient.post('/analytics/predictions', data)
        },

        // 图表生成
        charts: {
            generate: (data) => apiClient.post('/charts/generate', data),
            types: () => apiClient.get('/charts/types'),
            preview: (data) => apiClient.post('/charts/preview', data)
        },

        // 文件管理
        files: {
            list: (params = {}) => apiClient.get('/files', params),
            upload: (file, path = '') => {
                const formData = new FormData();
                formData.append('file', file);
                formData.append('path', path);
                return apiClient.upload('/files/upload', formData);
            },
            download: (id, filename) => apiClient.download(`/files/${id}/download`, filename),
            delete: (id) => apiClient.delete(`/files/${id}`)
        },

        // 系统设置
        settings: {
            get: () => apiClient.get('/settings'),
            update: (data) => apiClient.put('/settings', data),
            reset: () => apiClient.post('/settings/reset')
        },

        // 通知管理
        notifications: {
            list: (params = {}) => apiClient.get('/notifications', params),
            markRead: (id) => apiClient.put(`/notifications/${id}/read`),
            markAllRead: () => apiClient.put('/notifications/read-all'),
            delete: (id) => apiClient.delete(`/notifications/${id}`)
        }
    };

    // 错误处理包装器
    app.api.withErrorHandling = function(apiCall, options = {}) {
        return async (...args) => {
            try {
                const result = await apiCall(...args);
                
                if (options.successMessage) {
                    app.notify.success(options.successMessage);
                }
                
                return result;
            } catch (error) {
                console.error('API调用错误:', error);
                
                const errorMessage = options.errorMessage || error.message || 'API调用失败';
                app.notify.error(errorMessage);
                
                if (options.throwError !== false) {
                    throw error;
                }
                
                return null;
            }
        };
    };

    // 批量API调用
    app.api.batch = async function(calls) {
        try {
            app.loading.show('批量处理中...');
            
            const results = await Promise.allSettled(calls);
            
            const succeeded = results.filter(r => r.status === 'fulfilled').length;
            const failed = results.filter(r => r.status === 'rejected').length;
            
            if (failed > 0) {
                app.notify.warning(`批量操作完成: ${succeeded} 成功, ${failed} 失败`);
            } else {
                app.notify.success(`批量操作完成: ${succeeded} 个操作成功`);
            }
            
            return results;
        } catch (error) {
            console.error('批量API调用错误:', error);
            app.notify.error('批量操作失败: ' + error.message);
            throw error;
        } finally {
            app.loading.hide();
        }
    };

})(window.AnalysisApp);