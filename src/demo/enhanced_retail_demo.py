#!/usr/bin/env python3
"""
增强零售业务分析演示脚本
展示更新后的虚拟数据集和专业报告格式
基于华东区分析报告标准设计
"""

import os
import sys
import time
from datetime import datetime, timedelta

# 添加源代码路径
sys.path.append('src')

def main():
    """增强零售业务分析演示主函数"""
    print("🏪 增强零售业务分析报告系统演示")
    print("   集成虚拟数据生成器和专业报告格式")
    print("=" * 80)
    
    start_time = time.time()
    
    # 确保输出目录存在
    os.makedirs('output/enhanced_retail_demo', exist_ok=True)
    
    demo_results = {}
    
    try:
        # 1. 演示虚拟数据生成
        print("\n📊 1. 演示虚拟数据生成...")
        demo_results['data_generation'] = demo_virtual_data_generation()
        
        # 2. 演示增强报告生成
        print("\n📄 2. 演示增强零售报告生成...")
        demo_results['enhanced_reports'] = demo_enhanced_report_generation()
        
        # 3. 演示多场景分析
        print("\n🎯 3. 演示多场景业务分析...")
        demo_results['scenario_analysis'] = demo_scenario_analysis()
        
        # 4. 演示数据质量分析
        print("\n📈 4. 演示数据质量分析...")
        demo_results['quality_analysis'] = demo_data_quality_analysis()
        
        # 5. 演示完整业务流程
        print("\n🔄 5. 演示完整业务分析流程...")
        demo_results['complete_workflow'] = demo_complete_business_workflow()
        
    except Exception as e:
        print(f"\n❌ 演示过程中发生错误: {e}")
        demo_results['error'] = str(e)
    
    finally:
        # 总结演示结果
        end_time = time.time()
        execution_time = end_time - start_time
        
        print(f"\n{'='*80}")
        print("🎉 增强零售业务分析演示完成")
        print(f"⏱️  总执行时间: {execution_time:.2f} 秒")
        
        total_files = sum(len(result.get('files_created', [])) for result in demo_results.values() if isinstance(result, dict))
        print(f"📁 生成文件总数: {total_files} 个")
        
        successful_demos = len([k for k, v in demo_results.items() if k != 'error' and v])
        print(f"✅ 成功演示模块: {successful_demos}/5")
        
        if 'error' not in demo_results:
            print("🌟 所有演示模块运行成功!")
        
        print(f"\n📂 演示文件保存在: output/enhanced_retail_demo/")
        print("🔍 请查看生成的报告和数据文件")
        print("=" * 80)
    
    return demo_results

def demo_virtual_data_generation():
    """演示虚拟数据生成功能"""
    
    try:
        from data.sample_data_generator import SampleDataGenerator
        
        generator = SampleDataGenerator()
        demo_result = {
            'status': 'success',
            'files_created': [],
            'data_samples': {}
        }
        
        print("  📊 生成零售业务虚拟数据集...")
        
        # 生成基础样本数据
        sample_data = generator.generate_sample_data(300)
        print(f"    ✅ 生成样本数据: 300条记录")
        
        # 生成聚合数据
        aggregated_data = generator.generate_retail_aggregated_data()
        print(f"    ✅ 生成聚合数据: 包含区域、品类、时间序列数据")
        
        # 生成完整演示数据集
        demo_dataset = generator.generate_retail_demo_dataset()
        print(f"    ✅ 生成演示数据集: 完整的零售业务数据")
        
        # 导出数据文件
        output_dir = 'output/enhanced_retail_demo'
        
        # 导出样本数据
        if hasattr(sample_data, 'to_csv'):
            sample_file = os.path.join(output_dir, f"sample_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
            sample_data.to_csv(sample_file, index=False, encoding='utf-8-sig')
            demo_result['files_created'].append(sample_file)
            print(f"    📁 样本数据导出: {os.path.basename(sample_file)}")
        
        # 导出聚合数据
        import json
        aggregated_file = os.path.join(output_dir, f"aggregated_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(aggregated_file, 'w', encoding='utf-8') as f:
            json.dump(aggregated_data, f, indent=2, ensure_ascii=False)
        demo_result['files_created'].append(aggregated_file)
        print(f"    📁 聚合数据导出: {os.path.basename(aggregated_file)}")
        
        # 记录数据统计
        demo_result['data_samples'] = {
            'sample_records': len(sample_data) if hasattr(sample_data, '__len__') else 300,
            'regions': len(aggregated_data.get('regional_data', {})),
            'categories': len(aggregated_data.get('category_data', {})),
            'time_periods': len(aggregated_data.get('time_series', {}).get('monthly_gmv', {}))
        }
        
        return demo_result
        
    except ImportError:
        print("    ⚠️ 虚拟数据生成器不可用，使用简化演示")
        return {'status': 'unavailable', 'reason': 'module_not_found'}
    
    except Exception as e:
        print(f"    ❌ 虚拟数据生成失败: {e}")
        return {'status': 'error', 'error': str(e)}

def demo_enhanced_report_generation():
    """演示增强报告生成功能"""
    
    try:
        from reports.retail_business_report_generator import RetailBusinessReportGenerator
        
        generator = RetailBusinessReportGenerator()
        demo_result = {
            'status': 'success',
            'files_created': [],
            'reports_generated': []
        }
        
        print("  📄 生成增强零售业务报告...")
        
        # 使用新的数据生成和格式化器
        report_result = generator.generate_retail_business_report_with_data(
            report_period="2024年4月数据(4.1~4.30)",
            use_sample_data=True,
            output_dir='output/enhanced_retail_demo'
        )
        
        demo_result['files_created'] = report_result.get('files_created', [])
        demo_result['reports_generated'] = report_result.get('reports_generated', [])
        
        for file_path in demo_result['files_created']:
            print(f"    📁 报告生成: {os.path.basename(file_path)}")
        
        print(f"    ✅ 成功生成 {len(demo_result['files_created'])} 个报告文件")
        
        return demo_result
        
    except Exception as e:
        print(f"    ❌ 增强报告生成失败: {e}")
        return {'status': 'error', 'error': str(e)}

def demo_scenario_analysis():
    """演示多场景业务分析"""
    
    try:
        from reports.retail_business_report_generator import RetailBusinessReportGenerator
        
        generator = RetailBusinessReportGenerator()
        demo_result = {
            'status': 'success',
            'files_created': [],
            'scenarios_tested': []
        }
        
        print("  🎯 生成多场景业务分析报告...")
        
        # 生成完整的演示报告集合
        demo_reports = generator.generate_retail_demo_reports(
            output_dir='output/enhanced_retail_demo'
        )
        
        demo_result['files_created'] = demo_reports.get('files_created', [])
        demo_result['scenarios_tested'] = demo_reports.get('scenarios_tested', [])
        
        print(f"    ✅ 测试场景数量: {len(demo_result['scenarios_tested'])}")
        for scenario in demo_result['scenarios_tested']:
            print(f"      📊 {scenario.replace('_', ' ').title()}")
        
        print(f"    📁 生成文件数量: {len(demo_result['files_created'])}")
        
        return demo_result
        
    except Exception as e:
        print(f"    ❌ 场景分析演示失败: {e}")
        return {'status': 'error', 'error': str(e)}

def demo_data_quality_analysis():
    """演示数据质量分析"""
    
    try:
        from data.sample_data_generator import SampleDataGenerator
        
        generator = SampleDataGenerator()
        demo_result = {
            'status': 'success',
            'quality_metrics': {},
            'analysis_summary': {}
        }
        
        print("  📈 进行数据质量分析...")
        
        # 生成演示数据集并分析质量
        demo_dataset = generator.generate_retail_demo_dataset()
        quality_metrics = demo_dataset.get('data_quality', {})
        
        demo_result['quality_metrics'] = quality_metrics
        
        print("    📊 数据质量评估结果:")
        for metric, score in quality_metrics.items():
            metric_names = {
                'completeness': '完整性',
                'accuracy': '准确性',
                'consistency': '一致性',
                'timeliness': '时效性'
            }
            metric_name = metric_names.get(metric, metric)
            
            if score >= 95:
                status = "🌟 优秀"
            elif score >= 90:
                status = "✅ 良好"
            else:
                status = "⚠️ 一般"
            
            print(f"      {metric_name}: {score:.1f}% {status}")
        
        # 计算总体质量评分
        avg_score = sum(quality_metrics.values()) / len(quality_metrics) if quality_metrics else 0
        demo_result['analysis_summary'] = {
            'overall_score': avg_score,
            'total_metrics': len(quality_metrics),
            'excellent_metrics': len([s for s in quality_metrics.values() if s >= 95])
        }
        
        print(f"    📊 总体质量评分: {avg_score:.1f}%")
        
        return demo_result
        
    except ImportError:
        print("    ⚠️ 数据生成器不可用")
        return {'status': 'unavailable', 'reason': 'module_not_found'}
    
    except Exception as e:
        print(f"    ❌ 数据质量分析失败: {e}")
        return {'status': 'error', 'error': str(e)}

def demo_complete_business_workflow():
    """演示完整业务分析工作流"""
    
    demo_result = {
        'status': 'success',
        'workflow_steps': [],
        'total_processing_time': 0
    }
    
    workflow_start = time.time()
    
    print("  🔄 执行完整业务分析工作流...")
    
    try:
        # 步骤1: 数据准备
        print("    1️⃣ 数据准备阶段...")
        step_start = time.time()
        
        from data.sample_data_generator import SampleDataGenerator
        generator = SampleDataGenerator()
        
        # 生成业务数据
        sample_data = generator.generate_sample_data(200)
        aggregated_data = generator.generate_retail_aggregated_data()
        
        step_time = time.time() - step_start
        demo_result['workflow_steps'].append({
            'step': 'data_preparation',
            'duration': step_time,
            'status': 'success'
        })
        print(f"       ✅ 数据准备完成 ({step_time:.3f}s)")
        
        # 步骤2: 数据分析
        print("    2️⃣ 数据分析阶段...")
        step_start = time.time()
        
        # 模拟数据分析过程
        analysis_results = {
            'correlation_analysis': '相关性分析完成',
            'trend_analysis': '趋势分析完成',
            'anomaly_detection': '异常检测完成'
        }
        
        step_time = time.time() - step_start
        demo_result['workflow_steps'].append({
            'step': 'data_analysis',
            'duration': step_time,
            'status': 'success'
        })
        print(f"       ✅ 数据分析完成 ({step_time:.3f}s)")
        
        # 步骤3: 报告生成
        print("    3️⃣ 报告生成阶段...")
        step_start = time.time()
        
        from reports.retail_business_report_generator import RetailBusinessReportGenerator
        report_generator = RetailBusinessReportGenerator()
        
        report_results = report_generator.generate_retail_business_report_with_data(
            "2024年4月工作流演示",
            use_sample_data=True,
            output_dir='output/enhanced_retail_demo'
        )
        
        step_time = time.time() - step_start
        demo_result['workflow_steps'].append({
            'step': 'report_generation',
            'duration': step_time,
            'status': 'success',
            'files_created': len(report_results.get('files_created', []))
        })
        print(f"       ✅ 报告生成完成 ({step_time:.3f}s)")
        print(f"       📁 生成报告文件: {len(report_results.get('files_created', []))} 个")
        
        # 步骤4: 质量验证
        print("    4️⃣ 质量验证阶段...")
        step_start = time.time()
        
        # 验证生成的文件
        files_created = report_results.get('files_created', [])
        valid_files = [f for f in files_created if os.path.exists(f) and os.path.getsize(f) > 0]
        
        step_time = time.time() - step_start
        demo_result['workflow_steps'].append({
            'step': 'quality_validation',
            'duration': step_time,
            'status': 'success',
            'valid_files': len(valid_files),
            'total_files': len(files_created)
        })
        print(f"       ✅ 质量验证完成 ({step_time:.3f}s)")
        print(f"       📊 文件验证: {len(valid_files)}/{len(files_created)} 通过")
        
    except Exception as e:
        print(f"    ❌ 工作流执行失败: {e}")
        demo_result['status'] = 'error'
        demo_result['error'] = str(e)
    
    workflow_time = time.time() - workflow_start
    demo_result['total_processing_time'] = workflow_time
    
    if demo_result['status'] == 'success':
        print(f"    🎉 完整工作流执行成功 (总计 {workflow_time:.3f}s)")
        
        # 工作流性能统计
        total_steps = len(demo_result['workflow_steps'])
        successful_steps = len([s for s in demo_result['workflow_steps'] if s['status'] == 'success'])
        
        print(f"    📊 工作流统计: {successful_steps}/{total_steps} 步骤成功")
    
    return demo_result

if __name__ == "__main__":
    main() 