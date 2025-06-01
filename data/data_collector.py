from abc import ABC, abstractmethod
import pandas as pd
from typing import Optional, Dict, Any
import logging

from .cache_manager import CacheManager

logger = logging.getLogger(__name__)

class DataCollector(ABC):
    """数据采集基类"""
    
    def __init__(self, config: Dict[str, Any], cache_manager: Optional[CacheManager] = None):
        """
        初始化数据采集器
        
        Args:
            config: 配置信息
            cache_manager: 缓存管理器实例
        """
        self.config = config
        self.data: Optional[pd.DataFrame] = None
        self.cache_manager = cache_manager or CacheManager()
        self.source_type = self._get_source_type()
    
    @abstractmethod
    def _get_source_type(self) -> str:
        """
        获取数据源类型
        
        Returns:
            str: 数据源类型
        """
        pass
    
    @abstractmethod
    def collect(self) -> pd.DataFrame:
        """
        采集数据
        
        Returns:
            DataFrame: 采集到的数据
        """
        pass
    
    @abstractmethod
    def validate(self, data: pd.DataFrame) -> bool:
        """
        验证数据
        
        Args:
            data: 待验证的数据
            
        Returns:
            bool: 验证是否通过
        """
        pass
    
    def clean(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        清洗数据
        
        Args:
            data: 待清洗的数据
            
        Returns:
            DataFrame: 清洗后的数据
        """
        # 删除重复行
        data = data.drop_duplicates()
        
        # 处理缺失值
        numeric_columns = data.select_dtypes(include=['int64', 'float64']).columns
        data[numeric_columns] = data[numeric_columns].fillna(0)
        
        # 处理异常值
        for col in numeric_columns:
            Q1 = data[col].quantile(0.25)
            Q3 = data[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            data[col] = data[col].clip(lower_bound, upper_bound)
        
        return data
    
    def collect_with_cache(self, use_cache: bool = True, incremental: bool = False) -> pd.DataFrame:
        """
        带缓存的数据采集
        
        Args:
            use_cache: 是否使用缓存
            incremental: 是否使用增量采集
            
        Returns:
            DataFrame: 采集到的数据
        """
        cache_key = self.cache_manager.get_cache_key(self.source_type, self.config)
        
        if use_cache:
            # 尝试从缓存获取数据
            cached_data = self.cache_manager.get_cached_data(cache_key)
            if cached_data is not None:
                logger.info("使用缓存数据")
                self.data = cached_data
                return self.data
        
        # 采集新数据
        new_data = self.collect()
        
        if incremental:
            # 获取增量数据
            new_data = self.cache_manager.get_incremental_data(cache_key, new_data)
            if not new_data.empty:
                # 合并增量数据
                cached_data = self.cache_manager.get_cached_data(cache_key)
                if cached_data is not None:
                    self.data = pd.concat([cached_data, new_data], ignore_index=True)
                else:
                    self.data = new_data
            else:
                self.data = self.cache_manager.get_cached_data(cache_key)
        else:
            self.data = new_data
        
        # 保存到缓存
        if self.data is not None:
            self.cache_manager.save_to_cache(cache_key, self.data)
        
        return self.data

class CSVDataCollector(DataCollector):
    """CSV数据采集器"""
    
    def _get_source_type(self) -> str:
        return "csv"
    
    def collect(self) -> pd.DataFrame:
        """
        从CSV文件采集数据
        
        Returns:
            DataFrame: 采集到的数据
        """
        try:
            file_path = self.config.get('file_path')
            if not file_path:
                raise ValueError("未指定CSV文件路径")
            
            data = pd.read_csv(file_path)
            logger.info(f"成功从{file_path}加载数据")
            return data
            
        except Exception as e:
            logger.error(f"加载CSV文件失败: {str(e)}")
            raise
    
    def validate(self, data: pd.DataFrame) -> bool:
        """
        验证CSV数据
        
        Args:
            data: 待验证的数据
            
        Returns:
            bool: 验证是否通过
        """
        required_columns = ['date', 'category', 'region', 'gmv', 'dau', 
                          'order_price', 'conversion_rate']
        
        # 检查必需列是否存在
        missing_columns = [col for col in required_columns if col not in data.columns]
        if missing_columns:
            logger.error(f"缺少必需列: {missing_columns}")
            return False
        
        # 检查数据类型
        try:
            data['date'] = pd.to_datetime(data['date'])
            data['gmv'] = pd.to_numeric(data['gmv'])
            data['dau'] = pd.to_numeric(data['dau'])
            data['order_price'] = pd.to_numeric(data['order_price'])
            data['conversion_rate'] = pd.to_numeric(data['conversion_rate'])
            return True
        except Exception as e:
            logger.error(f"数据类型转换失败: {str(e)}")
            return False

class DatabaseDataCollector(DataCollector):
    """数据库数据采集器"""
    
    def _get_source_type(self) -> str:
        return "database"
    
    def collect(self) -> pd.DataFrame:
        """
        从数据库采集数据
        
        Returns:
            DataFrame: 采集到的数据
        """
        try:
            # TODO: 实现数据库连接和数据获取
            raise NotImplementedError("数据库采集器尚未实现")
            
        except Exception as e:
            logger.error(f"从数据库加载数据失败: {str(e)}")
            raise
    
    def validate(self, data: pd.DataFrame) -> bool:
        """
        验证数据库数据
        
        Args:
            data: 待验证的数据
            
        Returns:
            bool: 验证是否通过
        """
        # TODO: 实现数据库数据验证
        raise NotImplementedError("数据库数据验证尚未实现")

class APIDataCollector(DataCollector):
    """API数据采集器"""
    
    def _get_source_type(self) -> str:
        return "api"
    
    def collect(self) -> pd.DataFrame:
        """
        从API采集数据
        
        Returns:
            DataFrame: 采集到的数据
        """
        try:
            # TODO: 实现API数据获取
            raise NotImplementedError("API采集器尚未实现")
            
        except Exception as e:
            logger.error(f"从API加载数据失败: {str(e)}")
            raise
    
    def validate(self, data: pd.DataFrame) -> bool:
        """
        验证API数据
        
        Args:
            data: 待验证的数据
            
        Returns:
            bool: 验证是否通过
        """
        # TODO: 实现API数据验证
        raise NotImplementedError("API数据验证尚未实现") 