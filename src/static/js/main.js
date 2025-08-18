/**
 * 主JavaScript文件 - 业务分析报告自动化系统
 * 提供通用工具函数和基础功能
 */

// 全局应用对象
window.AnalysisApp = window.AnalysisApp || {};

(function(app) {
    'use strict';

    // 应用配置
    app.config = {
        apiBaseUrl: '/api',
        wsUrl: `${window.location.protocol === 'https:' ? 'wss:' : 'ws:'}//${window.location.host}/ws`,
        version: '4.0',
        debug: false
    };

    // 工具函数
    app.utils = {
        /**
         * 格式化日期
         * @param {Date|string} date 日期对象或字符串
         * @param {string} format 格式化模式
         * @returns {string} 格式化后的日期字符串
         */
        formatDate: function(date, format = 'YYYY-MM-DD HH:mm:ss') {
            if (!date) return '';
            
            const d = new Date(date);
            if (isNaN(d.getTime())) return '';
            
            const year = d.getFullYear();
            const month = String(d.getMonth() + 1).padStart(2, '0');
            const day = String(d.getDate()).padStart(2, '0');
            const hours = String(d.getHours()).padStart(2, '0');
            const minutes = String(d.getMinutes()).padStart(2, '0');
            const seconds = String(d.getSeconds()).padStart(2, '0');
            
            return format
                .replace('YYYY', year)
                .replace('MM', month)
                .replace('DD', day)
                .replace('HH', hours)
                .replace('mm', minutes)
                .replace('ss', seconds);
        },

        /**
         * 格式化文件大小
         * @param {number} bytes 字节数
         * @returns {string} 格式化后的文件大小
         */
        formatFileSize: function(bytes) {
            if (bytes === 0) return '0 B';
            
            const k = 1024;
            const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            
            return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
        },

        /**
         * 格式化数字
         * @param {number} num 数字
         * @param {number} decimals 小数位数
         * @returns {string} 格式化后的数字
         */
        formatNumber: function(num, decimals = 2) {
            if (isNaN(num)) return '0';
            return Number(num).toLocaleString('zh-CN', {
                minimumFractionDigits: decimals,
                maximumFractionDigits: decimals
            });
        },

        /**
         * 防抖函数
         * @param {Function} func 要防抖的函数
         * @param {number} wait 等待时间（毫秒）
         * @returns {Function} 防抖后的函数
         */
        debounce: function(func, wait) {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        },

        /**
         * 节流函数
         * @param {Function} func 要节流的函数
         * @param {number} limit 时间间隔（毫秒）
         * @returns {Function} 节流后的函数
         */
        throttle: function(func, limit) {
            let inThrottle;
            return function(...args) {
                if (!inThrottle) {
                    func.apply(this, args);
                    inThrottle = true;
                    setTimeout(() => inThrottle = false, limit);
                }
            };
        },

        /**
         * 深拷贝对象
         * @param {any} obj 要拷贝的对象
         * @returns {any} 拷贝后的对象
         */
        deepClone: function(obj) {
            if (obj === null || typeof obj !== 'object') return obj;
            if (obj instanceof Date) return new Date(obj.getTime());
            if (obj instanceof Array) return obj.map(item => this.deepClone(item));
            if (typeof obj === 'object') {
                const clonedObj = {};
                for (const key in obj) {
                    if (obj.hasOwnProperty(key)) {
                        clonedObj[key] = this.deepClone(obj[key]);
                    }
                }
                return clonedObj;
            }
        },

        /**
         * 生成UUID
         * @returns {string} UUID字符串
         */
        generateUUID: function() {
            return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
                const r = Math.random() * 16 | 0;
                const v = c === 'x' ? r : (r & 0x3 | 0x8);
                return v.toString(16);
            });
        },

        /**
         * 获取URL参数
         * @param {string} name 参数名
         * @returns {string|null} 参数值
         */
        getUrlParameter: function(name) {
            const urlParams = new URLSearchParams(window.location.search);
            return urlParams.get(name);
        },

        /**
         * 设置URL参数
         * @param {string} name 参数名
         * @param {string} value 参数值
         */
        setUrlParameter: function(name, value) {
            const url = new URL(window.location);
            url.searchParams.set(name, value);
            window.history.pushState({}, '', url);
        }
    };

    // 存储管理
    app.storage = {
        /**
         * 设置本地存储
         * @param {string} key 键名
         * @param {any} value 值
         */
        set: function(key, value) {
            try {
                localStorage.setItem(key, JSON.stringify(value));
            } catch (e) {
                console.warn('无法设置本地存储:', e);
            }
        },

        /**
         * 获取本地存储
         * @param {string} key 键名
         * @param {any} defaultValue 默认值
         * @returns {any} 存储的值
         */
        get: function(key, defaultValue = null) {
            try {
                const item = localStorage.getItem(key);
                return item ? JSON.parse(item) : defaultValue;
            } catch (e) {
                console.warn('无法获取本地存储:', e);
                return defaultValue;
            }
        },

        /**
         * 删除本地存储
         * @param {string} key 键名
         */
        remove: function(key) {
            try {
                localStorage.removeItem(key);
            } catch (e) {
                console.warn('无法删除本地存储:', e);
            }
        },

        /**
         * 清空本地存储
         */
        clear: function() {
            try {
                localStorage.clear();
            } catch (e) {
                console.warn('无法清空本地存储:', e);
            }
        }
    };

    // 事件管理
    app.events = {
        listeners: {},

        /**
         * 添加事件监听器
         * @param {string} event 事件名
         * @param {Function} callback 回调函数
         */
        on: function(event, callback) {
            if (!this.listeners[event]) {
                this.listeners[event] = [];
            }
            this.listeners[event].push(callback);
        },

        /**
         * 移除事件监听器
         * @param {string} event 事件名
         * @param {Function} callback 回调函数
         */
        off: function(event, callback) {
            if (!this.listeners[event]) return;
            
            const index = this.listeners[event].indexOf(callback);
            if (index > -1) {
                this.listeners[event].splice(index, 1);
            }
        },

        /**
         * 触发事件
         * @param {string} event 事件名
         * @param {any} data 事件数据
         */
        emit: function(event, data) {
            if (!this.listeners[event]) return;
            
            this.listeners[event].forEach(callback => {
                try {
                    callback(data);
                } catch (e) {
                    console.error('事件回调执行错误:', e);
                }
            });
        }
    };

    // 通知系统
    app.notify = {
        /**
         * 显示通知
         * @param {string} message 消息内容
         * @param {string} type 通知类型 (success, warning, error, info)
         * @param {number} duration 显示时长（毫秒）
         */
        show: function(message, type = 'info', duration = 3000) {
            const notification = document.createElement('div');
            notification.className = `alert alert-${type} notification`;
            notification.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 9999;
                min-width: 300px;
                max-width: 500px;
                opacity: 0;
                transform: translateX(100%);
                transition: all 0.3s ease;
            `;
            notification.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span>${message}</span>
                    <button type="button" class="btn-close" style="background: none; border: none; font-size: 1.2rem; cursor: pointer;">&times;</button>
                </div>
            `;

            document.body.appendChild(notification);

            // 显示动画
            setTimeout(() => {
                notification.style.opacity = '1';
                notification.style.transform = 'translateX(0)';
            }, 10);

            // 关闭按钮事件
            const closeBtn = notification.querySelector('.btn-close');
            closeBtn.addEventListener('click', () => {
                this.hide(notification);
            });

            // 自动关闭
            if (duration > 0) {
                setTimeout(() => {
                    this.hide(notification);
                }, duration);
            }

            return notification;
        },

        /**
         * 隐藏通知
         * @param {Element} notification 通知元素
         */
        hide: function(notification) {
            notification.style.opacity = '0';
            notification.style.transform = 'translateX(100%)';
            
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        },

        success: function(message, duration = 3000) {
            return this.show(message, 'success', duration);
        },

        warning: function(message, duration = 3000) {
            return this.show(message, 'warning', duration);
        },

        error: function(message, duration = 5000) {
            return this.show(message, 'error', duration);
        },

        info: function(message, duration = 3000) {
            return this.show(message, 'info', duration);
        }
    };

    // 加载管理
    app.loading = {
        count: 0,

        /**
         * 显示加载状态
         * @param {string} message 加载消息
         */
        show: function(message = '加载中...') {
            this.count++;
            
            let loader = document.getElementById('global-loader');
            if (!loader) {
                loader = document.createElement('div');
                loader.id = 'global-loader';
                loader.innerHTML = `
                    <div style="
                        position: fixed;
                        top: 0;
                        left: 0;
                        width: 100%;
                        height: 100%;
                        background: rgba(0, 0, 0, 0.5);
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        z-index: 9999;
                    ">
                        <div style="
                            background: white;
                            padding: 2rem;
                            border-radius: 0.5rem;
                            text-align: center;
                            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
                        ">
                            <div class="spinner" style="margin-bottom: 1rem;"></div>
                            <div id="loading-message">${message}</div>
                        </div>
                    </div>
                `;
                document.body.appendChild(loader);
            } else {
                document.getElementById('loading-message').textContent = message;
                loader.style.display = 'block';
            }
        },

        /**
         * 隐藏加载状态
         */
        hide: function() {
            this.count = Math.max(0, this.count - 1);
            
            if (this.count === 0) {
                const loader = document.getElementById('global-loader');
                if (loader) {
                    loader.style.display = 'none';
                }
            }
        }
    };

    // 初始化函数
    app.init = function() {
        console.log('业务分析报告自动化系统 v' + this.config.version + ' 已加载');
        
        // 设置全局错误处理
        window.addEventListener('error', function(e) {
            console.error('全局错误:', e.error);
            if (app.config.debug) {
                app.notify.error('系统错误: ' + e.message);
            }
        });

        // 设置未处理的Promise拒绝处理
        window.addEventListener('unhandledrejection', function(e) {
            console.error('未处理的Promise拒绝:', e.reason);
            if (app.config.debug) {
                app.notify.error('异步操作错误: ' + e.reason);
            }
        });

        // 触发初始化完成事件
        this.events.emit('app:initialized');
    };

    // DOM加载完成后初始化
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            app.init();
        });
    } else {
        app.init();
    }

})(window.AnalysisApp);

// 导出到全局作用域
window.utils = window.AnalysisApp.utils;
window.storage = window.AnalysisApp.storage;
window.notify = window.AnalysisApp.notify;
window.loading = window.AnalysisApp.loading;