import os
import sys
import logging
from datetime import datetime
from pathlib import Path
import argparse
from typing import Optional

from src.main import AnalysisReportSystem

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('analysis_report.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def setup_directories() -> None:
    """创建必要的目录"""
    directories = ['data', 'output/charts', 'output/reports']
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        logger.info(f"创建目录: {directory}")

def validate_input_file(input_file: str) -> bool:
    """
    验证输入文件
    
    Args:
        input_file: 输入文件路径
        
    Returns:
        文件是否有效
    """
    if not os.path.exists(input_file):
        logger.error(f"输入文件不存在: {input_file}")
        return False
        
    if not input_file.endswith('.csv'):
        logger.error("输入文件必须是CSV格式")
        return False
        
    return True

def main(input_file: Optional[str] = None, output_dir: Optional[str] = None) -> None:
    """
    运行分析报告系统
    
    Args:
        input_file: 输入文件路径，默认为data/example_data.csv
        output_dir: 输出目录路径，默认为output
    """
    try:
        # 获取当前目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 设置默认值
        if input_file is None:
            input_file = os.path.join(current_dir, 'data', 'example_data.csv')
        if output_dir is None:
            output_dir = os.path.join(current_dir, 'output')
            
        # 创建必要的目录
        setup_directories()
        
        # 验证输入文件
        if not validate_input_file(input_file):
            sys.exit(1)
            
        # 创建系统实例
        system = AnalysisReportSystem(input_file, output_dir)
        
        # 生成报告
        report_date = datetime.now().strftime('%Y-%m-%d')
        output_paths = system.generate_report(report_date)
        
        # 打印输出路径
        print("\n生成的报告文件：")
        print("=" * 50)
        for format_name, path in output_paths['reports'].items():
            print(f"{format_name.upper()}格式报告：{path}")
        
        print("\n生成的图表文件：")
        print("=" * 50)
        for chart_name, path in output_paths['charts'].items():
            print(f"{chart_name}：{path}")
            
        logger.info("系统运行完成")
        
    except Exception as e:
        logger.error(f"系统运行失败: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='运行分析报告系统')
    parser.add_argument('--input', help='输入数据文件路径')
    parser.add_argument('--output', help='输出目录路径')
    args = parser.parse_args()
    
    # 运行系统
    main(args.input, args.output) 