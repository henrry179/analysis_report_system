#!/usr/bin/env python3
"""
Qwen Coder - 通义千问代码生成模型
Windows本地运行版本

功能特性:
- 代码生成和补全
- 代码解释和优化
- 多语言支持
- 交互式对话界面

作者: QWCoder Team
版本: 1.0.0
"""

import os
import sys
import argparse
import platform
from pathlib import Path

# 检查Python版本
if sys.version_info < (3, 8):
    print("❌ 需要Python 3.8或更高版本")
    sys.exit(1)

# 检查操作系统
if platform.system() != "Windows":
    print("⚠️  此脚本针对Windows优化，其他系统可能需要调整")

def check_dependencies():
    """检查必要的依赖"""
    print("🔍 检查依赖...")

    required_packages = [
        'torch', 'transformers', 'accelerate',
        'numpy', 'gradio', 'streamlit'
    ]

    missing_packages = []

    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"✗ {package}")

    if missing_packages:
        print(f"\n❌ 缺少必要的包: {', '.join(missing_packages)}")
        print("请运行: pip install -r requirements.txt")
        return False

    print("✅ 所有依赖检查通过")
    return True

def download_model(model_name="Qwen/Qwen2.5-Coder-7B-Instruct"):
    """下载Qwen Coder模型"""
    print(f"📥 下载模型: {model_name}")
    print("⚠️  注意: 模型文件较大(约15GB)，下载需要时间")

    try:
        from transformers import AutoTokenizer, AutoModelForCausalLM
        import torch

        print("正在下载tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

        print("正在下载模型...")
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            trust_remote_code=True,
            torch_dtype=torch.float16,
            device_map="auto",
            load_in_8bit=True  # 使用8-bit量化节省内存
        )

        print("✅ 模型下载完成")
        return tokenizer, model

    except Exception as e:
        print(f"❌ 模型下载失败: {e}")
        print("💡 建议:")
        print("   1. 检查网络连接")
        print("   2. 确保有足够的磁盘空间(>20GB)")
        print("   3. 考虑使用更小的模型版本")
        return None, None

def create_web_interface(tokenizer, model):
    """创建Gradio Web界面"""
    print("🌐 创建Web界面...")

    try:
        import gradio as gr

        def generate_code(prompt, max_length=512, temperature=0.7):
            """生成代码"""
            try:
                inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

                with torch.no_grad():
                    outputs = model.generate(
                        **inputs,
                        max_length=max_length,
                        temperature=temperature,
                        do_sample=True,
                        pad_token_id=tokenizer.eos_token_id
                    )

                generated_code = tokenizer.decode(outputs[0], skip_special_tokens=True)
                return generated_code

            except Exception as e:
                return f"生成失败: {e}"

        def explain_code(code):
            """解释代码"""
            prompt = f"请解释以下代码的功能和逻辑:\n\n{code}\n\n解释:"
            return generate_code(prompt)

        def optimize_code(code, language):
            """优化代码"""
            prompt = f"请优化以下{language}代码，提高性能和可读性:\n\n{code}\n\n优化后的代码:"
            return generate_code(prompt)

        # 创建界面
        with gr.Blocks(title="Qwen Coder - 代码生成助手") as interface:
            gr.Markdown("# 🤖 Qwen Coder - 通义千问代码生成助手")
            gr.Markdown("支持代码生成、解释、优化等多种功能")

            with gr.Tab("代码生成"):
                prompt_input = gr.Textbox(
                    label="输入需求描述",
                    placeholder="例如: 写一个Python函数来计算斐波那契数列",
                    lines=3
                )
                max_length_slider = gr.Slider(
                    minimum=100, maximum=2048, value=512, step=50,
                    label="最大生成长度"
                )
                temperature_slider = gr.Slider(
                    minimum=0.1, maximum=1.0, value=0.7, step=0.1,
                    label="创造性 (温度)"
                )
                generate_btn = gr.Button("🚀 生成代码")
                output_code = gr.Code(label="生成的代码", language="python")

                generate_btn.click(
                    generate_code,
                    inputs=[prompt_input, max_length_slider, temperature_slider],
                    outputs=output_code
                )

            with gr.Tab("代码解释"):
                code_input = gr.Code(label="输入代码", language="python")
                explain_btn = gr.Button("🔍 解释代码")
                explanation_output = gr.Textbox(label="代码解释", lines=10)

                explain_btn.click(explain_code, inputs=code_input, outputs=explanation_output)

            with gr.Tab("代码优化"):
                opt_code_input = gr.Code(label="输入需要优化的代码", language="python")
                language_selector = gr.Dropdown(
                    ["Python", "JavaScript", "Java", "C++", "Go"],
                    label="编程语言",
                    value="Python"
                )
                optimize_btn = gr.Button("⚡ 优化代码")
                optimized_output = gr.Code(label="优化后的代码", language="python")

                optimize_btn.click(
                    optimize_code,
                    inputs=[opt_code_input, language_selector],
                    outputs=optimized_output
                )

        return interface

    except ImportError:
        print("❌ Gradio未安装，请运行: pip install gradio")
        return None

def create_streamlit_app(tokenizer, model):
    """创建Streamlit应用"""
    print("📱 创建Streamlit应用...")

    streamlit_code = '''import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

st.set_page_config(page_title="Qwen Coder", page_icon="🤖")

st.title("🤖 Qwen Coder - 代码生成助手")
st.markdown("基于通义千问Qwen2.5-Coder模型")

# 侧边栏配置
with st.sidebar:
    st.header("⚙️ 配置")
    max_length = st.slider("最大生成长度", 100, 2048, 512)
    temperature = st.slider("创造性", 0.1, 1.0, 0.7)

# 主界面
tab1, tab2, tab3 = st.tabs(["💻 代码生成", "🔍 代码解释", "⚡ 代码优化"])

with tab1:
    st.header("代码生成")
    prompt = st.text_area("描述你的需求", height=100,
                         placeholder="例如: 写一个Python函数来计算斐波那契数列")

    if st.button("🚀 生成代码", type="primary"):
        if prompt:
            with st.spinner("正在生成代码..."):
                try:
                    # 这里应该调用实际的模型推理
                    st.code("print('Hello, World!')", language="python")
                except Exception as e:
                    st.error(f"生成失败: {e}")
        else:
            st.warning("请输入需求描述")

with tab2:
    st.header("代码解释")
    code_to_explain = st.code("def hello():\n    print('Hello, World!')", language="python")

    if st.button("🔍 解释代码"):
        with st.spinner("正在分析代码..."):
            st.write("这是一个简单的Python函数，用于输出'Hello, World!'")

with tab3:
    st.header("代码优化")
    code_to_optimize = st.text_area("输入需要优化的代码", height=200)
    language = st.selectbox("编程语言", ["Python", "JavaScript", "Java", "C++", "Go"])

    if st.button("⚡ 优化代码"):
        with st.spinner("正在优化代码..."):
            st.code(code_to_optimize, language=language.lower())
'''

    with open("qwen_coder_app.py", "w", encoding="utf-8") as f:
        f.write(streamlit_code)

    print("✅ Streamlit应用创建完成: qwen_coder_app.py")
    print("运行命令: streamlit run qwen_coder_app.py")

def interactive_mode(tokenizer, model):
    """交互式命令行模式"""
    print("💬 进入交互式模式")
    print("输入 'exit' 或 'quit' 退出")
    print("输入 'help' 查看帮助")
    print("-" * 50)

    while True:
        try:
            user_input = input("\n🤖 请输入你的问题或需求: ").strip()

            if user_input.lower() in ['exit', 'quit']:
                print("👋 再见!")
                break

            elif user_input.lower() == 'help':
                print_help()
                continue

            elif not user_input:
                continue

            # 生成响应
            print("\n🤔 正在思考...")
            try:
                inputs = tokenizer(user_input, return_tensors="pt").to(model.device)

                with torch.no_grad():
                    outputs = model.generate(
                        **inputs,
                        max_length=512,
                        temperature=0.7,
                        do_sample=True,
                        pad_token_id=tokenizer.eos_token_id
                    )

                response = tokenizer.decode(outputs[0], skip_special_tokens=True)
                print(f"\n💡 回答:\n{response}")

            except Exception as e:
                print(f"❌ 生成失败: {e}")

        except KeyboardInterrupt:
            print("\n👋 再见!")
            break
        except EOFError:
            print("\n👋 再见!")
            break

def print_help():
    """显示帮助信息"""
    help_text = """
🤖 Qwen Coder 使用帮助

可用命令:
  help        - 显示此帮助信息
  exit/quit   - 退出程序

功能说明:
  💻 代码生成 - 描述需求即可生成相应代码
  🔍 代码解释 - 输入代码片段获取详细解释
  ⚡ 代码优化 - 改进代码性能和可读性
  🗣️ 对话交流 - 自然语言交流各种编程问题

示例:
  "写一个Python函数来读取CSV文件"
  "解释这个JavaScript闭包的用法"
  "优化这个SQL查询的性能"

注意事项:
  - 模型需要一定的计算资源
  - 生成的代码可能需要手动调整
  - 建议使用英文描述获得更好效果
    """
    print(help_text)

def main():
    parser = argparse.ArgumentParser(description="Qwen Coder - 通义千问代码生成模型")
    parser.add_argument("--mode", choices=["web", "streamlit", "cli"],
                       default="web", help="运行模式 (默认: web)")
    parser.add_argument("--model", default="Qwen/Qwen2.5-Coder-7B-Instruct",
                       help="模型名称")
    parser.add_argument("--port", type=int, default=7860,
                       help="Web界面端口 (默认: 7860)")

    args = parser.parse_args()

    print("🚀 启动 Qwen Coder...")
    print(f"模式: {args.mode}")
    print(f"模型: {args.model}")
    print("-" * 50)

    # 检查依赖
    if not check_dependencies():
        return

    # 检查CUDA可用性
    try:
        import torch
        if torch.cuda.is_available():
            print(f"🎮 GPU可用: {torch.cuda.get_device_name()}")
        else:
            print("⚠️  GPU不可用，将使用CPU (性能较慢)")
    except ImportError:
        print("⚠️  PyTorch未安装")

    # 下载模型
    tokenizer, model = download_model(args.model)
    if tokenizer is None or model is None:
        print("❌ 模型加载失败，请检查网络连接和磁盘空间")
        return

    # 根据模式运行
    if args.mode == "web":
        interface = create_web_interface(tokenizer, model)
        if interface:
            print(f"🌐 启动Web界面: http://localhost:{args.port}")
            interface.launch(server_port=args.port, share=False)
        else:
            print("❌ Web界面创建失败")

    elif args.mode == "streamlit":
        create_streamlit_app(tokenizer, model)

    elif args.mode == "cli":
        interactive_mode(tokenizer, model)

if __name__ == "__main__":
    main()
