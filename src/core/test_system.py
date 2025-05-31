import os
import logging
from pathlib import Path
from datetime import datetime

from data.data_collector import CSVDataCollector
from data.cache_manager import CacheManager
from analysis.metrics_analyzer import MetricsAnalyzer
from visualization.chart_generator import ChartGenerator
from report.report_generator import ReportGenerator

def setup_logging():
    """配置日志"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / "analysis_report.log"),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def main():
    """主函数"""
    logger = setup_logging()
    logger.info("开始运行分析报告系统")
    
    try:
        # 创建输出目录
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        # 初始化缓存管理器
        cache_manager = CacheManager(cache_dir="cache")
        
        # 初始化数据采集器
        collector = CSVDataCollector(
            config={"file_path": "data/input.csv"},
            cache_manager=cache_manager
        )
        
        # 采集数据
        logger.info("开始数据采集")
        data = collector.collect_with_cache(use_cache=True, incremental=True)
        logger.info(f"成功采集{len(data)}条数据")
        
        # 初始化分析器
        analyzer = MetricsAnalyzer(data)
        
        # 执行分析
        logger.info("开始数据分析")
        analysis_result = analyzer.analyze()
        logger.info("数据分析完成")
        
        # 初始化图表生成器
        chart_generator = ChartGenerator(str(output_dir / "charts"))
        
        # 生成图表
        logger.info("开始生成图表")
        chart_paths = {
            'gmv_contribution': chart_generator.generate_gmv_contribution_chart(
                analysis_result.gmv_metrics,
                analyzer.analyze_contribution(analysis_result.gmv_metrics)
            ),
            'category_analysis': chart_generator.generate_category_analysis_chart(
                analysis_result.category_analysis
            ),
            'region_analysis': chart_generator.generate_region_analysis_chart(
                analysis_result.region_analysis
            )
        }
        logger.info("图表生成完成")
        
        # 初始化报告生成器
        report_generator = ReportGenerator(
            template_dir="templates",
            output_dir=str(output_dir / "reports")
        )
        
        # 生成报告
        logger.info("开始生成报告")
        report_paths = report_generator.generate_all_formats(
            analysis_result.__dict__,
            chart_paths,
            datetime.now()
        )
        logger.info(f"报告生成完成: {report_paths}")
        
    except Exception as e:
        logger.error(f"系统运行失败: {str(e)}", exc_info=True)
        raise
    
    logger.info("系统运行完成")

if __name__ == "__main__":
    main() 