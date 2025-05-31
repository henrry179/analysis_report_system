import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union, Tuple
import logging
from datetime import datetime
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import statsmodels.api as sm
from scipy import stats

class AnalysisEngine:
    """分析引擎核心类，负责数据分析和预测"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.scaler = StandardScaler()
        
    def analyze_data(self, df: pd.DataFrame, analysis_type: str) -> Dict:
        """
        数据分析主函数
        
        Args:
            df: 输入数据框
            analysis_type: 分析类型
            
        Returns:
            Dict: 分析结果
        """
        try:
            if analysis_type == 'descriptive':
                return self._descriptive_analysis(df)
            elif analysis_type == 'correlation':
                return self._correlation_analysis(df)
            elif analysis_type == 'trend':
                return self._trend_analysis(df)
            elif analysis_type == 'forecast':
                return self._forecast_analysis(df)
            else:
                raise ValueError(f"不支持的分析类型: {analysis_type}")
                
        except Exception as e:
            self.logger.error(f"数据分析失败: {str(e)}")
            raise
            
    def _descriptive_analysis(self, df: pd.DataFrame) -> Dict:
        """描述性统计分析"""
        try:
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            categorical_cols = df.select_dtypes(include=['object']).columns
            
            results = {
                'numeric_stats': {},
                'categorical_stats': {},
                'analysis_time': datetime.now().isoformat()
            }
            
            # 数值型列统计
            for col in numeric_cols:
                results['numeric_stats'][col] = {
                    'mean': df[col].mean(),
                    'median': df[col].median(),
                    'std': df[col].std(),
                    'min': df[col].min(),
                    'max': df[col].max(),
                    'skew': df[col].skew(),
                    'kurtosis': df[col].kurtosis()
                }
                
            # 分类型列统计
            for col in categorical_cols:
                results['categorical_stats'][col] = {
                    'unique_values': df[col].nunique(),
                    'most_common': df[col].value_counts().head().to_dict(),
                    'missing_values': df[col].isnull().sum()
                }
                
            return results
            
        except Exception as e:
            self.logger.error(f"描述性分析失败: {str(e)}")
            raise
            
    def _correlation_analysis(self, df: pd.DataFrame) -> Dict:
        """相关性分析"""
        try:
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            corr_matrix = df[numeric_cols].corr()
            
            # 获取强相关性对
            strong_correlations = []
            for i in range(len(numeric_cols)):
                for j in range(i+1, len(numeric_cols)):
                    corr = corr_matrix.iloc[i, j]
                    if abs(corr) > 0.7:  # 相关系数阈值
                        strong_correlations.append({
                            'var1': numeric_cols[i],
                            'var2': numeric_cols[j],
                            'correlation': corr
                        })
                        
            return {
                'correlation_matrix': corr_matrix.to_dict(),
                'strong_correlations': strong_correlations,
                'analysis_time': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"相关性分析失败: {str(e)}")
            raise
            
    def _trend_analysis(self, df: pd.DataFrame) -> Dict:
        """趋势分析"""
        try:
            # 确保有时间列
            time_cols = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]
            if not time_cols:
                raise ValueError("未找到时间列")
                
            time_col = time_cols[0]
            df[time_col] = pd.to_datetime(df[time_col])
            df = df.sort_values(time_col)
            
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            trend_results = {}
            
            for col in numeric_cols:
                # 计算移动平均
                df[f'{col}_ma7'] = df[col].rolling(window=7).mean()
                df[f'{col}_ma30'] = df[col].rolling(window=30).mean()
                
                # 计算同比增长率
                df[f'{col}_yoy'] = df[col].pct_change(periods=12)  # 假设月度数据
                
                trend_results[col] = {
                    'latest_value': df[col].iloc[-1],
                    'ma7': df[f'{col}_ma7'].iloc[-1],
                    'ma30': df[f'{col}_ma30'].iloc[-1],
                    'yoy_growth': df[f'{col}_yoy'].iloc[-1],
                    'trend_direction': 'up' if df[col].iloc[-1] > df[col].iloc[-2] else 'down'
                }
                
            return {
                'trend_analysis': trend_results,
                'analysis_time': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"趋势分析失败: {str(e)}")
            raise
            
    def _forecast_analysis(self, df: pd.DataFrame) -> Dict:
        """预测分析"""
        try:
            # 确保有时间列
            time_cols = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]
            if not time_cols:
                raise ValueError("未找到时间列")
                
            time_col = time_cols[0]
            df[time_col] = pd.to_datetime(df[time_col])
            df = df.sort_values(time_col)
            
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            forecast_results = {}
            
            for col in numeric_cols:
                # 准备时间序列数据
                y = df[col].values
                X = np.arange(len(y)).reshape(-1, 1)
                
                # 训练模型
                model = RandomForestRegressor(n_estimators=100, random_state=42)
                model.fit(X, y)
                
                # 预测未来30天
                future_X = np.arange(len(y), len(y) + 30).reshape(-1, 1)
                predictions = model.predict(future_X)
                
                forecast_results[col] = {
                    'predictions': predictions.tolist(),
                    'confidence_interval': {
                        'lower': (predictions - 1.96 * np.std(predictions)).tolist(),
                        'upper': (predictions + 1.96 * np.std(predictions)).tolist()
                    },
                    'model_metrics': {
                        'r2_score': r2_score(y, model.predict(X)),
                        'rmse': np.sqrt(mean_squared_error(y, model.predict(X)))
                    }
                }
                
            return {
                'forecast_analysis': forecast_results,
                'analysis_time': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"预测分析失败: {str(e)}")
            raise
            
    def segment_customers(self, df: pd.DataFrame, n_clusters: int = 3) -> Dict:
        """
        客户分群分析
        
        Args:
            df: 输入数据框
            n_clusters: 分群数量
            
        Returns:
            Dict: 分群结果
        """
        try:
            # 选择用于分群的特征
            features = df.select_dtypes(include=[np.number]).columns
            
            # 数据标准化
            X = self.scaler.fit_transform(df[features])
            
            # K-means聚类
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            clusters = kmeans.fit_predict(X)
            
            # 计算每个群的特征统计
            df['cluster'] = clusters
            cluster_stats = {}
            
            for i in range(n_clusters):
                cluster_data = df[df['cluster'] == i]
                cluster_stats[f'cluster_{i}'] = {
                    'size': len(cluster_data),
                    'features': {
                        feature: {
                            'mean': cluster_data[feature].mean(),
                            'std': cluster_data[feature].std()
                        }
                        for feature in features
                    }
                }
                
            return {
                'cluster_assignments': clusters.tolist(),
                'cluster_statistics': cluster_stats,
                'analysis_time': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"客户分群分析失败: {str(e)}")
            raise 