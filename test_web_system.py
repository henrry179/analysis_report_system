#!/usr/bin/env python3
"""
Web系统功能测试脚本
测试所有API接口和页面是否正常工作
"""

import requests
import json
import time
from datetime import datetime

def test_web_system():
    """测试Web系统的所有功能"""
    base_url = "http://localhost:8000"
    
    print("🔍 开始测试Web系统功能...")
    print("=" * 50)
    
    tests = []
    
    # 测试1: 主页
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200 and "<!DOCTYPE html>" in response.text:
            tests.append(("✅ 主页", "正常"))
        else:
            tests.append(("❌ 主页", f"状态码: {response.status_code}"))
    except Exception as e:
        tests.append(("❌ 主页", f"错误: {str(e)}"))
    
    # 测试2: 系统信息API
    try:
        response = requests.get(f"{base_url}/api/info")
        if response.status_code == 200:
            info = response.json()
            tests.append(("✅ 系统信息API", f"版本: {info.get('version', 'N/A')}"))
        else:
            tests.append(("❌ 系统信息API", f"状态码: {response.status_code}"))
    except Exception as e:
        tests.append(("❌ 系统信息API", f"错误: {str(e)}"))
    
    # 测试3: 图表数据API
    try:
        response = requests.get(f"{base_url}/charts")
        if response.status_code == 200:
            charts = response.json()
            pie_data_count = len(charts.get('pie', {}).get('values', []))
            bar_data_count = len(charts.get('bar', {}).get('values', []))
            tests.append(("✅ 图表数据API", f"饼图数据: {pie_data_count}项, 柱状图数据: {bar_data_count}项"))
        else:
            tests.append(("❌ 图表数据API", f"状态码: {response.status_code}"))
    except Exception as e:
        tests.append(("❌ 图表数据API", f"错误: {str(e)}"))
    
    # 测试4: 单个图表数据API
    try:
        response = requests.get(f"{base_url}/charts/pie")
        if response.status_code == 200:
            pie_chart = response.json()
            tests.append(("✅ 饼图数据API", f"标题: {pie_chart.get('title', 'N/A')}"))
        else:
            tests.append(("❌ 饼图数据API", f"状态码: {response.status_code}"))
    except Exception as e:
        tests.append(("❌ 饼图数据API", f"错误: {str(e)}"))
    
    # 测试5: 报告列表页面
    try:
        response = requests.get(f"{base_url}/reports")
        if response.status_code == 200 and "<!DOCTYPE html>" in response.text:
            tests.append(("✅ 报告列表页面", "正常"))
        else:
            tests.append(("❌ 报告列表页面", f"状态码: {response.status_code}"))
    except Exception as e:
        tests.append(("❌ 报告列表页面", f"错误: {str(e)}"))
    
    # 测试6: 报告列表API
    try:
        response = requests.get(f"{base_url}/api/reports")
        if response.status_code == 200:
            reports_data = response.json()
            total_reports = reports_data.get('total', 0)
            tests.append(("✅ 报告列表API", f"总报告数: {total_reports}"))
        else:
            tests.append(("❌ 报告列表API", f"状态码: {response.status_code}"))
    except Exception as e:
        tests.append(("❌ 报告列表API", f"错误: {str(e)}"))
    
    # 测试7: 报告详情页面
    try:
        response = requests.get(f"{base_url}/reports/1")
        if response.status_code == 200 and "<!DOCTYPE html>" in response.text:
            tests.append(("✅ 报告详情页面", "正常"))
        else:
            tests.append(("❌ 报告详情页面", f"状态码: {response.status_code}"))
    except Exception as e:
        tests.append(("❌ 报告详情页面", f"错误: {str(e)}"))
    
    # 测试8: 分析中心页面
    try:
        response = requests.get(f"{base_url}/analysis")
        if response.status_code == 200 and "<!DOCTYPE html>" in response.text:
            tests.append(("✅ 分析中心页面", "正常"))
        else:
            tests.append(("❌ 分析中心页面", f"状态码: {response.status_code}"))
    except Exception as e:
        tests.append(("❌ 分析中心页面", f"错误: {str(e)}"))
    
    # 测试9: 系统设置页面
    try:
        response = requests.get(f"{base_url}/settings")
        if response.status_code == 200 and "<!DOCTYPE html>" in response.text:
            tests.append(("✅ 系统设置页面", "正常"))
        else:
            tests.append(("❌ 系统设置页面", f"状态码: {response.status_code}"))
    except Exception as e:
        tests.append(("❌ 系统设置页面", f"错误: {str(e)}"))
    
    # 测试10: 系统仪表盘页面
    try:
        response = requests.get(f"{base_url}/dashboard")
        if response.status_code == 200 and "<!DOCTYPE html>" in response.text:
            tests.append(("✅ 系统仪表盘页面", "正常"))
        else:
            tests.append(("❌ 系统仪表盘页面", f"状态码: {response.status_code}"))
    except Exception as e:
        tests.append(("❌ 系统仪表盘页面", f"错误: {str(e)}"))
    
    # 测试11: 系统统计API
    try:
        response = requests.get(f"{base_url}/api/system/stats")
        if response.status_code == 200:
            stats = response.json()
            cpu_percent = stats.get('cpu_percent', 0)
            tests.append(("✅ 系统统计API", f"CPU使用率: {cpu_percent}%"))
        else:
            tests.append(("❌ 系统统计API", f"状态码: {response.status_code}"))
    except Exception as e:
        tests.append(("❌ 系统统计API", f"错误: {str(e)}"))
    
    # 测试12: 仪表盘概览API
    try:
        response = requests.get(f"{base_url}/api/dashboard/overview")
        if response.status_code == 200:
            overview = response.json()
            total_reports = overview.get('reports', {}).get('total', 0)
            tests.append(("✅ 仪表盘概览API", f"报告总数: {total_reports}"))
        else:
            tests.append(("❌ 仪表盘概览API", f"状态码: {response.status_code}"))
    except Exception as e:
        tests.append(("❌ 仪表盘概览API", f"错误: {str(e)}"))
    
    # 测试13: 仪表盘图表API
    try:
        response = requests.get(f"{base_url}/api/dashboard/charts")
        if response.status_code == 200:
            charts = response.json()
            chart_count = len(charts.keys())
            tests.append(("✅ 仪表盘图表API", f"图表类型数: {chart_count}"))
        else:
            tests.append(("❌ 仪表盘图表API", f"状态码: {response.status_code}"))
    except Exception as e:
        tests.append(("❌ 仪表盘图表API", f"错误: {str(e)}"))
    
    # 测试14: 用户管理页面
    try:
        response = requests.get(f"{base_url}/users")
        if response.status_code == 200 and "<!DOCTYPE html>" in response.text:
            tests.append(("✅ 用户管理页面", "正常"))
        else:
            tests.append(("❌ 用户管理页面", f"状态码: {response.status_code}"))
    except Exception as e:
        tests.append(("❌ 用户管理页面", f"错误: {str(e)}"))
    
    # 测试15: 综合API文档页面
    try:
        response = requests.get(f"{base_url}/api-docs")
        if response.status_code == 200 and "<!DOCTYPE html>" in response.text:
            tests.append(("✅ 综合API文档", "正常"))
        else:
            tests.append(("❌ 综合API文档", f"状态码: {response.status_code}"))
    except Exception as e:
        tests.append(("❌ 综合API文档", f"错误: {str(e)}"))
    
    # 测试16: Swagger API文档页面
    try:
        response = requests.get(f"{base_url}/docs")
        if response.status_code == 200:
            tests.append(("✅ Swagger API文档", "可访问"))
        else:
            tests.append(("❌ Swagger API文档", f"状态码: {response.status_code}"))
    except Exception as e:
        tests.append(("❌ Swagger API文档", f"错误: {str(e)}"))
    
    # 打印测试结果
    print(f"📊 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    success_count = 0
    for test_name, result in tests:
        print(f"{test_name}: {result}")
        if "✅" in test_name:
            success_count += 1
    
    print("=" * 50)
    print(f"📈 测试结果: {success_count}/{len(tests)} 项通过")
    
    if success_count == len(tests):
        print("🎉 所有功能测试通过！Web系统运行正常。")
    else:
        print("⚠️  部分功能存在问题，请检查日志。")
    
    return success_count == len(tests)

def show_system_urls():
    """显示系统访问链接"""
    print("\n🔗 系统访问链接:")
    print("=" * 50)
    print("🏠 主页: http://localhost:8000")
    print("📋 报告管理: http://localhost:8000/reports")
    print("📊 分析中心: http://localhost:8000/analysis")
    print("⚙️ 系统设置: http://localhost:8000/settings")
    print("🎛️ 系统仪表盘: http://localhost:8000/dashboard")
    print("👥 用户管理: http://localhost:8000/users")
    print("📖 综合API文档: http://localhost:8000/api-docs")
    print("⚡ Swagger API文档: http://localhost:8000/docs")
    print("🔄 图表数据: http://localhost:8000/charts")
    print("ℹ️ 系统信息: http://localhost:8000/api/info")
    print("📊 系统统计: http://localhost:8000/api/system/stats")
    print("🎯 仪表盘概览: http://localhost:8000/api/dashboard/overview")
    print("📈 仪表盘图表: http://localhost:8000/api/dashboard/charts")
    print("=" * 50)

def show_feature_summary():
    """显示功能模块摘要"""
    print("\n🎯 功能模块摘要:")
    print("=" * 50)
    print("📊 主页模块:")
    print("   - 系统概览和状态展示")
    print("   - 实时图表可视化")
    print("   - 功能模块导航")
    print("")
    print("📋 报告管理模块:")
    print("   - 报告列表查看和筛选")
    print("   - 报告详情查看")
    print("   - 报告生成和下载")
    print("")
    print("📈 分析中心模块:")
    print("   - 多种分析工具")
    print("   - 数据上传分析")
    print("   - 数据库连接分析")
    print("")
    print("🎛️ 系统仪表盘模块:")
    print("   - 系统性能监控（CPU、内存、磁盘）")
    print("   - 业务数据统计")
    print("   - 实时活动监控")
    print("   - 快捷操作入口")
    print("")
    print("👥 用户管理模块:")
    print("   - 用户列表查看")
    print("   - 用户创建和编辑")
    print("   - 权限管理")
    print("   - 用户统计")
    print("")
    print("⚙️ 系统设置模块:")
    print("   - 常规设置配置")
    print("   - 报告设置管理")
    print("   - 安全设置")
    print("   - 系统信息查看")
    print("")
    print("📡 API接口:")
    print("   - RESTful API设计")
    print("   - 实时数据接口")
    print("   - 系统监控接口")
    print("   - 自动生成文档")
    print("=" * 50)

def show_new_features():
    """显示最新功能特性"""
    print("\n🆕 最新功能特性:")
    print("=" * 50)
    print("🎛️ 全新系统仪表盘:")
    print("   ✅ 实时系统资源监控（CPU、内存、磁盘）")
    print("   ✅ 环形进度图表显示")
    print("   ✅ 业务数据统计卡片")
    print("   ✅ 用户活跃度趋势图")
    print("   ✅ 报告类型分布图")
    print("   ✅ 实时活动动态")
    print("   ✅ 快捷操作面板")
    print("")
    print("👥 用户管理系统:")
    print("   ✅ 用户列表展示")
    print("   ✅ 用户角色管理（admin、analyst、viewer）")
    print("   ✅ 用户创建和编辑")
    print("   ✅ 用户搜索和筛选")
    print("   ✅ 用户统计信息")
    print("   ✅ 模态框界面设计")
    print("")
    print("📊 系统监控增强:")
    print("   ✅ 系统性能统计API")
    print("   ✅ 仪表盘概览数据API")
    print("   ✅ 仪表盘图表数据API")
    print("   ✅ 实时数据刷新")
    print("   ✅ psutil系统监控集成")
    print("")
    print("🎨 界面设计优化:")
    print("   ✅ 渐变色彩设计")
    print("   ✅ 卡片悬停效果")
    print("   ✅ 响应式布局")
    print("   ✅ 图标统一设计")
    print("   ✅ 现代化UI风格")
    print("=" * 50)

if __name__ == "__main__":
    print("🚀 Web系统功能测试")
    print("=" * 50)
    
    # 等待服务启动
    print("⏳ 等待Web服务启动...")
    time.sleep(2)
    
    # 运行测试
    success = test_web_system()
    
    # 显示访问链接
    show_system_urls()
    
    # 显示功能摘要
    show_feature_summary()
    
    # 显示最新功能
    show_new_features()
    
    if success:
        print("\n💡 提示: 在浏览器中打开主页链接查看完整的模块化界面！")
        print("🎉 系统已升级为完整的多模块分析平台！")
        print("🔥 新增系统仪表盘和用户管理功能！")
    else:
        print("\n🔧 如有问题，请检查服务是否正在运行: ps aux | grep web_interface") 