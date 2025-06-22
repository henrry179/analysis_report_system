#!/usr/bin/env python3
"""
SQL代码管理器
支持本地SQL文件编写、执行、管理和个性化数据集导入
"""

import os
import sys
import json
import logging
import sqlite3
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime
import pandas as pd
from pathlib import Path
import re

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.config.database_config import DatabaseConfig
from src.data.mysql_manager import MySQLManager

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SQLManager:
    """SQL代码管理器"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化SQL管理器
        
        Args:
            config: 数据库配置
        """
        self.config = config
        self.mysql_manager = None
        self.sql_files_dir = "sql_scripts"
        self.datasets_dir = "custom_datasets"
        self.templates_dir = "sql_templates"
        
        # 创建必要的目录
        self._create_directories()
        
        # 初始化数据库连接
        if config:
            self._init_database_connection()
    
    def _create_directories(self):
        """创建必要的目录结构"""
        directories = [
            self.sql_files_dir,
            f"{self.sql_files_dir}/queries",
            f"{self.sql_files_dir}/schema",
            f"{self.sql_files_dir}/procedures",
            f"{self.sql_files_dir}/functions",
            self.datasets_dir,
            f"{self.datasets_dir}/csv",
            f"{self.datasets_dir}/json",
            f"{self.datasets_dir}/excel",
            self.templates_dir
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
        
        logger.info("✅ SQL管理器目录结构创建完成")
    
    def _init_database_connection(self):
        """初始化数据库连接"""
        try:
            self.mysql_manager = MySQLManager(self.config)
            if self.mysql_manager.setup_database():
                logger.info("✅ 数据库连接初始化成功")
            else:
                logger.warning("⚠️ 数据库连接初始化失败，将使用本地模式")
        except Exception as e:
            logger.error(f"❌ 数据库连接初始化失败: {str(e)}")
    
    def create_sql_file(self, filename: str, content: str, file_type: str = "queries") -> bool:
        """
        创建SQL文件
        
        Args:
            filename: 文件名
            content: SQL内容
            file_type: 文件类型 (queries, schema, procedures, functions)
            
        Returns:
            bool: 创建是否成功
        """
        try:
            if not filename.endswith('.sql'):
                filename += '.sql'
            
            file_path = os.path.join(self.sql_files_dir, file_type, filename)
            
            # 添加文件头注释
            header = f"""-- SQL文件: {filename}
-- 创建时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
-- 文件类型: {file_type}
-- 描述: 个性化SQL代码文件

"""
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(header + content)
            
            logger.info(f"✅ SQL文件创建成功: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"❌ SQL文件创建失败: {str(e)}")
            return False
    
    def list_sql_files(self, file_type: str = None) -> List[Dict[str, Any]]:
        """
        列出SQL文件
        
        Args:
            file_type: 文件类型筛选
            
        Returns:
            List[Dict]: SQL文件列表
        """
        sql_files = []
        
        try:
            if file_type:
                search_dirs = [os.path.join(self.sql_files_dir, file_type)]
            else:
                search_dirs = [
                    os.path.join(self.sql_files_dir, "queries"),
                    os.path.join(self.sql_files_dir, "schema"),
                    os.path.join(self.sql_files_dir, "procedures"),
                    os.path.join(self.sql_files_dir, "functions")
                ]
            
            for search_dir in search_dirs:
                if os.path.exists(search_dir):
                    for file in os.listdir(search_dir):
                        if file.endswith('.sql'):
                            file_path = os.path.join(search_dir, file)
                            file_stat = os.stat(file_path)
                            
                            sql_files.append({
                                'filename': file,
                                'path': file_path,
                                'type': os.path.basename(search_dir),
                                'size': file_stat.st_size,
                                'created': datetime.fromtimestamp(file_stat.st_ctime),
                                'modified': datetime.fromtimestamp(file_stat.st_mtime)
                            })
            
            return sorted(sql_files, key=lambda x: x['modified'], reverse=True)
            
        except Exception as e:
            logger.error(f"❌ 列出SQL文件失败: {str(e)}")
            return []
    
    def read_sql_file(self, filename: str, file_type: str = "queries") -> Optional[str]:
        """
        读取SQL文件内容
        
        Args:
            filename: 文件名
            file_type: 文件类型
            
        Returns:
            str: SQL文件内容
        """
        try:
            if not filename.endswith('.sql'):
                filename += '.sql'
            
            file_path = os.path.join(self.sql_files_dir, file_type, filename)
            
            if not os.path.exists(file_path):
                logger.error(f"❌ SQL文件不存在: {file_path}")
                return None
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            logger.info(f"✅ SQL文件读取成功: {file_path}")
            return content
            
        except Exception as e:
            logger.error(f"❌ SQL文件读取失败: {str(e)}")
            return None
    
    def execute_sql_file(self, filename: str, file_type: str = "queries", 
                        params: Dict[str, Any] = None) -> Tuple[bool, Any]:
        """
        执行SQL文件
        
        Args:
            filename: 文件名
            file_type: 文件类型
            params: SQL参数
            
        Returns:
            Tuple[bool, Any]: (是否成功, 结果数据)
        """
        try:
            # 读取SQL文件
            sql_content = self.read_sql_file(filename, file_type)
            if not sql_content:
                return False, "SQL文件读取失败"
            
            # 执行SQL
            return self.execute_sql(sql_content, params)
            
        except Exception as e:
            logger.error(f"❌ SQL文件执行失败: {str(e)}")
            return False, str(e)
    
    def execute_sql(self, sql_content: str, params: Dict[str, Any] = None) -> Tuple[bool, Any]:
        """
        执行SQL语句
        
        Args:
            sql_content: SQL内容
            params: SQL参数
            
        Returns:
            Tuple[bool, Any]: (是否成功, 结果数据)
        """
        try:
            if not self.mysql_manager:
                return False, "数据库连接未初始化"
            
            # 清理SQL语句
            sql_statements = self._split_sql_statements(sql_content)
            
            results = []
            engine = self.mysql_manager.db_config.engine
            
            for sql in sql_statements:
                if sql.strip():
                    # 判断是否为查询语句
                    if sql.strip().upper().startswith('SELECT'):
                        # 执行查询
                        df = pd.read_sql(sql, engine, params=params)
                        results.append({
                            'type': 'query',
                            'sql': sql,
                            'data': df,
                            'rows': len(df)
                        })
                    else:
                        # 执行其他语句
                        with engine.connect() as conn:
                            result = conn.execute(sql, params or {})
                            conn.commit()
                            results.append({
                                'type': 'execute',
                                'sql': sql,
                                'affected_rows': result.rowcount if hasattr(result, 'rowcount') else 0
                            })
            
            logger.info(f"✅ SQL执行成功，共执行 {len(results)} 条语句")
            return True, results
            
        except Exception as e:
            logger.error(f"❌ SQL执行失败: {str(e)}")
            return False, str(e)
    
    def _split_sql_statements(self, sql_content: str) -> List[str]:
        """
        分割SQL语句
        
        Args:
            sql_content: SQL内容
            
        Returns:
            List[str]: SQL语句列表
        """
        # 移除注释
        sql_content = re.sub(r'--.*?\n', '\n', sql_content)
        sql_content = re.sub(r'/\*.*?\*/', '', sql_content, flags=re.DOTALL)
        
        # 按分号分割
        statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
        
        return statements
    
    def create_dataset_template(self, template_name: str, table_structure: Dict[str, Any]) -> bool:
        """
        创建数据集模板
        
        Args:
            template_name: 模板名称
            table_structure: 表结构定义
            
        Returns:
            bool: 创建是否成功
        """
        try:
            template_file = os.path.join(self.templates_dir, f"{template_name}.json")
            
            template_data = {
                'name': template_name,
                'created_at': datetime.now().isoformat(),
                'description': f"个性化数据集模板: {template_name}",
                'structure': table_structure,
                'sample_data': self._generate_sample_data(table_structure)
            }
            
            with open(template_file, 'w', encoding='utf-8') as f:
                json.dump(template_data, f, ensure_ascii=False, indent=2)
            
            # 创建对应的SQL建表语句
            sql_content = self._generate_create_table_sql(template_name, table_structure)
            self.create_sql_file(f"create_{template_name}_table.sql", sql_content, "schema")
            
            logger.info(f"✅ 数据集模板创建成功: {template_file}")
            return True
            
        except Exception as e:
            logger.error(f"❌ 数据集模板创建失败: {str(e)}")
            return False
    
    def _generate_sample_data(self, table_structure: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        生成示例数据
        
        Args:
            table_structure: 表结构
            
        Returns:
            List[Dict]: 示例数据
        """
        sample_data = []
        
        for i in range(3):  # 生成3条示例数据
            row = {}
            for column, column_info in table_structure.items():
                column_type = column_info.get('type', 'VARCHAR').upper()
                
                if 'INT' in column_type:
                    row[column] = i + 1
                elif 'FLOAT' in column_type or 'DECIMAL' in column_type:
                    row[column] = round((i + 1) * 10.5, 2)
                elif 'DATE' in column_type:
                    row[column] = f"2024-01-{i+1:02d}"
                elif 'DATETIME' in column_type or 'TIMESTAMP' in column_type:
                    row[column] = f"2024-01-{i+1:02d} 10:00:00"
                else:
                    row[column] = f"示例数据_{i+1}"
            
            sample_data.append(row)
        
        return sample_data
    
    def _generate_create_table_sql(self, table_name: str, table_structure: Dict[str, Any]) -> str:
        """
        生成建表SQL语句
        
        Args:
            table_name: 表名
            table_structure: 表结构
            
        Returns:
            str: 建表SQL
        """
        sql_lines = [f"CREATE TABLE IF NOT EXISTS {table_name} ("]
        
        columns = []
        for column, column_info in table_structure.items():
            column_type = column_info.get('type', 'VARCHAR(255)')
            nullable = '' if column_info.get('nullable', True) else ' NOT NULL'
            default = f" DEFAULT '{column_info['default']}'" if 'default' in column_info else ''
            comment = f" COMMENT '{column_info['comment']}'" if 'comment' in column_info else ''
            
            column_def = f"  {column} {column_type}{nullable}{default}{comment}"
            columns.append(column_def)
        
        sql_lines.append(',\n'.join(columns))
        sql_lines.append(") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='个性化数据表';")
        
        return '\n'.join(sql_lines)
    
    def import_custom_dataset(self, file_path: str, table_name: str, 
                             mapping: Dict[str, str] = None) -> bool:
        """
        导入个性化数据集
        
        Args:
            file_path: 数据文件路径
            table_name: 目标表名
            mapping: 字段映射关系
            
        Returns:
            bool: 导入是否成功
        """
        try:
            # 检测文件类型并读取数据
            file_ext = os.path.splitext(file_path)[1].lower()
            
            if file_ext == '.csv':
                df = pd.read_csv(file_path, encoding='utf-8')
            elif file_ext == '.json':
                df = pd.read_json(file_path)
            elif file_ext in ['.xlsx', '.xls']:
                df = pd.read_excel(file_path)
            else:
                logger.error(f"❌ 不支持的文件格式: {file_ext}")
                return False
            
            # 应用字段映射
            if mapping:
                df = df.rename(columns=mapping)
            
            # 数据清洗和预处理
            df = self._preprocess_dataframe(df)
            
            # 导入到数据库
            if self.mysql_manager:
                engine = self.mysql_manager.db_config.engine
                df.to_sql(table_name, engine, if_exists='append', index=False)
                logger.info(f"✅ 数据导入成功: {len(df)} 行数据导入到表 {table_name}")
            else:
                # 保存到本地文件
                output_file = os.path.join(self.datasets_dir, f"{table_name}_imported.csv")
                df.to_csv(output_file, index=False, encoding='utf-8')
                logger.info(f"✅ 数据保存成功: {output_file}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ 数据导入失败: {str(e)}")
            return False
    
    def _preprocess_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        预处理DataFrame
        
        Args:
            df: 原始DataFrame
            
        Returns:
            pd.DataFrame: 预处理后的DataFrame
        """
        # 处理空值
        df = df.fillna('')
        
        # 处理列名（移除特殊字符）
        df.columns = [re.sub(r'[^\w\u4e00-\u9fff]', '_', col) for col in df.columns]
        
        # 添加导入时间戳
        df['imported_at'] = datetime.now()
        
        return df
    
    def generate_sql_templates(self):
        """生成常用SQL模板"""
        templates = {
            'basic_select.sql': """-- 基础查询模板
SELECT 
    column1,
    column2,
    COUNT(*) as count
FROM your_table_name
WHERE condition = 'value'
GROUP BY column1, column2
ORDER BY count DESC
LIMIT 10;""",
            
            'data_analysis.sql': """-- 数据分析模板
SELECT 
    DATE(date_column) as analysis_date,
    category,
    SUM(amount) as total_amount,
    AVG(amount) as avg_amount,
    COUNT(*) as record_count
FROM your_table_name
WHERE date_column >= '2024-01-01'
GROUP BY DATE(date_column), category
ORDER BY analysis_date DESC, total_amount DESC;""",
            
            'join_query.sql': """-- 关联查询模板
SELECT 
    a.id,
    a.name,
    b.category,
    b.value
FROM table_a a
LEFT JOIN table_b b ON a.id = b.foreign_key
WHERE a.status = 'active'
ORDER BY a.name;""",
            
            'create_index.sql': """-- 创建索引模板
-- 为提高查询性能创建索引
CREATE INDEX idx_table_column ON your_table_name(column_name);
CREATE INDEX idx_table_multi ON your_table_name(column1, column2);""",
            
            'data_validation.sql': """-- 数据验证模板
-- 检查数据质量
SELECT 
    'total_records' as metric,
    COUNT(*) as value
FROM your_table_name

UNION ALL

SELECT 
    'null_values' as metric,
    COUNT(*) as value
FROM your_table_name
WHERE important_column IS NULL

UNION ALL

SELECT 
    'duplicate_records' as metric,
    COUNT(*) - COUNT(DISTINCT unique_column) as value
FROM your_table_name;"""
        }
        
        for filename, content in templates.items():
            self.create_sql_file(filename, content, "queries")
        
        logger.info("✅ SQL模板生成完成")
    
    def export_query_results(self, sql_content: str, output_file: str, 
                           file_format: str = 'csv') -> bool:
        """
        导出查询结果
        
        Args:
            sql_content: SQL查询语句
            output_file: 输出文件路径
            file_format: 输出格式 (csv, json, excel)
            
        Returns:
            bool: 导出是否成功
        """
        try:
            success, results = self.execute_sql(sql_content)
            
            if not success:
                logger.error(f"❌ SQL查询失败: {results}")
                return False
            
            # 找到查询结果
            query_result = None
            for result in results:
                if result['type'] == 'query' and 'data' in result:
                    query_result = result['data']
                    break
            
            if query_result is None:
                logger.error("❌ 没有找到查询结果")
                return False
            
            # 导出数据
            if file_format.lower() == 'csv':
                query_result.to_csv(output_file, index=False, encoding='utf-8')
            elif file_format.lower() == 'json':
                query_result.to_json(output_file, orient='records', ensure_ascii=False, indent=2)
            elif file_format.lower() in ['xlsx', 'excel']:
                query_result.to_excel(output_file, index=False)
            else:
                logger.error(f"❌ 不支持的导出格式: {file_format}")
                return False
            
            logger.info(f"✅ 查询结果导出成功: {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"❌ 查询结果导出失败: {str(e)}")
            return False


def interactive_sql_manager():
    """交互式SQL管理器"""
    print("🔧 SQL代码管理器")
    print("=" * 50)
    
    # 获取数据库配置
    config_file = input("MySQL配置文件路径 (默认: src/config/mysql_config.json): ") or "src/config/mysql_config.json"
    
    config = None
    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        if config.get('password') == '***':
            password = input("请输入MySQL密码: ")
            config['password'] = password
    else:
        print("⚠️ 配置文件不存在，将在本地模式下运行")
    
    # 创建SQL管理器
    sql_manager = SQLManager(config)
    
    # 生成SQL模板
    sql_manager.generate_sql_templates()
    
    while True:
        print("\n📋 SQL管理器菜单:")
        print("1. 创建SQL文件")
        print("2. 列出SQL文件")
        print("3. 执行SQL文件")
        print("4. 导入个性化数据集")
        print("5. 创建数据集模板")
        print("6. 导出查询结果")
        print("7. 退出")
        
        choice = input("请选择操作 (1-7): ").strip()
        
        if choice == '1':
            # 创建SQL文件
            filename = input("SQL文件名: ")
            file_type = input("文件类型 (queries/schema/procedures/functions): ") or "queries"
            print("请输入SQL内容 (输入'END'结束):")
            
            lines = []
            while True:
                line = input()
                if line.strip() == 'END':
                    break
                lines.append(line)
            
            content = '\n'.join(lines)
            sql_manager.create_sql_file(filename, content, file_type)
        
        elif choice == '2':
            # 列出SQL文件
            files = sql_manager.list_sql_files()
            if files:
                print("\n📁 SQL文件列表:")
                for file in files:
                    print(f"  - {file['filename']} ({file['type']}) - {file['modified']}")
            else:
                print("📭 没有找到SQL文件")
        
        elif choice == '3':
            # 执行SQL文件
            filename = input("SQL文件名: ")
            file_type = input("文件类型 (queries/schema/procedures/functions): ") or "queries"
            
            success, results = sql_manager.execute_sql_file(filename, file_type)
            
            if success:
                print("✅ SQL执行成功:")
                for result in results:
                    if result['type'] == 'query':
                        print(f"  查询结果: {result['rows']} 行数据")
                        print(result['data'].head())
                    else:
                        print(f"  执行结果: 影响 {result['affected_rows']} 行")
            else:
                print(f"❌ SQL执行失败: {results}")
        
        elif choice == '4':
            # 导入个性化数据集
            file_path = input("数据文件路径: ")
            table_name = input("目标表名: ")
            
            if sql_manager.import_custom_dataset(file_path, table_name):
                print("✅ 数据导入成功")
            else:
                print("❌ 数据导入失败")
        
        elif choice == '5':
            # 创建数据集模板
            template_name = input("模板名称: ")
            print("请定义表结构 (格式: 列名:类型:注释，输入'END'结束):")
            
            structure = {}
            while True:
                line = input().strip()
                if line == 'END':
                    break
                
                if ':' in line:
                    parts = line.split(':')
                    column_name = parts[0].strip()
                    column_type = parts[1].strip() if len(parts) > 1 else 'VARCHAR(255)'
                    comment = parts[2].strip() if len(parts) > 2 else ''
                    
                    structure[column_name] = {
                        'type': column_type,
                        'comment': comment,
                        'nullable': True
                    }
            
            if structure:
                sql_manager.create_dataset_template(template_name, structure)
                print("✅ 数据集模板创建成功")
            else:
                print("❌ 表结构定义为空")
        
        elif choice == '6':
            # 导出查询结果
            print("请输入SQL查询语句 (输入'END'结束):")
            lines = []
            while True:
                line = input()
                if line.strip() == 'END':
                    break
                lines.append(line)
            
            sql_content = '\n'.join(lines)
            output_file = input("输出文件路径: ")
            file_format = input("输出格式 (csv/json/excel): ") or "csv"
            
            if sql_manager.export_query_results(sql_content, output_file, file_format):
                print("✅ 查询结果导出成功")
            else:
                print("❌ 查询结果导出失败")
        
        elif choice == '7':
            print("👋 感谢使用SQL管理器")
            break
        
        else:
            print("❌ 无效选择，请重试")


if __name__ == "__main__":
    interactive_sql_manager()