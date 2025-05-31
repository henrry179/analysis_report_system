# 条件导入，优雅处理缺失依赖
try:
    import pandas as pd
    import numpy as np
    PANDAS_AVAILABLE = True
    NUMPY_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    NUMPY_AVAILABLE = False
    print("⚠️  警告: pandas/numpy 未安装，分析功能将使用简化模式")

from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class GMVMetrics:
    """GMV相关指标"""
    current: float
    previous: float
    change_rate: float
    contribution: float

@dataclass
class CategoryMetrics:
    """品类相关指标"""
    name: str
    current_price: float
    previous_price: float
    change_rate: float
    current_share: float
    previous_share: float
    structure_change: float
    contribution: float

@dataclass
class RegionMetrics:
    """区域相关指标"""
    name: str
    current_price: float
    previous_price: float
    change_value: float
    change_rate: float
    current_rate: float
    previous_rate: float

@dataclass
class AnalysisResult:
    """分析结果数据类"""
    gmv_metrics: Dict
    category_analysis: Any  # 可能是DataFrame或dict
    region_analysis: Any    # 可能是DataFrame或dict
    main_issues: List[Dict]
    recommendations: List[str]

# 简化数据处理类，替代pandas功能
class SimpleDataProcessor:
    """简化的数据处理器"""
    
    @staticmethod
    def group_by(data: List[Dict], group_key: str) -> Dict[str, List[Dict]]:
        """按指定键分组"""
        groups = {}
        for item in data:
            key = item.get(group_key)
            if key not in groups:
                groups[key] = []
            groups[key].append(item)
        return groups
    
    @staticmethod
    def sum_column(data: List[Dict], column: str) -> float:
        """计算列的总和"""
        return sum(item.get(column, 0) for item in data)
    
    @staticmethod
    def mean_column(data: List[Dict], column: str) -> float:
        """计算列的平均值"""
        values = [item.get(column, 0) for item in data]
        return sum(values) / len(values) if values else 0
    
    @staticmethod
    def to_dict_list(data) -> List[Dict]:
        """将pandas DataFrame转换为字典列表"""
        if PANDAS_AVAILABLE and hasattr(data, 'to_dict'):
            return data.to_dict('records')
        elif hasattr(data, 'data'):
            return data.data if isinstance(data.data, list) else []
        else:
            return data if isinstance(data, list) else []

class MetricsAnalyzer:
    """指标分析类，负责数据分析和洞察生成"""
    
    def __init__(self, current_data: Any, previous_data: Any):
        """
        初始化指标分析器
        
        Args:
            current_data: 当前期数据（可能是DataFrame或模拟对象）
            previous_data: 上期数据（可能是DataFrame或模拟对象）
        """
        self.current_data = current_data
        self.previous_data = previous_data
        self.processor = SimpleDataProcessor()
        
        # 将数据转换为统一格式
        self.current_dict_list = self.processor.to_dict_list(current_data)
        self.previous_dict_list = self.processor.to_dict_list(previous_data)
        
    def calculate_gmv_metrics(self) -> Dict[str, GMVMetrics]:
        """
        计算GMV相关指标（支持简化模式）
        
        Returns:
            GMV相关指标字典
        """
        metrics = {}
        
        # 使用简化处理器或pandas
        if PANDAS_AVAILABLE and hasattr(self.current_data, 'sum'):
            # pandas模式
            current_gmv = self.current_data['gmv'].sum()
            previous_gmv = self.previous_data['gmv'].sum()
            current_dau = self.current_data['dau'].sum()
            previous_dau = self.previous_data['dau'].sum()
            current_frequency = self.current_data['frequency'].mean()
            previous_frequency = self.previous_data['frequency'].mean()
            current_order_price = self.current_data['order_price'].mean()
            previous_order_price = self.previous_data['order_price'].mean()
            current_conversion_rate = self.current_data['conversion_rate'].mean()
            previous_conversion_rate = self.previous_data['conversion_rate'].mean()
        else:
            # 简化模式
            current_gmv = self.processor.sum_column(self.current_dict_list, 'gmv')
            previous_gmv = self.processor.sum_column(self.previous_dict_list, 'gmv')
            current_dau = self.processor.sum_column(self.current_dict_list, 'dau')
            previous_dau = self.processor.sum_column(self.previous_dict_list, 'dau')
            current_frequency = self.processor.mean_column(self.current_dict_list, 'frequency')
            previous_frequency = self.processor.mean_column(self.previous_dict_list, 'frequency')
            current_order_price = self.processor.mean_column(self.current_dict_list, 'order_price')
            previous_order_price = self.processor.mean_column(self.previous_dict_list, 'order_price')
            current_conversion_rate = self.processor.mean_column(self.current_dict_list, 'conversion_rate')
            previous_conversion_rate = self.processor.mean_column(self.previous_dict_list, 'conversion_rate')
        
        # 安全的除法运算
        def safe_divide(a, b):
            return (a / b * 100) if b != 0 else 0
        
        gmv_change_rate = safe_divide(current_gmv - previous_gmv, previous_gmv)
        
        metrics['gmv'] = GMVMetrics(
            current=current_gmv,
            previous=previous_gmv,
            change_rate=gmv_change_rate,
            contribution=100.0
        )
        
        dau_change_rate = safe_divide(current_dau - previous_dau, previous_dau)
        metrics['dau'] = GMVMetrics(
            current=current_dau,
            previous=previous_dau,
            change_rate=dau_change_rate,
            contribution=safe_divide(dau_change_rate, gmv_change_rate) * 100 if gmv_change_rate != 0 else 0
        )
        
        frequency_change_rate = safe_divide(current_frequency - previous_frequency, previous_frequency)
        metrics['frequency'] = GMVMetrics(
            current=current_frequency,
            previous=previous_frequency,
            change_rate=frequency_change_rate,
            contribution=safe_divide(frequency_change_rate, gmv_change_rate) * 100 if gmv_change_rate != 0 else 0
        )
        
        order_price_change_rate = safe_divide(current_order_price - previous_order_price, previous_order_price)
        metrics['order_price'] = GMVMetrics(
            current=current_order_price,
            previous=previous_order_price,
            change_rate=order_price_change_rate,
            contribution=safe_divide(order_price_change_rate, gmv_change_rate) * 100 if gmv_change_rate != 0 else 0
        )
        
        conversion_rate_change = safe_divide(current_conversion_rate - previous_conversion_rate, previous_conversion_rate)
        metrics['conversion_rate'] = GMVMetrics(
            current=current_conversion_rate,
            previous=previous_conversion_rate,
            change_rate=conversion_rate_change,
            contribution=safe_divide(conversion_rate_change, gmv_change_rate) * 100 if gmv_change_rate != 0 else 0
        )
        
        return metrics
    
    def calculate_category_metrics(self) -> List[CategoryMetrics]:
        """
        计算品类相关指标（支持简化模式）
        
        Returns:
            品类指标列表
        """
        metrics = []
        
        if PANDAS_AVAILABLE and hasattr(self.current_data, 'groupby'):
            # pandas模式
            current_by_category = self.current_data.groupby('category')
            previous_by_category = self.previous_data.groupby('category')
            
            for category in current_by_category.groups:
                if category in previous_by_category.groups:
                    current = current_by_category.get_group(category)
                    previous = previous_by_category.get_group(category)
                    
                    # 计算笔单价
                    current_price = current['order_price'].mean()
                    previous_price = previous['order_price'].mean()
                    change_rate = ((current_price - previous_price) / previous_price * 100) if previous_price != 0 else 0
                    
                    # 计算销售占比
                    current_share = current['gmv'].sum() / self.current_data['gmv'].sum() * 100
                    previous_share = previous['gmv'].sum() / self.previous_data['gmv'].sum() * 100
                    structure_change = ((current_share - previous_share) / previous_share * 100) if previous_share != 0 else 0
                    
                    # 计算贡献度
                    contribution = (change_rate * current_share) / 100
                    
                    metrics.append(CategoryMetrics(
                        name=category,
                        current_price=current_price,
                        previous_price=previous_price,
                        change_rate=change_rate,
                        current_share=current_share,
                        previous_share=previous_share,
                        structure_change=structure_change,
                        contribution=contribution
                    ))
        else:
            # 简化模式
            current_groups = self.processor.group_by(self.current_dict_list, 'category')
            previous_groups = self.processor.group_by(self.previous_dict_list, 'category')
            
            current_total_gmv = self.processor.sum_column(self.current_dict_list, 'gmv')
            previous_total_gmv = self.processor.sum_column(self.previous_dict_list, 'gmv')
            
            for category in current_groups:
                if category in previous_groups:
                    current_data = current_groups[category]
                    previous_data = previous_groups[category]
                    
                    # 计算笔单价
                    current_price = self.processor.mean_column(current_data, 'order_price')
                    previous_price = self.processor.mean_column(previous_data, 'order_price')
                    change_rate = ((current_price - previous_price) / previous_price * 100) if previous_price != 0 else 0
                    
                    # 计算销售占比
                    current_gmv = self.processor.sum_column(current_data, 'gmv')
                    previous_gmv = self.processor.sum_column(previous_data, 'gmv')
                    current_share = (current_gmv / current_total_gmv * 100) if current_total_gmv != 0 else 0
                    previous_share = (previous_gmv / previous_total_gmv * 100) if previous_total_gmv != 0 else 0
                    structure_change = ((current_share - previous_share) / previous_share * 100) if previous_share != 0 else 0
                    
                    # 计算贡献度
                    contribution = (change_rate * current_share) / 100
                    
                    metrics.append(CategoryMetrics(
                        name=category,
                        current_price=current_price,
                        previous_price=previous_price,
                        change_rate=change_rate,
                        current_share=current_share,
                        previous_share=previous_share,
                        structure_change=structure_change,
                        contribution=contribution
                    ))
        
        return metrics
    
    def calculate_region_metrics(self) -> List[RegionMetrics]:
        """
        计算区域相关指标（支持简化模式）
        
        Returns:
            区域指标列表
        """
        metrics = []
        
        if PANDAS_AVAILABLE and hasattr(self.current_data, 'groupby'):
            # pandas模式
            current_by_region = self.current_data.groupby('region')
            previous_by_region = self.previous_data.groupby('region')
            
            for region in current_by_region.groups:
                if region in previous_by_region.groups:
                    current = current_by_region.get_group(region)
                    previous = previous_by_region.get_group(region)
                    
                    # 计算笔单价
                    current_price = current['order_price'].mean()
                    previous_price = previous['order_price'].mean()
                    change_value = current_price - previous_price
                    change_rate = (change_value / previous_price * 100) if previous_price != 0 else 0
                    
                    # 计算转化率
                    current_rate = current['conversion_rate'].mean()
                    previous_rate = previous['conversion_rate'].mean()
                    
                    metrics.append(RegionMetrics(
                        name=region,
                        current_price=current_price,
                        previous_price=previous_price,
                        change_value=change_value,
                        change_rate=change_rate,
                        current_rate=current_rate,
                        previous_rate=previous_rate
                    ))
        else:
            # 简化模式
            current_groups = self.processor.group_by(self.current_dict_list, 'region')
            previous_groups = self.processor.group_by(self.previous_dict_list, 'region')
            
            for region in current_groups:
                if region in previous_groups:
                    current_data = current_groups[region]
                    previous_data = previous_groups[region]
                    
                    # 计算笔单价
                    current_price = self.processor.mean_column(current_data, 'order_price')
                    previous_price = self.processor.mean_column(previous_data, 'order_price')
                    change_value = current_price - previous_price
                    change_rate = (change_value / previous_price * 100) if previous_price != 0 else 0
                    
                    # 计算转化率
                    current_rate = self.processor.mean_column(current_data, 'conversion_rate')
                    previous_rate = self.processor.mean_column(previous_data, 'conversion_rate')
                    
                    metrics.append(RegionMetrics(
                        name=region,
                        current_price=current_price,
                        previous_price=previous_price,
                        change_value=change_value,
                        change_rate=change_rate,
                        current_rate=current_rate,
                        previous_rate=previous_rate
                    ))
        
        return metrics
    
    def calculate_gini_coefficient(self, data) -> float:
        """
        计算基尼系数（支持简化模式）
        
        Args:
            data: 数据序列或列表
            
        Returns:
            基尼系数
        """
        if NUMPY_AVAILABLE and hasattr(data, 'values'):
            # numpy模式
            sorted_data = np.sort(data.values if hasattr(data, 'values') else data)
            n = len(sorted_data)
            if n == 0:
                return 0.0
            index = np.arange(1, n + 1) / n
            return ((2 * index - n - 1) * sorted_data).sum() / (n * sorted_data.sum())
        else:
            # 简化模式
            if isinstance(data, (list, tuple)):
                sorted_data = sorted(data)
            else:
                # 假设是某种可迭代对象
                try:
                    sorted_data = sorted(list(data))
                except:
                    return 0.0
            
            n = len(sorted_data)
            if n == 0 or sum(sorted_data) == 0:
                return 0.0
            
            # 简化的基尼系数计算
            cumsum = 0
            for i, val in enumerate(sorted_data):
                cumsum += (2 * (i + 1) - n - 1) * val
            
            return cumsum / (n * sum(sorted_data))
    
    def identify_top_declining_categories(self, metrics: List[CategoryMetrics], top_n: int = 3) -> List[Dict]:
        """
        识别下降最显著的品类
        
        Args:
            metrics: 品类指标列表
            top_n: 返回前N个品类
            
        Returns:
            下降最显著的品类列表
        """
        declining = sorted(
            [m for m in metrics if m.change_rate < 0],
            key=lambda x: x.change_rate
        )[:top_n]
        
        return [
            {
                'name': m.name,
                'decline_rate': f"{m.change_rate:.2f}"
            }
            for m in declining
        ]
    
    def identify_top_declining_regions(self, metrics: List[RegionMetrics], top_n: int = 3) -> List[Dict]:
        """
        识别下降最显著的区域
        
        Args:
            metrics: 区域指标列表
            top_n: 返回前N个区域
            
        Returns:
            下降最显著的区域列表
        """
        declining = sorted(
            [m for m in metrics if m.change_rate < 0],
            key=lambda x: x.change_rate
        )[:top_n]
        
        return [
            {
                'name': m.name,
                'decline_rate': f"{m.change_rate:.2f}"
            }
            for m in declining
        ]
    
    def generate_improvement_suggestions(self, metrics: Dict[str, GMVMetrics]) -> List[str]:
        """
        生成改进建议
        
        Args:
            metrics: GMV相关指标
            
        Returns:
            改进建议列表
        """
        suggestions = []
        
        # 基于笔单价分析
        if metrics['order_price'].change_rate < 0:
            suggestions.append(
                f"针对笔单价下降{abs(metrics['order_price'].change_rate):.2f}%的情况，"
                "建议分析价格下降原因，评估促销策略影响"
            )
        
        # 基于转化率分析
        if metrics['conversion_rate'].change_rate < 0:
            suggestions.append(
                f"针对转化率下降{abs(metrics['conversion_rate'].change_rate):.2f}%的情况，"
                "建议优化用户转化路径，提升转化率"
            )
        
        return suggestions
    
    def analyze(self) -> Dict:
        """
        执行完整分析（支持简化模式）
        
        Returns:
            分析结果字典
        """
        # 计算各项指标
        gmv_metrics = self.calculate_gmv_metrics()
        category_metrics = self.calculate_category_metrics()
        region_metrics = self.calculate_region_metrics()
        
        # 计算基尼系数
        if PANDAS_AVAILABLE and hasattr(self.current_data, 'groupby'):
            # pandas模式
            category_prices = self.current_data.groupby('category')['order_price'].mean()
            region_prices = self.current_data.groupby('region')['order_price'].mean()
            category_gini = self.calculate_gini_coefficient(category_prices)
            region_gini = self.calculate_gini_coefficient(region_prices)
        else:
            # 简化模式
            category_groups = self.processor.group_by(self.current_dict_list, 'category')
            region_groups = self.processor.group_by(self.current_dict_list, 'region')
            
            category_prices = [
                self.processor.mean_column(data, 'order_price') 
                for data in category_groups.values()
            ]
            region_prices = [
                self.processor.mean_column(data, 'order_price') 
                for data in region_groups.values()
            ]
            
            category_gini = self.calculate_gini_coefficient(category_prices)
            region_gini = self.calculate_gini_coefficient(region_prices)
        
        # 识别主要问题
        top_declining_categories = self.identify_top_declining_categories(category_metrics)
        top_declining_regions = self.identify_top_declining_regions(region_metrics)
        
        # 生成改进建议
        improvement_suggestions = self.generate_improvement_suggestions(gmv_metrics)
        
        return {
            'gmv_metrics': gmv_metrics,
            'category_metrics': category_metrics,
            'region_metrics': region_metrics,
            'category_gini': category_gini,
            'region_gini': region_gini,
            'top_declining_categories': top_declining_categories,
            'top_declining_regions': top_declining_regions,
            'improvement_suggestions': improvement_suggestions
        } 