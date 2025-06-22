#!/usr/bin/env python3
"""
本地数据导入工具
支持多种格式的本地数据集导入到MySQL数据库
"""

import os
import sys
import json
import logging
from typing import Dict, Any, Optional, List, Union
import pandas as pd
from datetime import datetime
import glob
from pathlib import Path

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.data.mysql_manager import MySQLManager
from src.config.database_config import DatabaseConfig

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LocalDataImporter:
    """本地数据导入器"""
    
    def __init__(self, mysql_manager: MySQLManager):
        """
        初始化数据导入器
        
        Args:
            mysql_manager: MySQL管理器实例
        """
        self.mysql_manager = mysql_manager
        self.supported_formats = ['.csv', '.xlsx', '.xls', '.json', '.parquet']
        
        # 数据类型映射
        self.dtype_mapping = {
            'object': 'TEXT',
            'int64': 'INTEGER',
            'float64': 'FLOAT',
            'bool': 'BOOLEAN',
            'datetime64[ns]': 'DATETIME'
        }
        
        # 预定义表结构映射
        self.table_schemas = {
            'business_data': {
                'date': 'DATETIME',
                'category': 'VARCHAR(100)',
                'region': 'VARCHAR(100)', 
                'gmv': 'FLOAT',
                'dau': 'INTEGER',
                'order_price': 'FLOAT',
                'conversion_rate': 'FLOAT'
            },
            'financial_data': {
                'date': 'DATETIME',
                'transaction_type': 'VARCHAR(50)',
                'currency': 'VARCHAR(10)',
                'amount': 'FLOAT',
                'fee': 'FLOAT',
                'user_id': 'VARCHAR(100)',
                'status': 'VARCHAR(20)'
            },
            'user_data': {
                'username': 'VARCHAR(50)',
                'email': 'VARCHAR(100)',
                'role': 'VARCHAR(20)',
                'is_active': 'INTEGER',
                'created_at': 'DATETIME',
                'last_login': 'DATETIME'
            }
        }
    
    def scan_data_directory(self, directory: str = 'data') -> List[Dict[str, Any]]:
        """
        扫描数据目录，发现可导入的数据文件
        
        Args:
            directory: 数据目录路径
            
        Returns:
            List: 发现的数据文件信息列表
        """
        logger.info(f"🔍 扫描数据目录: {directory}")
        
        found_files = []
        
        # 扫描所有支持的文件格式
        for ext in self.supported_formats:
            pattern = os.path.join(directory, '**', f'*{ext}')
            files = glob.glob(pattern, recursive=True)
            
            for file_path in files:
                try:
                    file_info = self._analyze_file(file_path)
                    if file_info:
                        found_files.append(file_info)
                except Exception as e:
                    logger.warning(f"分析文件失败 {file_path}: {str(e)}")
        
        logger.info(f"✅ 发现 {len(found_files)} 个可导入文件")
        return found_files
    
    def _analyze_file(self, file_path: str) -> Optional[Dict[str, Any]]:
        """
        分析文件基本信息
        
        Args:
            file_path: 文件路径
            
        Returns:
            Dict: 文件信息
        """
        file_ext = Path(file_path).suffix.lower()
        file_size = os.path.getsize(file_path)
        
        # 读取文件头部数据进行分析
        try:
            if file_ext == '.csv':
                df_sample = pd.read_csv(file_path, nrows=5)
            elif file_ext in ['.xlsx', '.xls']:
                df_sample = pd.read_excel(file_path, nrows=5)
            elif file_ext == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                if isinstance(data, list) and len(data) > 0:
                    df_sample = pd.DataFrame(data[:5])
                else:
                    return None
            elif file_ext == '.parquet':
                df_sample = pd.read_parquet(file_path).head(5)
            else:
                return None
            
            return {
                'file_path': file_path,
                'file_name': os.path.basename(file_path),
                'file_ext': file_ext,
                'file_size': file_size,
                'file_size_mb': round(file_size / 1024 / 1024, 2),
                'columns': list(df_sample.columns),
                'column_count': len(df_sample.columns),
                'sample_data': df_sample.to_dict('records'),
                'suggested_table': self._suggest_table_name(file_path, df_sample.columns)
            }
            
        except Exception as e:
            logger.warning(f"无法分析文件 {file_path}: {str(e)}")
            return None
    
    def _suggest_table_name(self, file_path: str, columns: List[str]) -> str:
        """
        根据文件名和列名建议表名
        
        Args:
            file_path: 文件路径
            columns: 列名列表
            
        Returns:
            str: 建议的表名
        """
        file_name = Path(file_path).stem.lower()
        
        # 根据文件名匹配
        if any(keyword in file_name for keyword in ['business', 'sales', 'revenue']):
            return 'business_data'
        elif any(keyword in file_name for keyword in ['financial', 'transaction', 'payment']):
            return 'financial_data'
        elif any(keyword in file_name for keyword in ['user', 'customer', 'client']):
            return 'user_data'
        elif any(keyword in file_name for keyword in ['ai', 'agent', 'model']):
            return 'ai_agent_data'
        elif any(keyword in file_name for keyword in ['community', 'group']):
            return 'community_group_buying'
        elif any(keyword in file_name for keyword in ['log', 'system']):
            return 'system_logs'
        
        # 根据列名匹配
        columns_str = ' '.join(columns).lower()
        if any(keyword in columns_str for keyword in ['gmv', 'dau', 'conversion']):
            return 'business_data'
        elif any(keyword in columns_str for keyword in ['amount', 'transaction', 'currency']):
            return 'financial_data'
        elif any(keyword in columns_str for keyword in ['username', 'email', 'password']):
            return 'user_data'
        
        # 默认使用文件名
        return file_name.replace('-', '_').replace(' ', '_')
    
    def import_file(self, 
                   file_path: str, 
                   table_name: str = None,
                   chunk_size: int = 1000,
                   if_exists: str = 'append') -> bool:
        """
        导入单个文件到数据库
        
        Args:
            file_path: 文件路径
            table_name: 目标表名
            chunk_size: 分块大小
            if_exists: 如果表存在的处理方式 ('append', 'replace', 'fail')
            
        Returns:
            bool: 导入是否成功
        """
        try:
            logger.info(f"📥 开始导入文件: {file_path}")
            
            if not os.path.exists(file_path):
                logger.error(f"❌ 文件不存在: {file_path}")
                return False
            
            # 读取数据
            df = self._read_file(file_path)
            if df is None or df.empty:
                logger.error(f"❌ 无法读取文件或文件为空: {file_path}")
                return False
            
            # 确定表名
            if not table_name:
                table_name = self._suggest_table_name(file_path, df.columns)
            
            # 数据预处理
            df_processed = self._preprocess_data(df, table_name)
            
            # 导入数据库
            success = self._import_to_database(df_processed, table_name, chunk_size, if_exists)
            
            if success:
                logger.info(f"✅ 文件导入成功: {file_path} -> {table_name} ({len(df_processed)} 条记录)")
                return True
            else:
                logger.error(f"❌ 文件导入失败: {file_path}")
                return False
                
        except Exception as e:
            logger.error(f"❌ 导入文件时发生错误: {str(e)}")
            return False
    
    def _read_file(self, file_path: str) -> Optional[pd.DataFrame]:
        """
        读取文件数据
        
        Args:
            file_path: 文件路径
            
        Returns:
            DataFrame: 读取的数据
        """
        file_ext = Path(file_path).suffix.lower()
        
        try:
            if file_ext == '.csv':
                # 尝试不同编码
                for encoding in ['utf-8', 'gbk', 'gb2312', 'latin1']:
                    try:
                        return pd.read_csv(file_path, encoding=encoding)
                    except UnicodeDecodeError:
                        continue
                logger.error(f"无法读取CSV文件，尝试了多种编码: {file_path}")
                return None
                
            elif file_ext in ['.xlsx', '.xls']:
                return pd.read_excel(file_path)
                
            elif file_ext == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                if isinstance(data, list):
                    return pd.DataFrame(data)
                elif isinstance(data, dict):
                    return pd.DataFrame([data])
                else:
                    logger.error(f"不支持的JSON格式: {file_path}")
                    return None
                    
            elif file_ext == '.parquet':
                return pd.read_parquet(file_path)
                
            else:
                logger.error(f"不支持的文件格式: {file_ext}")
                return None
                
        except Exception as e:
            logger.error(f"读取文件失败 {file_path}: {str(e)}")
            return None
    
    def _preprocess_data(self, df: pd.DataFrame, table_name: str) -> pd.DataFrame:
        """
        数据预处理
        
        Args:
            df: 原始数据
            table_name: 目标表名
            
        Returns:
            DataFrame: 处理后的数据
        """
        df_processed = df.copy()
        
        # 清理列名
        df_processed.columns = [col.strip().replace(' ', '_').replace('-', '_').lower() 
                               for col in df_processed.columns]
        
        # 处理缺失值
        df_processed = df_processed.fillna('')
        
        # 日期列处理
        date_columns = ['date', 'created_at', 'updated_at', 'last_login']
        for col in date_columns:
            if col in df_processed.columns:
                try:
                    df_processed[col] = pd.to_datetime(df_processed[col], errors='coerce')
                except:
                    pass
        
        # 添加时间戳
        if 'created_at' not in df_processed.columns:
            df_processed['created_at'] = datetime.now()
        
        if 'updated_at' not in df_processed.columns:
            df_processed['updated_at'] = datetime.now()
        
        # 根据表类型进行特定处理
        if table_name == 'business_data':
            df_processed = self._process_business_data(df_processed)
        elif table_name == 'financial_data':
            df_processed = self._process_financial_data(df_processed)
        elif table_name == 'user_data':
            df_processed = self._process_user_data(df_processed)
        
        return df_processed
    
    def _process_business_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """处理业务数据"""
        # 确保数值列为数值类型
        numeric_columns = ['gmv', 'dau', 'order_price', 'conversion_rate']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        return df
    
    def _process_financial_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """处理金融数据"""
        # 确保金额列为数值类型
        numeric_columns = ['amount', 'fee']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        return df
    
    def _process_user_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """处理用户数据"""
        # 处理布尔列
        if 'is_active' in df.columns:
            df['is_active'] = df['is_active'].astype(int)
        
        return df
    
    def _import_to_database(self, 
                           df: pd.DataFrame, 
                           table_name: str, 
                           chunk_size: int,
                           if_exists: str) -> bool:
        """
        导入数据到数据库
        
        Args:
            df: 要导入的数据
            table_name: 表名
            chunk_size: 分块大小
            if_exists: 存在时的处理方式
            
        Returns:
            bool: 导入是否成功
        """
        try:
            engine = self.mysql_manager.db_config.engine
            
            # 分块导入大文件
            if len(df) > chunk_size:
                logger.info(f"📊 大文件分块导入，总计 {len(df)} 条记录，分块大小 {chunk_size}")
                
                for i in range(0, len(df), chunk_size):
                    chunk = df.iloc[i:i+chunk_size]
                    chunk.to_sql(table_name, engine, if_exists='append' if i > 0 else if_exists, index=False)
                    logger.info(f"  导入进度: {min(i+chunk_size, len(df))}/{len(df)} 条记录")
            else:
                df.to_sql(table_name, engine, if_exists=if_exists, index=False)
            
            logger.info(f"✅ 数据成功导入表 {table_name}")
            return True
            
        except Exception as e:
            logger.error(f"❌ 数据库导入失败: {str(e)}")
            return False
    
    def import_directory(self, 
                        directory: str = 'data',
                        table_mapping: Dict[str, str] = None,
                        if_exists: str = 'append') -> Dict[str, bool]:
        """
        批量导入目录中的所有数据文件
        
        Args:
            directory: 数据目录
            table_mapping: 文件到表名的映射
            if_exists: 存在时的处理方式
            
        Returns:
            Dict: 导入结果
        """
        logger.info(f"📁 开始批量导入目录: {directory}")
        
        # 扫描文件
        files = self.scan_data_directory(directory)
        
        results = {}
        
        for file_info in files:
            file_path = file_info['file_path']
            
            # 确定表名
            if table_mapping and file_info['file_name'] in table_mapping:
                table_name = table_mapping[file_info['file_name']]
            else:
                table_name = file_info['suggested_table']
            
            # 导入文件
            success = self.import_file(file_path, table_name, if_exists=if_exists)
            results[file_path] = success
        
        # 统计结果
        success_count = sum(1 for success in results.values() if success)
        total_count = len(results)
        
        logger.info(f"📊 批量导入完成: {success_count}/{total_count} 个文件成功导入")
        
        return results
    
    def create_import_report(self, results: Dict[str, bool]) -> str:
        """
        创建导入报告
        
        Args:
            results: 导入结果
            
        Returns:
            str: 报告内容
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        report = f"""
# 数据导入报告
生成时间: {timestamp}

## 导入统计
- 总文件数: {len(results)}
- 成功导入: {sum(1 for success in results.values() if success)}
- 导入失败: {sum(1 for success in results.values() if not success)}

## 详细结果
"""
        
        for file_path, success in results.items():
            status = "✅ 成功" if success else "❌ 失败"
            report += f"- {os.path.basename(file_path)}: {status}\n"
        
        return report


def interactive_import():
    """交互式数据导入"""
    print("📥 本地数据导入工具")
    print("=" * 50)
    
    # 检查MySQL连接
    print("🔧 请先配置MySQL连接...")
    
    # 获取数据库配置
    host = input("数据库主机 (默认: localhost): ") or "localhost"
    port = input("数据库端口 (默认: 3306): ") or "3306"
    user = input("数据库用户名 (默认: root): ") or "root"
    password = input("数据库密码: ")
    database = input("数据库名称 (默认: analysis_system): ") or "analysis_system"
    
    config = {
        'host': host,
        'port': int(port),
        'user': user,
        'password': password,
        'database': database
    }
    
    # 创建MySQL管理器
    mysql_manager = MySQLManager(config)
    if not mysql_manager.setup_database():
        print("❌ 数据库连接失败")
        return
    
    # 创建导入器
    importer = LocalDataImporter(mysql_manager)
    
    # 选择导入方式
    print("\n📂 选择导入方式:")
    print("1. 扫描并导入整个目录")
    print("2. 导入单个文件")
    
    choice = input("请选择 (1-2): ").strip()
    
    if choice == '1':
        # 目录导入
        data_dir = input("数据目录路径 (默认: data): ") or "data"
        
        if not os.path.exists(data_dir):
            print(f"❌ 目录不存在: {data_dir}")
            return
        
        # 扫描文件
        files = importer.scan_data_directory(data_dir)
        
        if not files:
            print("❌ 未发现可导入的数据文件")
            return
        
        print(f"\n📋 发现 {len(files)} 个数据文件:")
        for i, file_info in enumerate(files, 1):
            print(f"{i}. {file_info['file_name']} ({file_info['file_size_mb']}MB)")
            print(f"   列数: {file_info['column_count']}, 建议表名: {file_info['suggested_table']}")
        
        if input("\n确认导入所有文件？(y/n): ").lower() == 'y':
            results = importer.import_directory(data_dir)
            
            # 显示结果
            print("\n📊 导入结果:")
            for file_path, success in results.items():
                status = "✅" if success else "❌"
                print(f"{status} {os.path.basename(file_path)}")
            
            # 保存报告
            report = importer.create_import_report(results)
            report_file = f"data_import_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"\n📄 导入报告已保存: {report_file}")
    
    elif choice == '2':
        # 单文件导入
        file_path = input("文件路径: ")
        
        if not os.path.exists(file_path):
            print(f"❌ 文件不存在: {file_path}")
            return
        
        table_name = input("目标表名 (留空自动推测): ") or None
        
        if importer.import_file(file_path, table_name):
            print("✅ 文件导入成功")
        else:
            print("❌ 文件导入失败")
    
    mysql_manager.close_connection()
    print("\n👋 导入完成")


def main():
    """主函数"""
    try:
        interactive_import()
    except KeyboardInterrupt:
        print("\n\n👋 用户取消操作")
    except Exception as e:
        logger.error(f"程序执行失败: {str(e)}")


if __name__ == "__main__":
    main() 