#!/usr/bin/env python3
"""
自动化虚拟数据生成器
支持多种业务场景的测试数据生成
"""

import random
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import numpy as np
from faker import Faker
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 初始化Faker
fake = Faker(['zh_CN'])

class VirtualDataGenerator:
    """虚拟数据生成器"""
    
    def __init__(self, seed: Optional[int] = None):
        """
        初始化数据生成器
        
        Args:
            seed: 随机种子，用于生成可重现的数据
        """
        if seed:
            random.seed(seed)
            np.random.seed(seed)
            Faker.seed(seed)
        
        self.categories = [
            '电子产品', '服装配饰', '家居用品', '美妆护肤', '食品饮料',
            '运动户外', '图书音像', '母婴用品', '汽车用品', '健康保健'
        ]
        
        self.regions = [
            '北京', '上海', '广州', '深圳', '杭州', '南京', '武汉', '成都',
            '西安', '重庆', '天津', '青岛', '大连', '厦门', '苏州', '宁波'
        ]
        
        self.industries = [
            'RETAIL', 'FINTECH', 'AI_AGENT', 'COMMUNITY_GB', 'CROSS_INDUSTRY'
        ]
    
    def generate_business_data(self, 
                             num_records: int = 1000,
                             start_date: str = '2024-01-01',
                             end_date: str = '2024-12-31') -> pd.DataFrame:
        """
        生成业务数据
        
        Args:
            num_records: 生成记录数
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            DataFrame: 生成的业务数据
        """
        logger.info(f"开始生成 {num_records} 条业务数据...")
        
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        
        data = []
        for _ in range(num_records):
            # 随机日期
            random_date = start_dt + timedelta(
                days=random.randint(0, (end_dt - start_dt).days)
            )
            
            # 基础数据
            category = random.choice(self.categories)
            region = random.choice(self.regions)
            
            # 生成相关性数据
            base_gmv = random.uniform(10000, 1000000)
            seasonal_factor = 1 + 0.3 * np.sin(random_date.timetuple().tm_yday * 2 * np.pi / 365)
            regional_factor = 1 + random.uniform(-0.2, 0.3)
            category_factor = 1 + random.uniform(-0.15, 0.25)
            
            gmv = base_gmv * seasonal_factor * regional_factor * category_factor
            
            # DAU与GMV相关
            dau = int(gmv / random.uniform(50, 200))
            
            # 订单均价
            order_price = gmv / max(1, dau * random.uniform(0.8, 1.5))
            
            # 转化率
            conversion_rate = random.uniform(0.02, 0.15)
            
            # 添加噪声
            gmv *= random.uniform(0.9, 1.1)
            dau = int(dau * random.uniform(0.9, 1.1))
            order_price *= random.uniform(0.9, 1.1)
            conversion_rate *= random.uniform(0.9, 1.1)
            
            data.append({
                'date': random_date,
                'category': category,
                'region': region,
                'gmv': round(gmv, 2),
                'dau': max(1, dau),
                'order_price': round(order_price, 2),
                'conversion_rate': min(1.0, round(conversion_rate, 4)),
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            })
        
        df = pd.DataFrame(data)
        logger.info(f"✅ 成功生成 {len(df)} 条业务数据")
        return df
    
    def generate_user_data(self, num_users: int = 100) -> pd.DataFrame:
        """
        生成用户数据
        
        Args:
            num_users: 用户数量
            
        Returns:
            DataFrame: 用户数据
        """
        logger.info(f"开始生成 {num_users} 个用户数据...")
        
        users = []
        roles = ['admin', 'analyst', 'user']
        
        for i in range(num_users):
            username = fake.user_name()
            email = fake.email()
            role = random.choices(roles, weights=[0.1, 0.3, 0.6])[0]
            
            users.append({
                'username': username,
                'email': email,
                'password_hash': fake.sha256(),
                'role': role,
                'is_active': random.choice([1, 1, 1, 0]),  # 75%激活率
                'created_at': fake.date_time_between(start_date='-1y', end_date='now'),
                'last_login': fake.date_time_between(start_date='-30d', end_date='now') if random.random() > 0.2 else None
            })
        
        df = pd.DataFrame(users)
        logger.info(f"✅ 成功生成 {len(df)} 个用户数据")
        return df
    
    def generate_financial_data(self, num_records: int = 500) -> pd.DataFrame:
        """
        生成金融交易数据
        
        Args:
            num_records: 记录数量
            
        Returns:
            DataFrame: 金融数据
        """
        logger.info(f"开始生成 {num_records} 条金融数据...")
        
        transaction_types = ['买入', '卖出', '转账', '充值', '提现']
        currencies = ['CNY', 'USD', 'EUR', 'JPY', 'GBP']
        
        data = []
        for _ in range(num_records):
            transaction_type = random.choice(transaction_types)
            currency = random.choice(currencies)
            
            # 根据交易类型生成金额
            if transaction_type in ['买入', '卖出']:
                amount = random.uniform(1000, 100000)
            elif transaction_type in ['充值', '提现']:
                amount = random.uniform(100, 50000)
            else:  # 转账
                amount = random.uniform(10, 10000)
            
            # 手续费
            fee_rate = random.uniform(0.001, 0.01)
            fee = amount * fee_rate
            
            data.append({
                'date': fake.date_time_between(start_date='-1y', end_date='now'),
                'transaction_type': transaction_type,
                'currency': currency,
                'amount': round(amount, 2),
                'fee': round(fee, 2),
                'user_id': fake.uuid4(),
                'status': random.choices(['成功', '失败', '处理中'], weights=[0.85, 0.1, 0.05])[0],
                'created_at': datetime.now()
            })
        
        df = pd.DataFrame(data)
        logger.info(f"✅ 成功生成 {len(df)} 条金融数据")
        return df
    
    def generate_ai_agent_data(self, num_records: int = 300) -> pd.DataFrame:
        """
        生成AI代理数据
        
        Args:
            num_records: 记录数量
            
        Returns:
            DataFrame: AI代理数据
        """
        logger.info(f"开始生成 {num_records} 条AI代理数据...")
        
        agent_types = ['客服机器人', '销售助手', '数据分析师', '内容生成器', '智能推荐']
        models = ['GPT-4', 'Claude-3', 'ChatGLM', 'Qwen', 'Baichuan']
        
        data = []
        for _ in range(num_records):
            agent_type = random.choice(agent_types)
            model = random.choice(models)
            
            # 性能指标
            accuracy = random.uniform(0.7, 0.98)
            response_time = random.uniform(0.1, 3.0)
            success_rate = random.uniform(0.8, 0.99)
            
            # 使用量
            daily_requests = random.randint(100, 10000)
            monthly_cost = daily_requests * 30 * random.uniform(0.001, 0.01)
            
            data.append({
                'date': fake.date_time_between(start_date='-6m', end_date='now'),
                'agent_type': agent_type,
                'model': model,
                'accuracy': round(accuracy, 4),
                'response_time': round(response_time, 2),
                'success_rate': round(success_rate, 4),
                'daily_requests': daily_requests,
                'monthly_cost': round(monthly_cost, 2),
                'created_at': datetime.now()
            })
        
        df = pd.DataFrame(data)
        logger.info(f"✅ 成功生成 {len(df)} 条AI代理数据")
        return df
    
    def generate_community_group_buying_data(self, num_records: int = 800) -> pd.DataFrame:
        """
        生成社区团购数据
        
        Args:
            num_records: 记录数量
            
        Returns:
            DataFrame: 社区团购数据
        """
        logger.info(f"开始生成 {num_records} 条社区团购数据...")
        
        product_categories = ['生鲜蔬菜', '肉类海鲜', '水果', '日用品', '零食饮料']
        community_types = ['高档小区', '普通小区', '老旧小区', '新建小区']
        
        data = []
        for _ in range(num_records):
            category = random.choice(product_categories)
            community_type = random.choice(community_types)
            
            # 基于社区类型调整价格
            price_factor = {
                '高档小区': 1.3,
                '普通小区': 1.0,
                '老旧小区': 0.8,
                '新建小区': 1.1
            }[community_type]
            
            base_price = random.uniform(10, 200)
            group_price = base_price * price_factor * random.uniform(0.6, 0.9)  # 团购折扣
            
            # 团购参与人数
            participants = random.randint(5, 50)
            min_participants = random.randint(3, 10)
            
            # 成团率
            success_rate = 0.9 if participants >= min_participants else 0.3
            is_successful = random.random() < success_rate
            
            data.append({
                'date': fake.date_time_between(start_date='-3m', end_date='now'),
                'product_category': category,
                'community_type': community_type,
                'original_price': round(base_price, 2),
                'group_price': round(group_price, 2),
                'participants': participants,
                'min_participants': min_participants,
                'is_successful': is_successful,
                'total_gmv': round(group_price * participants if is_successful else 0, 2),
                'created_at': datetime.now()
            })
        
        df = pd.DataFrame(data)
        logger.info(f"✅ 成功生成 {len(df)} 条社区团购数据")
        return df
    
    def generate_system_logs(self, num_logs: int = 200) -> pd.DataFrame:
        """
        生成系统日志数据
        
        Args:
            num_logs: 日志数量
            
        Returns:
            DataFrame: 系统日志数据
        """
        logger.info(f"开始生成 {num_logs} 条系统日志...")
        
        log_levels = ['INFO', 'WARNING', 'ERROR', 'DEBUG']
        modules = ['auth', 'api', 'database', 'report', 'websocket', 'analysis']
        
        messages = {
            'INFO': ['用户登录成功', '报告生成完成', '数据处理完成', '系统启动'],
            'WARNING': ['数据库连接缓慢', '内存使用率过高', '请求频率过高'],
            'ERROR': ['数据库连接失败', '文件读取错误', '认证失败', '系统异常'],
            'DEBUG': ['调试信息', '变量值检查', '函数调用跟踪']
        }
        
        data = []
        for _ in range(num_logs):
            level = random.choices(log_levels, weights=[0.6, 0.2, 0.15, 0.05])[0]
            module = random.choice(modules)
            message = random.choice(messages[level])
            
            data.append({
                'level': level,
                'message': message,
                'module': module,
                'user_id': fake.uuid4() if random.random() > 0.3 else None,
                'ip_address': fake.ipv4(),
                'created_at': fake.date_time_between(start_date='-7d', end_date='now')
            })
        
        df = pd.DataFrame(data)
        logger.info(f"✅ 成功生成 {len(df)} 条系统日志")
        return df
    
    def generate_all_data(self) -> Dict[str, pd.DataFrame]:
        """
        生成所有类型的数据
        
        Returns:
            Dict: 包含所有数据类型的字典
        """
        logger.info("🚀 开始生成所有类型的数据...")
        
        all_data = {
            'business_data': self.generate_business_data(1000),
            'users': self.generate_user_data(100),
            'financial_data': self.generate_financial_data(500),
            'ai_agent_data': self.generate_ai_agent_data(300),
            'community_group_buying': self.generate_community_group_buying_data(800),
            'system_logs': self.generate_system_logs(200)
        }
        
        logger.info("🎉 所有数据生成完成！")
        return all_data
    
    def save_to_csv(self, data: Dict[str, pd.DataFrame], output_dir: str = 'data/generated'):
        """
        保存数据到CSV文件
        
        Args:
            data: 数据字典
            output_dir: 输出目录
        """
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        for table_name, df in data.items():
            file_path = os.path.join(output_dir, f"{table_name}.csv")
            df.to_csv(file_path, index=False, encoding='utf-8')
            logger.info(f"✅ 数据已保存到: {file_path}")


def main():
    """主函数 - 生成并保存测试数据"""
    generator = VirtualDataGenerator(seed=42)  # 使用固定种子确保可重现
    
    # 生成所有数据
    all_data = generator.generate_all_data()
    
    # 保存到CSV
    generator.save_to_csv(all_data)
    
    # 显示数据统计
    print("\n📊 数据生成统计:")
    print("=" * 50)
    for table_name, df in all_data.items():
        print(f"{table_name:25} : {len(df):6} 条记录")
    
    print("\n🎉 虚拟数据生成完成！")


if __name__ == "__main__":
    main() 