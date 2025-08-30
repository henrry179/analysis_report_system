#!/usr/bin/env python3
"""
Qwen Code 中文编程示例
演示通义千问代码的中文编程支持功能
创建时间: 2025年8月19日
版本: 1.0.0
"""

import subprocess
import json

class QwenCodeDemo:
    """Qwen Code 演示类"""
    
    def __init__(self):
        self.examples = []
    
    def 生成算法代码(self):
        """使用中文描述生成算法"""
        commands = [
            {
                "描述": "生成冒泡排序算法",
                "命令": 'qwen-code generate --desc "实现一个冒泡排序算法" --lang python'
            },
            {
                "描述": "生成二叉树遍历",
                "命令": 'qwen-code generate --desc "实现二叉树的前序、中序、后序遍历" --lang java'
            },
            {
                "描述": "生成动态规划解法",
                "命令": 'qwen-code generate --desc "用动态规划解决背包问题" --lang python'
            }
        ]
        
        for cmd_info in commands:
            print(f"\n{cmd_info['描述']}:")
            print(f"命令: {cmd_info['命令']}")
            # 实际执行时取消注释
            # result = subprocess.run(cmd_info['命令'], shell=True, capture_output=True, text=True)
            # print(f"结果: {result.stdout}")
    
    def 代码翻译示例(self):
        """代码和注释翻译"""
        print("\n=== 代码翻译功能 ===")
        
        翻译任务 = [
            "qwen-code translate --file english_code.py --target zh --add-comments",
            "qwen-code translate --file chinese_vars.js --target en --rename-vars",
            "qwen-code translate --file README.md --from en --to zh"
        ]
        
        for 任务 in 翻译任务:
            print(f"执行: {任务}")
    
    def 企业级应用生成(self):
        """生成企业级应用代码"""
        print("\n=== 企业级应用生成 ===")
        
        应用描述 = """
        qwen-code create-project --name "订单管理系统" \\
          --architecture microservices \\
          --services "用户服务,订单服务,支付服务,库存服务" \\
          --tech "spring-cloud,dubbo,nacos"
        """
        
        print("生成微服务架构:")
        print(应用描述)
        
        # 数据处理脚本
        数据处理 = """
        qwen-code generate --desc "
        从多个Excel文件中：
        1. 读取销售数据
        2. 清洗和合并数据
        3. 计算各类统计指标
        4. 生成可视化报表
        " --lang python --libs "pandas,matplotlib,openpyxl"
        """
        
        print("\n生成数据处理脚本:")
        print(数据处理)
    
    def 阿里巴巴代码规范(self):
        """应用阿里巴巴代码规范"""
        print("\n=== 阿里巴巴代码规范 ===")
        
        规范检查 = [
            "应用P3C规范: qwen-code format --file App.java --standard p3c",
            "代码审查: qwen-code review --file project/ --standard alibaba",
            "规范检查: qwen-code lint --project . --standard alibaba"
        ]
        
        for 检查 in 规范检查:
            print(f"• {检查}")
    
    def 教学功能演示(self):
        """中文编程教学功能"""
        print("\n=== 中文编程教学 ===")
        
        教学示例 = {
            "生成教学代码": 'qwen-code teach --topic "递归算法" --level beginner --lang python',
            "生成练习题": 'qwen-code exercise --topic "数据结构" --difficulty medium',
            "生成解释文档": 'qwen-code explain --file complex.py --lang zh'
        }
        
        for 功能, 命令 in 教学示例.items():
            print(f"\n{功能}:")
            print(f"  {命令}")

def main():
    """主函数"""
    print("=" * 60)
    print("Qwen Code (通义千问代码) 中文编程示例")
    print("=" * 60)
    
    demo = QwenCodeDemo()
    
    # 运行各个示例
    demo.生成算法代码()
    demo.代码翻译示例()
    demo.企业级应用生成()
    demo.阿里巴巴代码规范()
    demo.教学功能演示()
    
    print("\n" + "=" * 60)
    print("示例演示完成！")
    print("更多功能请查看文档: docs/qwen-code.md")

if __name__ == "__main__":
    main()