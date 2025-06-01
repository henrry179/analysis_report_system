import os
import json
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class CacheManager:
    """数据缓存管理器"""
    
    def __init__(self, cache_dir: str = "cache"):
        """
        初始化缓存管理器
        
        Args:
            cache_dir: 缓存目录路径
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_file = self.cache_dir / "metadata.json"
        self._load_metadata()
    
    def _load_metadata(self):
        """加载缓存元数据"""
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r', encoding='utf-8') as f:
                self.metadata = json.load(f)
        else:
            self.metadata = {}
    
    def _save_metadata(self):
        """保存缓存元数据"""
        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, ensure_ascii=False, indent=2)
    
    def get_cache_key(self, source_type: str, config: Dict[str, Any]) -> str:
        """
        生成缓存键
        
        Args:
            source_type: 数据源类型
            config: 配置信息
            
        Returns:
            str: 缓存键
        """
        if source_type == "csv":
            return f"csv_{config.get('file_path', '')}"
        elif source_type == "database":
            return f"db_{config.get('connection_string', '')}_{config.get('table', '')}"
        elif source_type == "api":
            return f"api_{config.get('base_url', '')}_{','.join(config.get('endpoints', []))}"
        else:
            raise ValueError(f"不支持的数据源类型: {source_type}")
    
    def get_cached_data(self, cache_key: str, max_age_hours: int = 24) -> Optional[pd.DataFrame]:
        """
        获取缓存数据
        
        Args:
            cache_key: 缓存键
            max_age_hours: 最大缓存时间（小时）
            
        Returns:
            Optional[DataFrame]: 缓存的数据，如果不存在或已过期则返回None
        """
        cache_file = self.cache_dir / f"{cache_key}.parquet"
        
        if not cache_file.exists():
            return None
        
        # 检查缓存元数据
        if cache_key not in self.metadata:
            return None
        
        cache_info = self.metadata[cache_key]
        cache_time = datetime.fromisoformat(cache_info['timestamp'])
        
        # 检查缓存是否过期
        if datetime.now() - cache_time > timedelta(hours=max_age_hours):
            return None
        
        try:
            return pd.read_parquet(cache_file)
        except Exception as e:
            logger.error(f"读取缓存数据失败: {str(e)}")
            return None
    
    def save_to_cache(self, cache_key: str, data: pd.DataFrame):
        """
        保存数据到缓存
        
        Args:
            cache_key: 缓存键
            data: 要缓存的数据
        """
        try:
            cache_file = self.cache_dir / f"{cache_key}.parquet"
            data.to_parquet(cache_file)
            
            # 更新元数据
            self.metadata[cache_key] = {
                'timestamp': datetime.now().isoformat(),
                'rows': len(data),
                'columns': list(data.columns)
            }
            self._save_metadata()
            
            logger.info(f"数据已缓存到{cache_file}")
            
        except Exception as e:
            logger.error(f"保存缓存数据失败: {str(e)}")
    
    def clear_cache(self, cache_key: Optional[str] = None):
        """
        清除缓存
        
        Args:
            cache_key: 要清除的缓存键，如果为None则清除所有缓存
        """
        try:
            if cache_key:
                cache_file = self.cache_dir / f"{cache_key}.parquet"
                if cache_file.exists():
                    cache_file.unlink()
                if cache_key in self.metadata:
                    del self.metadata[cache_key]
            else:
                for file in self.cache_dir.glob("*.parquet"):
                    file.unlink()
                self.metadata = {}
            
            self._save_metadata()
            logger.info(f"已清除缓存: {cache_key if cache_key else 'all'}")
            
        except Exception as e:
            logger.error(f"清除缓存失败: {str(e)}")
    
    def get_incremental_data(self, cache_key: str, data: pd.DataFrame, 
                           date_column: str = 'date') -> pd.DataFrame:
        """
        获取增量数据
        
        Args:
            cache_key: 缓存键
            data: 新数据
            date_column: 日期列名
            
        Returns:
            DataFrame: 增量数据
        """
        cached_data = self.get_cached_data(cache_key)
        if cached_data is None:
            return data
        
        # 获取最新日期
        latest_date = pd.to_datetime(cached_data[date_column]).max()
        
        # 筛选新数据
        new_data = data[pd.to_datetime(data[date_column]) > latest_date]
        
        if len(new_data) > 0:
            logger.info(f"发现{len(new_data)}条新数据")
            return new_data
        else:
            logger.info("没有新数据")
            return pd.DataFrame() 