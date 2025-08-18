/**
 * Service Worker - 业务分析报告自动化系统
 * 提供离线功能、缓存管理和推送通知
 */

const CACHE_NAME = 'analysis-system-v4.0.0';
const STATIC_CACHE = 'static-v4.0.0';
const DYNAMIC_CACHE = 'dynamic-v4.0.0';
const API_CACHE = 'api-v4.0.0';

// 需要缓存的静态资源
const STATIC_ASSETS = [
    '/',
    '/mobile/',
    '/static/css/main.css',
    '/static/js/main.js',
    '/static/js/api.js',
    '/static/mobile/css/mobile.css',
    '/static/mobile/js/mobile.js',
    '/static/mobile/manifest.json',
    '/static/mobile/icons/icon-192x192.png',
    '/static/mobile/icons/icon-512x512.png'
];

// 需要缓存的API路径
const CACHEABLE_API_PATHS = [
    '/api/info',
    '/api/reports',
    '/api/charts/types',
    '/api/settings'
];

// 网络优先的资源
const NETWORK_FIRST_PATHS = [
    '/api/auth/',
    '/api/notifications',
    '/api/data/upload'
];

// 安装事件 - 缓存静态资源
self.addEventListener('install', event => {
    console.log('Service Worker: Installing...');
    
    event.waitUntil(
        Promise.all([
            // 缓存静态资源
            caches.open(STATIC_CACHE).then(cache => {
                console.log('Service Worker: Caching static assets');
                return cache.addAll(STATIC_ASSETS);
            }),
            
            // 跳过等待，立即激活
            self.skipWaiting()
        ])
    );
});

// 激活事件 - 清理旧缓存
self.addEventListener('activate', event => {
    console.log('Service Worker: Activating...');
    
    event.waitUntil(
        Promise.all([
            // 清理旧缓存
            caches.keys().then(cacheNames => {
                return Promise.all(
                    cacheNames.map(cacheName => {
                        if (cacheName !== STATIC_CACHE && 
                            cacheName !== DYNAMIC_CACHE && 
                            cacheName !== API_CACHE) {
                            console.log('Service Worker: Deleting old cache:', cacheName);
                            return caches.delete(cacheName);
                        }
                    })
                );
            }),
            
            // 立即控制所有客户端
            self.clients.claim()
        ])
    );
});

// 拦截网络请求
self.addEventListener('fetch', event => {
    const { request } = event;
    const url = new URL(request.url);
    
    // 跳过非HTTP请求
    if (!request.url.startsWith('http')) {
        return;
    }
    
    // 处理不同类型的请求
    if (isStaticAsset(request)) {
        event.respondWith(handleStaticAsset(request));
    } else if (isApiRequest(request)) {
        event.respondWith(handleApiRequest(request));
    } else {
        event.respondWith(handleDynamicRequest(request));
    }
});

/**
 * 判断是否为静态资源
 */
function isStaticAsset(request) {
    const url = new URL(request.url);
    return url.pathname.startsWith('/static/') || 
           STATIC_ASSETS.includes(url.pathname);
}

/**
 * 判断是否为API请求
 */
function isApiRequest(request) {
    const url = new URL(request.url);
    return url.pathname.startsWith('/api/');
}

/**
 * 处理静态资源请求 - 缓存优先策略
 */
async function handleStaticAsset(request) {
    try {
        // 先从缓存中查找
        const cachedResponse = await caches.match(request);
        if (cachedResponse) {
            return cachedResponse;
        }
        
        // 缓存中没有，从网络获取
        const networkResponse = await fetch(request);
        
        // 缓存成功的响应
        if (networkResponse.ok) {
            const cache = await caches.open(STATIC_CACHE);
            cache.put(request, networkResponse.clone());
        }
        
        return networkResponse;
    } catch (error) {
        console.error('Static asset fetch failed:', error);
        
        // 返回离线页面或默认内容
        if (request.destination === 'document') {
            return caches.match('/offline.html');
        }
        
        // 返回空响应
        return new Response('', { status: 408, statusText: 'Request Timeout' });
    }
}

/**
 * 处理API请求
 */
async function handleApiRequest(request) {
    const url = new URL(request.url);
    const path = url.pathname;
    
    // 网络优先的路径
    if (NETWORK_FIRST_PATHS.some(p => path.startsWith(p))) {
        return handleNetworkFirst(request);
    }
    
    // 可缓存的API路径
    if (CACHEABLE_API_PATHS.some(p => path.startsWith(p))) {
        return handleCacheFirst(request);
    }
    
    // 默认网络优先
    return handleNetworkFirst(request);
}

/**
 * 网络优先策略
 */
async function handleNetworkFirst(request) {
    try {
        const networkResponse = await fetch(request);
        
        // 缓存GET请求的成功响应
        if (request.method === 'GET' && networkResponse.ok) {
            const cache = await caches.open(API_CACHE);
            cache.put(request, networkResponse.clone());
        }
        
        return networkResponse;
    } catch (error) {
        console.log('Network request failed, trying cache:', error);
        
        // 网络失败，尝试从缓存获取
        const cachedResponse = await caches.match(request);
        if (cachedResponse) {
            return cachedResponse;
        }
        
        // 返回离线响应
        return new Response(
            JSON.stringify({
                error: 'Network unavailable',
                message: '网络连接不可用，请检查网络设置'
            }),
            {
                status: 503,
                statusText: 'Service Unavailable',
                headers: { 'Content-Type': 'application/json' }
            }
        );
    }
}

/**
 * 缓存优先策略
 */
async function handleCacheFirst(request) {
    try {
        // 先从缓存中查找
        const cachedResponse = await caches.match(request);
        if (cachedResponse) {
            // 在后台更新缓存
            updateCacheInBackground(request);
            return cachedResponse;
        }
        
        // 缓存中没有，从网络获取
        const networkResponse = await fetch(request);
        
        if (networkResponse.ok) {
            const cache = await caches.open(API_CACHE);
            cache.put(request, networkResponse.clone());
        }
        
        return networkResponse;
    } catch (error) {
        console.error('Cache first request failed:', error);
        
        return new Response(
            JSON.stringify({
                error: 'Request failed',
                message: '请求失败，请稍后重试'
            }),
            {
                status: 500,
                statusText: 'Internal Server Error',
                headers: { 'Content-Type': 'application/json' }
            }
        );
    }
}

/**
 * 处理动态请求
 */
async function handleDynamicRequest(request) {
    try {
        const networkResponse = await fetch(request);
        
        // 缓存成功的GET请求
        if (request.method === 'GET' && networkResponse.ok) {
            const cache = await caches.open(DYNAMIC_CACHE);
            cache.put(request, networkResponse.clone());
        }
        
        return networkResponse;
    } catch (error) {
        console.log('Dynamic request failed, trying cache:', error);
        
        // 尝试从缓存获取
        const cachedResponse = await caches.match(request);
        if (cachedResponse) {
            return cachedResponse;
        }
        
        // 返回离线页面
        if (request.destination === 'document') {
            return caches.match('/offline.html') || 
                   new Response('<h1>离线模式</h1><p>网络连接不可用</p>', {
                       headers: { 'Content-Type': 'text/html' }
                   });
        }
        
        return new Response('', { status: 408, statusText: 'Request Timeout' });
    }
}

/**
 * 后台更新缓存
 */
async function updateCacheInBackground(request) {
    try {
        const networkResponse = await fetch(request);
        if (networkResponse.ok) {
            const cache = await caches.open(API_CACHE);
            await cache.put(request, networkResponse);
        }
    } catch (error) {
        console.log('Background cache update failed:', error);
    }
}

// 推送通知事件
self.addEventListener('push', event => {
    console.log('Service Worker: Push received');
    
    let data = {};
    if (event.data) {
        try {
            data = event.data.json();
        } catch (e) {
            data = { title: '新消息', body: event.data.text() };
        }
    }
    
    const options = {
        title: data.title || '业务分析系统',
        body: data.body || '您有新的消息',
        icon: '/static/mobile/icons/icon-192x192.png',
        badge: '/static/mobile/icons/badge-72x72.png',
        image: data.image,
        tag: data.tag || 'general',
        requireInteraction: data.requireInteraction || false,
        actions: data.actions || [
            {
                action: 'view',
                title: '查看',
                icon: '/static/mobile/icons/action-view.png'
            },
            {
                action: 'close',
                title: '关闭',
                icon: '/static/mobile/icons/action-close.png'
            }
        ],
        data: {
            url: data.url || '/mobile/',
            timestamp: Date.now()
        }
    };
    
    event.waitUntil(
        self.registration.showNotification(options.title, options)
    );
});

// 通知点击事件
self.addEventListener('notificationclick', event => {
    console.log('Service Worker: Notification clicked');
    
    const notification = event.notification;
    const action = event.action;
    const data = notification.data || {};
    
    notification.close();
    
    if (action === 'close') {
        return;
    }
    
    // 打开或聚焦到应用
    event.waitUntil(
        clients.matchAll({ type: 'window', includeUncontrolled: true })
            .then(clientList => {
                const url = data.url || '/mobile/';
                
                // 查找已打开的窗口
                for (const client of clientList) {
                    if (client.url.includes('/mobile/') && 'focus' in client) {
                        client.postMessage({
                            type: 'NOTIFICATION_CLICK',
                            action: action,
                            data: data
                        });
                        return client.focus();
                    }
                }
                
                // 打开新窗口
                if (clients.openWindow) {
                    return clients.openWindow(url);
                }
            })
    );
});

// 后台同步事件
self.addEventListener('sync', event => {
    console.log('Service Worker: Background sync triggered');
    
    if (event.tag === 'background-sync') {
        event.waitUntil(doBackgroundSync());
    }
});

/**
 * 执行后台同步
 */
async function doBackgroundSync() {
    try {
        // 获取待同步的数据
        const syncData = await getSyncData();
        
        if (syncData.length > 0) {
            console.log('Service Worker: Syncing', syncData.length, 'items');
            
            // 同步数据到服务器
            for (const item of syncData) {
                try {
                    await syncItem(item);
                    await removeSyncData(item.id);
                } catch (error) {
                    console.error('Sync item failed:', error);
                }
            }
        }
    } catch (error) {
        console.error('Background sync failed:', error);
    }
}

/**
 * 获取待同步数据
 */
async function getSyncData() {
    // 从IndexedDB或其他存储中获取待同步数据
    // 这里返回空数组作为示例
    return [];
}

/**
 * 同步单个数据项
 */
async function syncItem(item) {
    const response = await fetch('/api/sync', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(item)
    });
    
    if (!response.ok) {
        throw new Error(`Sync failed: ${response.status}`);
    }
    
    return response.json();
}

/**
 * 移除已同步的数据
 */
async function removeSyncData(id) {
    // 从存储中移除已同步的数据
    console.log('Removing synced data:', id);
}

// 消息处理
self.addEventListener('message', event => {
    const { type, data } = event.data;
    
    switch (type) {
        case 'SKIP_WAITING':
            self.skipWaiting();
            break;
            
        case 'GET_VERSION':
            event.ports[0].postMessage({ version: CACHE_NAME });
            break;
            
        case 'CLEAN_CACHE':
            cleanOldCaches().then(() => {
                event.ports[0].postMessage({ success: true });
            });
            break;
            
        default:
            console.log('Unknown message type:', type);
    }
});

/**
 * 清理旧缓存
 */
async function cleanOldCaches() {
    const cacheNames = await caches.keys();
    const oldCaches = cacheNames.filter(name => 
        name !== STATIC_CACHE && 
        name !== DYNAMIC_CACHE && 
        name !== API_CACHE
    );
    
    return Promise.all(oldCaches.map(name => caches.delete(name)));
}