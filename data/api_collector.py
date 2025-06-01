from typing import Dict, Any, Optional, List
import pandas as pd
import requests
import aiohttp
import asyncio
import logging
from datetime import datetime, timedelta

from .data_collector import DataCollector

logger = logging.getLogger(__name__)

class APIDataCollector(DataCollector):
    """API数据采集器"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化API采集器
        
        Args:
            config: 配置信息，包含：
                - base_url: API基础URL
                - endpoints: API端点列表
                - headers: 请求头
                - params: 请求参数
                - auth: 认证信息
        """
        super().__init__(config)
        self.session = None
        self._init_session()
    
    def _init_session(self):
        """初始化HTTP会话"""
        try:
            self.session = requests.Session()
            headers = self.config.get('headers', {})
            self.session.headers.update(headers)
            
            # 设置认证信息
            auth = self.config.get('auth')
            if auth:
                self.session.auth = (auth.get('username'), auth.get('password'))
            
            logger.info("HTTP会话初始化成功")
            
        except Exception as e:
            logger.error(f"HTTP会话初始化失败: {str(e)}")
            raise
    
    async def _fetch_endpoint(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        异步获取单个端点数据
        
        Args:
            endpoint: API端点
            params: 请求参数
            
        Returns:
            Dict: 响应数据
        """
        url = f"{self.config['base_url']}{endpoint}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.error(f"API请求失败: {response.status} - {await response.text()}")
                        return None
        except Exception as e:
            logger.error(f"获取端点{endpoint}数据失败: {str(e)}")
            return None
    
    async def _fetch_all_endpoints(self) -> List[Dict[str, Any]]:
        """
        异步获取所有端点数据
        
        Returns:
            List[Dict]: 所有端点的响应数据
        """
        endpoints = self.config.get('endpoints', [])
        params = self.config.get('params', {})
        
        tasks = [self._fetch_endpoint(endpoint, params) for endpoint in endpoints]
        results = await asyncio.gather(*tasks)
        
        return [result for result in results if result is not None]
    
    def collect(self) -> pd.DataFrame:
        """
        从API采集数据
        
        Returns:
            DataFrame: 采集到的数据
        """
        try:
            # 运行异步任务
            loop = asyncio.get_event_loop()
            results = loop.run_until_complete(self._fetch_all_endpoints())
            
            if not results:
                raise ValueError("未获取到任何数据")
            
            # 合并数据
            data_list = []
            for result in results:
                # 转换API响应为DataFrame格式
                df = pd.DataFrame(result)
                data_list.append(df)
            
            self.data = pd.concat(data_list, ignore_index=True)
            logger.info(f"成功获取{len(self.data)}条数据")
            
            return self.data
            
        except Exception as e:
            logger.error(f"API数据采集失败: {str(e)}")
            raise
    
    def validate(self, data: pd.DataFrame) -> bool:
        """
        验证API数据
        
        Args:
            data: 待验证的数据
            
        Returns:
            bool: 验证是否通过
        """
        try:
            # 检查数据是否为空
            if data.empty:
                logger.error("数据为空")
                return False
            
            # 检查必需列是否存在
            required_columns = ['date', 'category', 'region', 'gmv', 'dau', 
                              'order_price', 'conversion_rate']
            missing_columns = [col for col in required_columns if col not in data.columns]
            if missing_columns:
                logger.error(f"缺少必需列: {missing_columns}")
                return False
            
            # 检查数据类型
            data['date'] = pd.to_datetime(data['date'])
            data['gmv'] = pd.to_numeric(data['gmv'])
            data['dau'] = pd.to_numeric(data['dau'])
            data['order_price'] = pd.to_numeric(data['order_price'])
            data['conversion_rate'] = pd.to_numeric(data['conversion_rate'])
            
            # 检查数值范围
            if (data['gmv'] < 0).any():
                logger.error("存在负GMV值")
                return False
            if (data['dau'] < 0).any():
                logger.error("存在负DAU值")
                return False
            if (data['order_price'] < 0).any():
                logger.error("存在负订单价格")
                return False
            if ((data['conversion_rate'] < 0) | (data['conversion_rate'] > 1)).any():
                logger.error("转化率超出合理范围[0,1]")
                return False
            
            # 检查日期范围
            today = datetime.now().date()
            if (data['date'].dt.date > today).any():
                logger.error("存在未来日期数据")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"数据验证失败: {str(e)}")
            return False
    
    def __del__(self):
        """清理HTTP会话"""
        if self.session:
            self.session.close()
            logger.info("HTTP会话已关闭") 