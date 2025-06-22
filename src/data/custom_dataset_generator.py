#!/usr/bin/env python3
"""
个性化数据集生成器
帮助用户创建自定义的数据结构和示例数据
"""

import os
import sys
import json
import logging
import random
from typing import Dict, Any, List, Optional, Union
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from faker import Faker

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CustomDatasetGenerator:
    """个性化数据集生成器"""
    
    def __init__(self, locale: str = 'zh_CN'):
        """
        初始化数据集生成器
        
        Args:
            locale: 语言环境
        """
        self.fake = Faker(locale)
        self.output_dir = "custom_datasets"
        self.templates_dir = "dataset_templates"
        
        # 创建输出目录
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.templates_dir, exist_ok=True)
        
    def create_business_dataset(self, 
                               name: str = "business_data",
                               size: int = 1000,
                               date_range: int = 365,
                               categories: List[str] = None,
                               regions: List[str] = None) -> pd.DataFrame:
        """
        创建商业数据集
        
        Args:
            name: 数据集名称
            size: 数据条数
            date_range: 日期范围（天数）
            categories: 业务类别列表
            regions: 地区列表
            
        Returns:
            pd.DataFrame: 生成的数据集
        """
        try:
            logger.info(f"🚀 开始生成商业数据集: {name}")
            
            # 默认类别和地区
            if not categories:
                categories = ['电商', '零售', '餐饮', '教育', '医疗', '金融', '科技', '制造']
            
            if not regions:
                regions = ['北京', '上海', '广州', '深圳', '杭州', '成都', '武汉', '西安']
            
            # 生成日期范围
            start_date = datetime.now() - timedelta(days=date_range)
            
            data = []
            for i in range(size):
                # 随机日期
                random_days = random.randint(0, date_range)
                date = start_date + timedelta(days=random_days)
                
                # 基础数据
                category = random.choice(categories)
                region = random.choice(regions)
                
                # 业务指标（添加一些相关性）
                base_gmv = random.uniform(1000, 50000)
                seasonal_factor = 1 + 0.3 * np.sin(2 * np.pi * random_days / 365)  # 季节性因子
                gmv = base_gmv * seasonal_factor
                
                dau = random.randint(100, 10000)
                order_price = gmv / max(dau * random.uniform(0.01, 0.1), 1)  # 订单均价
                conversion_rate = random.uniform(0.01, 0.15)
                
                # 用户行为数据
                page_views = int(dau * random.uniform(3, 15))
                bounce_rate = random.uniform(0.2, 0.8)
                session_duration = random.uniform(60, 1800)  # 会话时长（秒）
                
                # 营销数据
                ad_spend = gmv * random.uniform(0.05, 0.3)  # 广告支出
                organic_traffic = random.uniform(0.3, 0.8)  # 自然流量占比
                
                row = {
                    'date': date.strftime('%Y-%m-%d'),
                    'category': category,
                    'region': region,
                    'gmv': round(gmv, 2),
                    'dau': dau,
                    'order_price': round(order_price, 2),
                    'conversion_rate': round(conversion_rate, 4),
                    'page_views': page_views,
                    'bounce_rate': round(bounce_rate, 4),
                    'session_duration': round(session_duration, 2),
                    'ad_spend': round(ad_spend, 2),
                    'organic_traffic': round(organic_traffic, 4),
                    'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                
                data.append(row)
            
            df = pd.DataFrame(data)
            
            # 保存数据集
            output_file = os.path.join(self.output_dir, f"{name}.csv")
            df.to_csv(output_file, index=False, encoding='utf-8')
            
            logger.info(f"✅ 商业数据集生成完成: {output_file}")
            return df
            
        except Exception as e:
            logger.error(f"❌ 商业数据集生成失败: {str(e)}")
            return pd.DataFrame()
    
    def create_user_dataset(self,
                           name: str = "user_data", 
                           size: int = 1000) -> pd.DataFrame:
        """
        创建用户数据集
        
        Args:
            name: 数据集名称
            size: 用户数量
            
        Returns:
            pd.DataFrame: 生成的用户数据集
        """
        try:
            logger.info(f"🚀 开始生成用户数据集: {name}")
            
            data = []
            for i in range(size):
                # 基础用户信息
                user_id = f"user_{i+1:06d}"
                username = self.fake.user_name()
                email = self.fake.email()
                phone = self.fake.phone_number()
                
                # 个人信息
                name = self.fake.name()
                gender = random.choice(['男', '女'])
                age = random.randint(18, 65)
                birth_date = self.fake.date_of_birth(minimum_age=age, maximum_age=age)
                
                # 地址信息
                province = self.fake.province()
                city = self.fake.city()
                address = self.fake.address()
                
                # 职业信息
                job = self.fake.job()
                company = self.fake.company()
                
                # 用户行为数据
                register_date = self.fake.date_between(start_date='-2y', end_date='today')
                last_login = self.fake.date_time_between(start_date=register_date, end_date='now')
                login_count = random.randint(1, 500)
                
                # 消费数据
                total_orders = random.randint(0, 50)
                total_amount = round(random.uniform(0, 10000), 2)
                avg_order_value = round(total_amount / max(total_orders, 1), 2)
                
                # 用户标签
                user_level = random.choice(['青铜', '白银', '黄金', '铂金', '钻石'])
                is_vip = random.choice([True, False])
                credit_score = random.randint(300, 850)
                
                row = {
                    'user_id': user_id,
                    'username': username,
                    'email': email,
                    'phone': phone,
                    'name': name,
                    'gender': gender,
                    'age': age,
                    'birth_date': birth_date.strftime('%Y-%m-%d'),
                    'province': province,
                    'city': city,
                    'address': address,
                    'job': job,
                    'company': company,
                    'register_date': register_date.strftime('%Y-%m-%d'),
                    'last_login': last_login.strftime('%Y-%m-%d %H:%M:%S'),
                    'login_count': login_count,
                    'total_orders': total_orders,
                    'total_amount': total_amount,
                    'avg_order_value': avg_order_value,
                    'user_level': user_level,
                    'is_vip': is_vip,
                    'credit_score': credit_score,
                    'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                
                data.append(row)
            
            df = pd.DataFrame(data)
            
            # 保存数据集
            output_file = os.path.join(self.output_dir, f"{name}.csv")
            df.to_csv(output_file, index=False, encoding='utf-8')
            
            logger.info(f"✅ 用户数据集生成完成: {output_file}")
            return df
            
        except Exception as e:
            logger.error(f"❌ 用户数据集生成失败: {str(e)}")
            return pd.DataFrame()
    
    def create_product_dataset(self,
                              name: str = "product_data",
                              size: int = 500) -> pd.DataFrame:
        """
        创建产品数据集
        
        Args:
            name: 数据集名称
            size: 产品数量
            
        Returns:
            pd.DataFrame: 生成的产品数据集
        """
        try:
            logger.info(f"🚀 开始生成产品数据集: {name}")
            
            # 产品类别
            categories = ['电子产品', '服装鞋帽', '家居用品', '食品饮料', '美妆护肤', 
                         '运动户外', '图书音像', '母婴用品', '汽车用品', '办公用品']
            
            # 品牌列表
            brands = ['华为', '小米', '苹果', '三星', '联想', '戴尔', '耐克', '阿迪达斯', 
                     '优衣库', 'ZARA', '宜家', '无印良品', '雀巢', '蒙牛', '欧莱雅', '兰蔻']
            
            data = []
            for i in range(size):
                # 基础产品信息
                product_id = f"P{i+1:06d}"
                product_name = f"产品_{i+1}"
                category = random.choice(categories)
                brand = random.choice(brands)
                
                # 价格信息
                cost_price = round(random.uniform(10, 500), 2)
                selling_price = round(cost_price * random.uniform(1.2, 3.0), 2)
                discount_price = round(selling_price * random.uniform(0.7, 0.95), 2)
                
                # 库存信息
                stock_quantity = random.randint(0, 1000)
                sold_quantity = random.randint(0, 500)
                
                # 评价信息
                rating = round(random.uniform(3.0, 5.0), 1)
                review_count = random.randint(0, 1000)
                
                # 产品属性
                weight = round(random.uniform(0.1, 10.0), 2)
                size = random.choice(['S', 'M', 'L', 'XL', 'XXL', '均码'])
                color = random.choice(['红色', '蓝色', '黑色', '白色', '绿色', '黄色', '紫色'])
                
                # 销售数据
                launch_date = self.fake.date_between(start_date='-2y', end_date='today')
                is_active = random.choice([True, False])
                is_featured = random.choice([True, False])
                
                # 供应商信息
                supplier = self.fake.company()
                supplier_contact = self.fake.phone_number()
                
                row = {
                    'product_id': product_id,
                    'product_name': product_name,
                    'category': category,
                    'brand': brand,
                    'cost_price': cost_price,
                    'selling_price': selling_price,
                    'discount_price': discount_price,
                    'stock_quantity': stock_quantity,
                    'sold_quantity': sold_quantity,
                    'rating': rating,
                    'review_count': review_count,
                    'weight': weight,
                    'size': size,
                    'color': color,
                    'launch_date': launch_date.strftime('%Y-%m-%d'),
                    'is_active': is_active,
                    'is_featured': is_featured,
                    'supplier': supplier,
                    'supplier_contact': supplier_contact,
                    'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                
                data.append(row)
            
            df = pd.DataFrame(data)
            
            # 保存数据集
            output_file = os.path.join(self.output_dir, f"{name}.csv")
            df.to_csv(output_file, index=False, encoding='utf-8')
            
            logger.info(f"✅ 产品数据集生成完成: {output_file}")
            return df
            
        except Exception as e:
            logger.error(f"❌ 产品数据集生成失败: {str(e)}")
            return pd.DataFrame()
    
    def create_financial_dataset(self,
                                name: str = "financial_data",
                                size: int = 1000) -> pd.DataFrame:
        """
        创建财务数据集
        
        Args:
            name: 数据集名称
            size: 数据条数
            
        Returns:
            pd.DataFrame: 生成的财务数据集
        """
        try:
            logger.info(f"🚀 开始生成财务数据集: {name}")
            
            # 交易类型
            transaction_types = ['收入', '支出', '投资', '借贷', '转账', '退款', '奖金', '分红']
            
            # 账户类型
            account_types = ['储蓄账户', '支票账户', '信用卡', '投资账户', '贷款账户']
            
            data = []
            for i in range(size):
                # 基础交易信息
                transaction_id = f"T{i+1:08d}"
                transaction_date = self.fake.date_between(start_date='-1y', end_date='today')
                transaction_type = random.choice(transaction_types)
                
                # 金额信息
                amount = round(random.uniform(10, 50000), 2)
                currency = 'CNY'
                
                # 账户信息
                account_id = f"ACC{random.randint(1000, 9999)}"
                account_type = random.choice(account_types)
                account_balance = round(random.uniform(0, 100000), 2)
                
                # 交易对方信息
                counterparty = self.fake.company()
                counterparty_account = f"ACC{random.randint(1000, 9999)}"
                
                # 交易描述
                description = f"{transaction_type} - {self.fake.text(max_nb_chars=50)}"
                
                # 分类信息
                category = random.choice(['餐饮', '购物', '交通', '娱乐', '医疗', '教育', '投资', '其他'])
                subcategory = f"{category}子类{random.randint(1, 5)}"
                
                # 地理信息
                location = self.fake.city()
                merchant = self.fake.company()
                
                # 风险评估
                risk_score = random.randint(1, 100)
                is_suspicious = risk_score > 80
                
                # 状态信息
                status = random.choice(['成功', '处理中', '失败', '已取消'])
                
                row = {
                    'transaction_id': transaction_id,
                    'transaction_date': transaction_date.strftime('%Y-%m-%d'),
                    'transaction_type': transaction_type,
                    'amount': amount,
                    'currency': currency,
                    'account_id': account_id,
                    'account_type': account_type,
                    'account_balance': account_balance,
                    'counterparty': counterparty,
                    'counterparty_account': counterparty_account,
                    'description': description,
                    'category': category,
                    'subcategory': subcategory,
                    'location': location,
                    'merchant': merchant,
                    'risk_score': risk_score,
                    'is_suspicious': is_suspicious,
                    'status': status,
                    'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                
                data.append(row)
            
            df = pd.DataFrame(data)
            
            # 保存数据集
            output_file = os.path.join(self.output_dir, f"{name}.csv")
            df.to_csv(output_file, index=False, encoding='utf-8')
            
            logger.info(f"✅ 财务数据集生成完成: {output_file}")
            return df
            
        except Exception as e:
            logger.error(f"❌ 财务数据集生成失败: {str(e)}")
            return pd.DataFrame()
    
    def create_custom_dataset(self, 
                             template: Dict[str, Any],
                             name: str = "custom_data",
                             size: int = 1000) -> pd.DataFrame:
        """
        根据模板创建自定义数据集
        
        Args:
            template: 数据模板定义
            name: 数据集名称
            size: 数据条数
            
        Returns:
            pd.DataFrame: 生成的自定义数据集
        """
        try:
            logger.info(f"🚀 开始生成自定义数据集: {name}")
            
            data = []
            for i in range(size):
                row = {}
                
                for field_name, field_config in template.items():
                    field_type = field_config.get('type', 'string')
                    field_options = field_config.get('options', {})
                    
                    # 根据字段类型生成数据
                    if field_type == 'id':
                        row[field_name] = f"{field_options.get('prefix', 'ID')}{i+1:06d}"
                    
                    elif field_type == 'string':
                        if 'choices' in field_options:
                            row[field_name] = random.choice(field_options['choices'])
                        else:
                            row[field_name] = self.fake.text(max_nb_chars=field_options.get('max_length', 50))
                    
                    elif field_type == 'name':
                        row[field_name] = self.fake.name()
                    
                    elif field_type == 'email':
                        row[field_name] = self.fake.email()
                    
                    elif field_type == 'phone':
                        row[field_name] = self.fake.phone_number()
                    
                    elif field_type == 'address':
                        row[field_name] = self.fake.address()
                    
                    elif field_type == 'company':
                        row[field_name] = self.fake.company()
                    
                    elif field_type == 'integer':
                        min_val = field_options.get('min', 0)
                        max_val = field_options.get('max', 1000)
                        row[field_name] = random.randint(min_val, max_val)
                    
                    elif field_type == 'float':
                        min_val = field_options.get('min', 0.0)
                        max_val = field_options.get('max', 1000.0)
                        decimals = field_options.get('decimals', 2)
                        row[field_name] = round(random.uniform(min_val, max_val), decimals)
                    
                    elif field_type == 'boolean':
                        row[field_name] = random.choice([True, False])
                    
                    elif field_type == 'date':
                        start_date = field_options.get('start_date', '-1y')
                        end_date = field_options.get('end_date', 'today')
                        row[field_name] = self.fake.date_between(start_date=start_date, end_date=end_date).strftime('%Y-%m-%d')
                    
                    elif field_type == 'datetime':
                        start_date = field_options.get('start_date', '-1y')
                        end_date = field_options.get('end_date', 'now')
                        row[field_name] = self.fake.date_time_between(start_date=start_date, end_date=end_date).strftime('%Y-%m-%d %H:%M:%S')
                    
                    else:
                        row[field_name] = f"数据_{i+1}"
                
                data.append(row)
            
            df = pd.DataFrame(data)
            
            # 保存数据集
            output_file = os.path.join(self.output_dir, f"{name}.csv")
            df.to_csv(output_file, index=False, encoding='utf-8')
            
            logger.info(f"✅ 自定义数据集生成完成: {output_file}")
            return df
            
        except Exception as e:
            logger.error(f"❌ 自定义数据集生成失败: {str(e)}")
            return pd.DataFrame()
    
    def save_template(self, template: Dict[str, Any], template_name: str) -> bool:
        """
        保存数据模板
        
        Args:
            template: 数据模板
            template_name: 模板名称
            
        Returns:
            bool: 保存是否成功
        """
        try:
            template_file = os.path.join(self.templates_dir, f"{template_name}.json")
            
            template_data = {
                'name': template_name,
                'created_at': datetime.now().isoformat(),
                'template': template
            }
            
            with open(template_file, 'w', encoding='utf-8') as f:
                json.dump(template_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"✅ 数据模板保存成功: {template_file}")
            return True
            
        except Exception as e:
            logger.error(f"❌ 数据模板保存失败: {str(e)}")
            return False
    
    def load_template(self, template_name: str) -> Optional[Dict[str, Any]]:
        """
        加载数据模板
        
        Args:
            template_name: 模板名称
            
        Returns:
            Dict: 数据模板
        """
        try:
            template_file = os.path.join(self.templates_dir, f"{template_name}.json")
            
            if not os.path.exists(template_file):
                logger.error(f"❌ 模板文件不存在: {template_file}")
                return None
            
            with open(template_file, 'r', encoding='utf-8') as f:
                template_data = json.load(f)
            
            return template_data.get('template', {})
            
        except Exception as e:
            logger.error(f"❌ 数据模板加载失败: {str(e)}")
            return None
    
    def list_templates(self) -> List[str]:
        """
        列出所有模板
        
        Returns:
            List[str]: 模板名称列表
        """
        try:
            templates = []
            for file in os.listdir(self.templates_dir):
                if file.endswith('.json'):
                    templates.append(file[:-5])  # 移除.json后缀
            
            return sorted(templates)
            
        except Exception as e:
            logger.error(f"❌ 列出模板失败: {str(e)}")
            return []
    
    def export_to_formats(self, df: pd.DataFrame, name: str, formats: List[str] = None):
        """
        导出数据集到多种格式
        
        Args:
            df: 数据集
            name: 文件名
            formats: 导出格式列表
        """
        if formats is None:
            formats = ['csv', 'json', 'excel']
        
        try:
            for fmt in formats:
                if fmt.lower() == 'csv':
                    output_file = os.path.join(self.output_dir, f"{name}.csv")
                    df.to_csv(output_file, index=False, encoding='utf-8')
                
                elif fmt.lower() == 'json':
                    output_file = os.path.join(self.output_dir, f"{name}.json")
                    df.to_json(output_file, orient='records', ensure_ascii=False, indent=2)
                
                elif fmt.lower() in ['excel', 'xlsx']:
                    output_file = os.path.join(self.output_dir, f"{name}.xlsx")
                    df.to_excel(output_file, index=False)
                
                logger.info(f"✅ 数据集导出成功: {output_file}")
                
        except Exception as e:
            logger.error(f"❌ 数据集导出失败: {str(e)}")


def interactive_dataset_generator():
    """交互式数据集生成器"""
    print("🎯 个性化数据集生成器")
    print("=" * 50)
    
    generator = CustomDatasetGenerator()
    
    while True:
        print("\n📊 数据集生成菜单:")
        print("1. 生成商业数据集")
        print("2. 生成用户数据集")
        print("3. 生成产品数据集")
        print("4. 生成财务数据集")
        print("5. 创建自定义数据集")
        print("6. 管理数据模板")
        print("7. 退出")
        
        choice = input("请选择操作 (1-7): ").strip()
        
        if choice == '1':
            # 生成商业数据集
            name = input("数据集名称 (默认: business_data): ") or "business_data"
            size = int(input("数据条数 (默认: 1000): ") or "1000")
            date_range = int(input("日期范围/天 (默认: 365): ") or "365")
            
            df = generator.create_business_dataset(name, size, date_range)
            if not df.empty:
                print(f"✅ 商业数据集生成成功: {len(df)} 条数据")
                print(df.head())
        
        elif choice == '2':
            # 生成用户数据集
            name = input("数据集名称 (默认: user_data): ") or "user_data"
            size = int(input("用户数量 (默认: 1000): ") or "1000")
            
            df = generator.create_user_dataset(name, size)
            if not df.empty:
                print(f"✅ 用户数据集生成成功: {len(df)} 条数据")
                print(df.head())
        
        elif choice == '3':
            # 生成产品数据集
            name = input("数据集名称 (默认: product_data): ") or "product_data"
            size = int(input("产品数量 (默认: 500): ") or "500")
            
            df = generator.create_product_dataset(name, size)
            if not df.empty:
                print(f"✅ 产品数据集生成成功: {len(df)} 条数据")
                print(df.head())
        
        elif choice == '4':
            # 生成财务数据集
            name = input("数据集名称 (默认: financial_data): ") or "financial_data"
            size = int(input("数据条数 (默认: 1000): ") or "1000")
            
            df = generator.create_financial_dataset(name, size)
            if not df.empty:
                print(f"✅ 财务数据集生成成功: {len(df)} 条数据")
                print(df.head())
        
        elif choice == '5':
            # 创建自定义数据集
            print("请选择:")
            print("1. 从模板创建")
            print("2. 手动定义结构")
            
            sub_choice = input("选择 (1-2): ").strip()
            
            if sub_choice == '1':
                # 从模板创建
                templates = generator.list_templates()
                if templates:
                    print("可用模板:")
                    for i, template in enumerate(templates, 1):
                        print(f"  {i}. {template}")
                    
                    template_idx = int(input("选择模板编号: ")) - 1
                    if 0 <= template_idx < len(templates):
                        template_name = templates[template_idx]
                        template = generator.load_template(template_name)
                        
                        if template:
                            name = input("数据集名称: ")
                            size = int(input("数据条数 (默认: 1000): ") or "1000")
                            
                            df = generator.create_custom_dataset(template, name, size)
                            if not df.empty:
                                print(f"✅ 自定义数据集生成成功: {len(df)} 条数据")
                                print(df.head())
                else:
                    print("❌ 没有可用的模板")
            
            elif sub_choice == '2':
                # 手动定义结构
                print("请定义数据结构 (格式: 字段名:类型:选项，输入'END'结束):")
                print("支持的类型: id, string, name, email, phone, address, company, integer, float, boolean, date, datetime")
                
                template = {}
                while True:
                    line = input().strip()
                    if line == 'END':
                        break
                    
                    if ':' in line:
                        parts = line.split(':')
                        field_name = parts[0].strip()
                        field_type = parts[1].strip() if len(parts) > 1 else 'string'
                        
                        template[field_name] = {'type': field_type}
                        
                        # 根据类型添加选项
                        if field_type in ['integer', 'float']:
                            min_val = input(f"  {field_name} 最小值 (默认: 0): ") or "0"
                            max_val = input(f"  {field_name} 最大值 (默认: 1000): ") or "1000"
                            template[field_name]['options'] = {
                                'min': int(min_val) if field_type == 'integer' else float(min_val),
                                'max': int(max_val) if field_type == 'integer' else float(max_val)
                            }
                        
                        elif field_type == 'string':
                            choices = input(f"  {field_name} 选项 (用逗号分隔，留空则随机生成): ").strip()
                            if choices:
                                template[field_name]['options'] = {'choices': [c.strip() for c in choices.split(',')]}
                
                if template:
                    name = input("数据集名称: ")
                    size = int(input("数据条数 (默认: 1000): ") or "1000")
                    
                    # 询问是否保存模板
                    save_template = input("是否保存为模板? (y/n): ").lower() == 'y'
                    if save_template:
                        template_name = input("模板名称: ")
                        generator.save_template(template, template_name)
                    
                    df = generator.create_custom_dataset(template, name, size)
                    if not df.empty:
                        print(f"✅ 自定义数据集生成成功: {len(df)} 条数据")
                        print(df.head())
        
        elif choice == '6':
            # 管理数据模板
            print("模板管理:")
            print("1. 列出所有模板")
            print("2. 查看模板详情")
            print("3. 删除模板")
            
            sub_choice = input("选择 (1-3): ").strip()
            
            if sub_choice == '1':
                templates = generator.list_templates()
                if templates:
                    print("可用模板:")
                    for template in templates:
                        print(f"  - {template}")
                else:
                    print("❌ 没有可用的模板")
            
            elif sub_choice == '2':
                template_name = input("模板名称: ")
                template = generator.load_template(template_name)
                if template:
                    print(f"模板 '{template_name}' 详情:")
                    print(json.dumps(template, ensure_ascii=False, indent=2))
            
            elif sub_choice == '3':
                template_name = input("要删除的模板名称: ")
                template_file = os.path.join(generator.templates_dir, f"{template_name}.json")
                if os.path.exists(template_file):
                    os.remove(template_file)
                    print(f"✅ 模板 '{template_name}' 已删除")
                else:
                    print(f"❌ 模板 '{template_name}' 不存在")
        
        elif choice == '7':
            print("👋 感谢使用个性化数据集生成器")
            break
        
        else:
            print("❌ 无效选择，请重试")


if __name__ == "__main__":
    interactive_dataset_generator() 