from typing import Dict, Any, Optional
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import logging
import os
import sys

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from .data_collector import DataCollector

logger = logging.getLogger(__name__)

class DatabaseDataCollector(DataCollector):
    """数据库数据采集器 - 支持MySQL和其他数据库"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        初始化数据库采集器
        
        Args:
            config: 配置信息，包含：
                - connection_string: 数据库连接字符串
                - 或者分别提供：
                  - host: 主机地址
                  - port: 端口
                  - user: 用户名
                  - password: 密码
                  - database: 数据库名
                  - db_type: 数据库类型 (mysql, postgresql, sqlite)
                - query: SQL查询语句
                - table: 表名（如果使用表名而不是查询语句）
        """
        super().__init__(config)
        self.engine = None
        self._init_connection()
    
    def _init_connection(self):
        """初始化数据库连接"""
        try:
            connection_string = self.config.get('connection_string')
            
            # 如果没有提供连接字符串，则根据配置构建
            if not connection_string:
                connection_string = self._build_connection_string()
            
            self.engine = create_engine(connection_string)
            logger.info("数据库连接初始化成功")
            
        except Exception as e:
            logger.error(f"数据库连接初始化失败: {str(e)}")
            raise
    
    def _build_connection_string(self) -> str:
        """根据配置构建数据库连接字符串"""
        db_type = self.config.get('db_type', 'mysql').lower()
        host = self.config.get('host', 'localhost')
        port = self.config.get('port', 3306)
        user = self.config.get('user', 'root')
        password = self.config.get('password', '')
        database = self.config.get('database', 'analysis_system')
        charset = self.config.get('charset', 'utf8mb4')
        
        if db_type == 'mysql':
            return f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset={charset}"
        elif db_type == 'postgresql':
            return f"postgresql://{user}:{password}@{host}:{port}/{database}"
        elif db_type == 'sqlite':
            return f"sqlite:///{database}"
        else:
            raise ValueError(f"不支持的数据库类型: {db_type}")
    
    def collect(self) -> pd.DataFrame:
        """
        从数据库采集数据
        
        Returns:
            DataFrame: 采集到的数据
        """
        try:
            query = self.config.get('query')
            table = self.config.get('table')
            
            if query:
                self.data = pd.read_sql(query, self.engine)
                logger.info("成功执行SQL查询")
            elif table:
                self.data = pd.read_sql_table(table, self.engine)
                logger.info(f"成功从表{table}读取数据")
            else:
                raise ValueError("未指定查询语句或表名")
            
            return self.data
            
        except SQLAlchemyError as e:
            logger.error(f"数据库查询失败: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"数据采集失败: {str(e)}")
            raise
    
    def validate(self, data: pd.DataFrame) -> bool:
        """
        验证数据库数据
        
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
            
            return True
            
        except Exception as e:
            logger.error(f"数据验证失败: {str(e)}")
            return False
    
    def __del__(self):
        """清理数据库连接"""
        if self.engine:
            self.engine.dispose()
            logger.info("数据库连接已关闭")

def fetch_large_data(table, chunk_size=50_000):
    """流式读取大数据表"""
    offset = 0
    while True:
        data = pd.read_sql(
            f"SELECT * FROM {table} ORDER BY id LIMIT {chunk_size} OFFSET {offset}",
            con
        )
        if data.empty:
            break
        yield data
        offset += chunk_size 