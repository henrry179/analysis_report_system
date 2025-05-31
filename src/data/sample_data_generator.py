#!/usr/bin/env python3
"""
样本数据生成器
基于零售业务场景生成虚拟数据集
参考华东区分析报告格式设计
"""

import random
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path

# 条件导入
try:
    import pandas as pd
    import numpy as np
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

class SampleDataGenerator:
    """样本数据生成器"""
    
    def __init__(self):
        # 零售业务基础配置
        self.config = {
            'regions': ['华东一区', '华东二区', '华东三区'],
            'categories': ['肉禽蛋类', '水产类', '猪肉类', '冷藏及加工类', '蔬菜类', '水果类'],
            'store_types': ['标准店', '大店', '小店', '社区店'],
            'channels': ['线下门店', '线上销售', '批发渠道'],
            'time_periods': ['2024-01', '2024-02', '2024-03', '2024-04'],
            'base_metrics': {
                'gmv_range': (800000, 1200000),  # 单店月GMV范围
                'gross_profit_rate_range': (20.0, 30.0),  # 毛利率范围
                'discount_rate_range': (8.0, 12.0),  # 折扣率范围
                'promotion_rate_range': (12.0, 18.0),  # 促销率范围
                'dau_range': (150, 350),  # 日活用户范围
                'conversion_rate_range': (2.5, 4.5),  # 转化率范围
                'avg_order_value_range': (180, 280),  # 客单价范围
                'frequency_range': (1.8, 3.2)  # 购买频次范围
            }
        }
        
        # 区域权重（华东一区表现最好）
        self.region_weights = {
            '华东一区': 1.15,  # 15%高于平均
            '华东二区': 1.05,  # 5%高于平均
            '华东三区': 0.85   # 15%低于平均（但增长最快）
        }
        
        # 品类权重（不同品类表现差异）
        self.category_weights = {
            '肉禽蛋类': 1.20,      # 表现最佳
            '冷藏及加工类': 1.15,   # 高潜力
            '水果类': 1.10,        # 高价值
            '蔬菜类': 1.00,        # 稳定
            '水产类': 0.85,        # 下降
            '猪肉类': 0.80         # 需要关注
        }
        
        # 季节性因子
        self.seasonal_factors = {
            '2024-01': 0.95,  # 一月稍低
            '2024-02': 0.90,  # 二月春节影响
            '2024-03': 1.10,  # 三月回升
            '2024-04': 1.05   # 四月稳定
        }
        
    def generate_sample_data(self, num_records: int = 1000) -> Any:
        """生成样本数据"""
        
        if PANDAS_AVAILABLE:
            return self._generate_pandas_data(num_records)
        else:
            return self._generate_simple_data(num_records)
    
    def _generate_pandas_data(self, num_records: int):
        """使用pandas生成结构化数据"""
        
        if not PANDAS_AVAILABLE:
            # 如果pandas不可用，使用简化数据结构
            return self._generate_simple_data(num_records)
        
        data_records = []
        
        for i in range(num_records):
            # 随机选择基础属性
            region = random.choice(self.config['regions'])
            category = random.choice(self.config['categories'])
            store_type = random.choice(self.config['store_types'])
            channel = random.choice(self.config['channels'])
            period = random.choice(self.config['time_periods'])
            
            # 生成店铺ID
            store_id = f"ST{region[-1]}{random.randint(1000, 9999)}"
            
            # 基础日期
            base_date = datetime(2024, int(period.split('-')[1]), random.randint(1, 28))
            
            # 计算权重调整
            region_factor = self.region_weights.get(region, 1.0)
            category_factor = self.category_weights.get(category, 1.0)
            seasonal_factor = self.seasonal_factors.get(period, 1.0)
            total_factor = region_factor * category_factor * seasonal_factor
            
            # 生成核心指标
            base_gmv = random.uniform(*self.config['base_metrics']['gmv_range'])
            gmv = base_gmv * total_factor * random.uniform(0.8, 1.2)
            
            gross_profit_rate = random.uniform(*self.config['base_metrics']['gross_profit_rate_range'])
            # 华东一区毛利率更高
            if region == '华东一区':
                gross_profit_rate *= 1.05
            elif region == '华东三区':
                gross_profit_rate *= 0.98
                
            discount_rate = random.uniform(*self.config['base_metrics']['discount_rate_range'])
            # 华东一区折扣控制更好
            if region == '华东一区':
                discount_rate *= 0.95
                
            promotion_rate = random.uniform(*self.config['base_metrics']['promotion_rate_range'])
            
            dau = int(random.uniform(*self.config['base_metrics']['dau_range']) * region_factor)
            conversion_rate = random.uniform(*self.config['base_metrics']['conversion_rate_range'])
            avg_order_value = random.uniform(*self.config['base_metrics']['avg_order_value_range'])
            frequency = random.uniform(*self.config['base_metrics']['frequency_range'])
            
            # 计算衍生指标
            total_orders = int(dau * conversion_rate / 100)
            total_customers = int(dau * 0.7)  # 70%的DAU是付费用户
            sales_per_sqm = gmv / random.uniform(800, 1200)  # 假设店铺面积
            
            # 库存和供应链指标
            inventory_turnover = random.uniform(8, 15)
            supply_chain_score = random.uniform(75, 95)
            customer_satisfaction = random.uniform(80, 95)
            
            # 竞争和市场指标
            market_share = random.uniform(8, 25)
            competitor_count = random.randint(3, 8)
            
            record = {
                # 基础信息
                'date': base_date.strftime('%Y-%m-%d'),
                'period': period,
                'store_id': store_id,
                'region': region,
                'category': category,
                'store_type': store_type,
                'channel': channel,
                
                # 核心财务指标
                'gmv': round(gmv, 2),
                'gross_profit_rate': round(gross_profit_rate, 2),
                'discount_rate': round(discount_rate, 2),
                'promotion_rate': round(promotion_rate, 2),
                'net_profit_rate': round(gross_profit_rate - discount_rate - 5, 2),
                
                # 用户和交易指标
                'dau': dau,
                'total_customers': total_customers,
                'total_orders': total_orders,
                'conversion_rate': round(conversion_rate, 2),
                'avg_order_value': round(avg_order_value, 2),
                'frequency': round(frequency, 2),
                
                # 运营效率指标
                'sales_per_sqm': round(sales_per_sqm, 2),
                'inventory_turnover': round(inventory_turnover, 2),
                'supply_chain_score': round(supply_chain_score, 1),
                'customer_satisfaction': round(customer_satisfaction, 1),
                
                # 市场和竞争指标
                'market_share': round(market_share, 2),
                'competitor_count': competitor_count,
                
                # 辅助计算字段
                'total_transaction_value': round(total_orders * avg_order_value, 2),
                'profit_amount': round(gmv * gross_profit_rate / 100, 2),
                'discount_amount': round(gmv * discount_rate / 100, 2),
                'promotion_amount': round(gmv * promotion_rate / 100, 2)
            }
            
            data_records.append(record)
        
        try:
            df = pd.DataFrame(data_records)
            
            # 添加一些数据质量特征（模拟真实数据）
            # 随机添加一些空值
            null_columns = ['customer_satisfaction', 'supply_chain_score', 'market_share']
            for col in null_columns:
                null_indices = np.random.choice(df.index, size=int(len(df) * 0.05), replace=False)
                df.loc[null_indices, col] = np.nan
            
            # 添加一些异常值
            outlier_indices = np.random.choice(df.index, size=int(len(df) * 0.02), replace=False)
            df.loc[outlier_indices, 'gmv'] *= random.uniform(2.0, 3.0)
            
            return df
        except ImportError:
            # 如果pandas仍然不可用，返回字典格式
            return {
                'data': data_records,
                'summary': {
                    'total_records': len(data_records),
                    'regions': self.config['regions'],
                    'categories': self.config['categories'],
                    'time_periods': self.config['time_periods']
                }
            }
    
    def _generate_simple_data(self, num_records: int) -> Dict[str, Any]:
        """生成简化数据结构"""
        
        data = {
            'data': [],
            'summary': {
                'total_records': num_records,
                'regions': self.config['regions'],
                'categories': self.config['categories'],
                'time_periods': self.config['time_periods']
            }
        }
        
        for i in range(min(num_records, 100)):  # 简化模式限制记录数
            region = random.choice(self.config['regions'])
            category = random.choice(self.config['categories'])
            
            record = {
                'id': i + 1,
                'date': f"2024-{random.randint(1,4):02d}-{random.randint(1,28):02d}",
                'region': region,
                'category': category,
                'gmv': random.uniform(800000, 1200000),
                'dau': random.randint(150, 350),
                'conversion_rate': random.uniform(2.5, 4.5),
                'avg_order_value': random.uniform(180, 280),
                'frequency': random.uniform(1.8, 3.2),
                'gross_profit_rate': random.uniform(20.0, 30.0),
                'discount_rate': random.uniform(8.0, 12.0)
            }
            
            data['data'].append(record)
        
        return data
    
    def generate_retail_aggregated_data(self) -> Dict[str, Any]:
        """生成零售业务聚合数据"""
        
        aggregated_data = {
            # 华东区总体数据
            'overall_metrics': {
                'total_gmv': 850000000,  # 8.5亿
                'total_stores': 156,
                'gross_profit_rate': 24.7,
                'discount_rate': 9.9,
                'promotion_rate': 14.8,
                'avg_store_gmv': 5450000,
                'sales_per_sqm': 15200,
                'customer_satisfaction': 87.5
            },
            
            # 区域数据
            'regional_data': {
                '华东一区': {
                    'gmv': 320000000,
                    'store_count': 52,
                    'gmv_growth': 4.9,
                    'gross_profit_rate': 25.1,
                    'discount_rate': 9.5,
                    'promotion_rate': 14.2,
                    'performance_rank': 1
                },
                '华东二区': {
                    'gmv': 290000000,
                    'store_count': 48,
                    'gmv_growth': 1.8,
                    'gross_profit_rate': 24.5,
                    'discount_rate': 10.2,
                    'promotion_rate': 15.1,
                    'performance_rank': 2
                },
                '华东三区': {
                    'gmv': 240000000,
                    'store_count': 56,
                    'gmv_growth': 14.3,
                    'gross_profit_rate': 24.2,
                    'discount_rate': 10.5,
                    'promotion_rate': 15.8,
                    'performance_rank': 3
                }
            },
            
            # 品类数据
            'category_data': {
                '肉禽蛋类': {
                    'sales_volume': 132000000,
                    'sales_growth': 14.0,
                    'profit_margin': 21.2,
                    'contribution_rate': 15.5,
                    'market_trend': 'growing'
                },
                '水产类': {
                    'sales_volume': 84000000,
                    'sales_growth': -6.6,
                    'profit_margin': 18.5,
                    'contribution_rate': 9.9,
                    'market_trend': 'declining'
                },
                '猪肉类': {
                    'sales_volume': 117000000,
                    'sales_growth': -10.7,
                    'profit_margin': 16.8,
                    'contribution_rate': 13.8,
                    'market_trend': 'concerning'
                },
                '冷藏及加工类': {
                    'sales_volume': 82000000,
                    'sales_growth': 13.7,
                    'profit_margin': 28.1,
                    'contribution_rate': 9.6,
                    'market_trend': 'promising'
                },
                '蔬菜类': {
                    'sales_volume': 89000000,
                    'sales_growth': -7.8,
                    'profit_margin': 23.9,
                    'contribution_rate': 10.5,
                    'market_trend': 'stable'
                },
                '水果类': {
                    'sales_volume': 84000000,
                    'sales_growth': 8.9,
                    'profit_margin': 29.8,
                    'contribution_rate': 9.9,
                    'market_trend': 'positive'
                }
            },
            
            # 时间序列数据
            'time_series': {
                'monthly_gmv': {
                    '2024-01': 785000000,
                    '2024-02': 720000000,  # 春节影响
                    '2024-03': 850000000,
                    '2024-04': 890000000
                },
                'monthly_gross_profit_rate': {
                    '2024-01': 24.1,
                    '2024-02': 23.8,
                    '2024-03': 24.7,
                    '2024-04': 24.9
                },
                'monthly_store_count': {
                    '2024-01': 152,
                    '2024-02': 152,
                    '2024-03': 154,
                    '2024-04': 156
                }
            },
            
            # 对比数据（华东区 vs 其他大外区）
            'comparison_data': {
                '华东区': {
                    'gmv': 850000000,
                    'market_share': 18.5,
                    'profit_margin': 24.7,
                    'store_efficiency': 5450000,
                    'growth_rate': 6.25
                },
                '华南区': {
                    'gmv': 720000000,
                    'market_share': 15.6,
                    'profit_margin': 23.2,
                    'store_efficiency': 4950000,
                    'growth_rate': 4.8
                },
                '华北区': {
                    'gmv': 680000000,
                    'market_share': 14.8,
                    'profit_margin': 22.8,
                    'store_efficiency': 4720000,
                    'growth_rate': 3.5
                },
                '西南区': {
                    'gmv': 450000000,
                    'market_share': 9.8,
                    'profit_margin': 21.5,
                    'store_efficiency': 3850000,
                    'growth_rate': 8.2
                }
            }
        }
        
        return aggregated_data
    
    def export_sample_data(self, data: Any, filepath: str, format: str = 'csv') -> bool:
        """导出样本数据"""
        try:
            if format.lower() == 'csv' and PANDAS_AVAILABLE and hasattr(data, 'to_csv'):
                data.to_csv(filepath, index=False, encoding='utf-8-sig')
            elif format.lower() == 'json':
                if hasattr(data, 'to_dict'):
                    data_dict = data.to_dict('records')
                else:
                    data_dict = data
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(data_dict, f, indent=2, ensure_ascii=False)
            else:
                return False
            
            return True
        except Exception as e:
            print(f"导出数据失败: {e}")
            return False
    
    def generate_retail_demo_dataset(self) -> Dict[str, Any]:
        """生成零售演示数据集"""
        
        # 基础样本数据
        sample_data = self.generate_sample_data(500)
        
        # 聚合数据
        aggregated_data = self.generate_retail_aggregated_data()
        
        # 组合完整数据集
        demo_dataset = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'data_type': 'retail_business_demo',
                'records_count': 500 if PANDAS_AVAILABLE else 100,
                'regions': self.config['regions'],
                'categories': self.config['categories'],
                'time_periods': self.config['time_periods']
            },
            'raw_data': sample_data,
            'aggregated_data': aggregated_data,
            'data_quality': {
                'completeness': 95.0,
                'accuracy': 98.5,
                'consistency': 97.2,
                'timeliness': 100.0
            }
        }
        
        return demo_dataset
    
    def create_test_scenarios(self) -> Dict[str, Any]:
        """创建测试场景数据"""
        
        scenarios = {
            'normal_operation': self.generate_sample_data(100),
            'peak_season': self._generate_peak_season_data(),
            'low_season': self._generate_low_season_data(),
            'new_store_opening': self._generate_new_store_data(),
            'promotional_period': self._generate_promotional_data()
        }
        
        return scenarios
    
    def _generate_peak_season_data(self):
        """生成旺季数据"""
        # 增加GMV和客流量
        base_data = self.generate_sample_data(50)
        
        if PANDAS_AVAILABLE and hasattr(base_data, 'loc'):
            # pandas DataFrame处理
            base_data.loc[:, 'gmv'] *= 1.3
            base_data.loc[:, 'dau'] *= 1.25
            base_data.loc[:, 'conversion_rate'] *= 1.1
        elif isinstance(base_data, dict) and 'data' in base_data:
            # 字典格式处理
            for record in base_data['data']:
                record['gmv'] = record.get('gmv', 0) * 1.3
                record['dau'] = int(record.get('dau', 0) * 1.25)
                record['conversion_rate'] = record.get('conversion_rate', 0) * 1.1
        
        return base_data
    
    def _generate_low_season_data(self):
        """生成淡季数据"""
        # 降低GMV和客流量
        base_data = self.generate_sample_data(50)
        
        if PANDAS_AVAILABLE and hasattr(base_data, 'loc'):
            # pandas DataFrame处理
            base_data.loc[:, 'gmv'] *= 0.8
            base_data.loc[:, 'dau'] *= 0.85
            base_data.loc[:, 'discount_rate'] *= 1.15
        elif isinstance(base_data, dict) and 'data' in base_data:
            # 字典格式处理
            for record in base_data['data']:
                record['gmv'] = record.get('gmv', 0) * 0.8
                record['dau'] = int(record.get('dau', 0) * 0.85)
                record['discount_rate'] = record.get('discount_rate', 0) * 1.15
        
        return base_data
    
    def _generate_new_store_data(self):
        """生成新店数据"""
        # 新店爬坡期数据
        base_data = self.generate_sample_data(30)
        
        if PANDAS_AVAILABLE and hasattr(base_data, 'loc'):
            # pandas DataFrame处理
            base_data.loc[:, 'gmv'] *= 0.6  # 新店GMV较低
            base_data.loc[:, 'customer_satisfaction'] *= 0.9  # 满意度待提升
        elif isinstance(base_data, dict) and 'data' in base_data:
            # 字典格式处理
            for record in base_data['data']:
                record['gmv'] = record.get('gmv', 0) * 0.6
                # 添加customer_satisfaction字段如果不存在
                if 'customer_satisfaction' not in record:
                    record['customer_satisfaction'] = random.uniform(80, 95)
                record['customer_satisfaction'] = record.get('customer_satisfaction', 85) * 0.9
        
        return base_data
    
    def _generate_promotional_data(self):
        """生成促销期数据"""
        # 促销活动期间数据
        base_data = self.generate_sample_data(40)
        
        if PANDAS_AVAILABLE and hasattr(base_data, 'loc'):
            # pandas DataFrame处理
            base_data.loc[:, 'gmv'] *= 1.2
            base_data.loc[:, 'discount_rate'] *= 1.4
            base_data.loc[:, 'promotion_rate'] *= 1.6
            base_data.loc[:, 'gross_profit_rate'] *= 0.95
        elif isinstance(base_data, dict) and 'data' in base_data:
            # 字典格式处理
            for record in base_data['data']:
                record['gmv'] = record.get('gmv', 0) * 1.2
                record['discount_rate'] = record.get('discount_rate', 0) * 1.4
                # 添加promotion_rate字段如果不存在
                if 'promotion_rate' not in record:
                    record['promotion_rate'] = random.uniform(12.0, 18.0)
                record['promotion_rate'] = record.get('promotion_rate', 15) * 1.6
                record['gross_profit_rate'] = record.get('gross_profit_rate', 0) * 0.95
        
        return base_data 