#!/usr/bin/env python3
"""
Gemini CLI 多模态示例
演示如何使用图像输入生成代码
"""

import subprocess
import os

def generate_code_from_image():
    """从UI设计图生成前端代码"""
    commands = [
        # 从设计图生成React组件
        "gemini-cli code --image design.png --output component.jsx",
        
        # 从流程图生成算法
        "gemini-cli code --image flowchart.jpg --lang python",
        
        # 从手绘草图生成HTML
        "gemini-cli code --image sketch.jpg --format html+css"
    ]
    
    for cmd in commands:
        print(f"执行: {cmd}")
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            print(f"结果: {result.stdout}")
        except Exception as e:
            print(f"错误: {e}")

def batch_process_images():
    """批量处理多个设计图"""
    image_dir = "./designs"
    output_dir = "./generated_code"
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 批量处理
    cmd = f"gemini-cli batch --input-dir {image_dir} --operation code-gen --output-dir {output_dir}"
    print(f"批量处理: {cmd}")
    subprocess.run(cmd, shell=True)

if __name__ == "__main__":
    print("Gemini CLI 多模态代码生成示例")
    print("-" * 40)
    generate_code_from_image()
    print("\n批量处理模式:")
    batch_process_images()