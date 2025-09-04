#!/usr/bin/env python3
"""
Qwen Coder 模型下载脚本
下载通义千问Qwen2.5-Coder模型到本地

作者: QWCoder Team
版本: 1.0.0
"""

import os
import sys
import time
import threading
import requests
from pathlib import Path
from huggingface_hub import snapshot_download, HfApi
import logging
from tqdm import tqdm

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('qwen_model_download.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class DownloadProgress:
    """自定义下载进度跟踪器"""

    def __init__(self, total_size=None):
        self.total_size = total_size
        self.downloaded = 0
        self.start_time = time.time()
        self.speed_history = []
        self.last_update = self.start_time

    def update(self, chunk_size):
        """更新下载进度"""
        self.downloaded += chunk_size
        current_time = time.time()

        # 计算速度 (每秒字节)
        time_diff = current_time - self.last_update
        if time_diff > 1:  # 每秒更新一次
            speed = chunk_size / time_diff
            self.speed_history.append(speed)
            if len(self.speed_history) > 10:  # 保留最近10个速度记录
                self.speed_history.pop(0)

            self.last_update = current_time
            self.display_progress()

    def display_progress(self):
        """显示进度条"""
        elapsed = time.time() - self.start_time

        if self.total_size:
            percent = min(100, (self.downloaded / self.total_size) * 100)
            bar_length = 50
            filled_length = int(bar_length * percent / 100)
            bar = '█' * filled_length + '░' * (bar_length - filled_length)

            # 计算剩余时间
            if self.speed_history:
                avg_speed = sum(self.speed_history) / len(self.speed_history)
                if avg_speed > 0:
                    remaining = (self.total_size - self.downloaded) / avg_speed
                    eta = f"{remaining/60:.1f}min"
                else:
                    eta = "未知"
            else:
                eta = "计算中..."

            # 显示进度
            sys.stdout.write(f'\r📥 [{bar}] {percent:.1f}% | {self._format_bytes(self.downloaded)}/{self._format_bytes(self.total_size)} | {eta}')
        else:
            # 未知总大小时显示简单进度
            sys.stdout.write(f'\r📥 已下载: {self._format_bytes(self.downloaded)} | 耗时: {elapsed:.1f}s')
        sys.stdout.flush()

    def _format_bytes(self, bytes):
        """格式化字节数"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes < 1024.0:
                return f"{bytes:.1f}{unit}"
            bytes /= 1024.0
        return f"{bytes:.1f}TB"

    def finish(self):
        """完成下载"""
        elapsed = time.time() - self.start_time
        print(f"\n✅ 下载完成! 总耗时: {elapsed:.1f}秒")
        if self.speed_history:
            avg_speed = sum(self.speed_history) / len(self.speed_history)
            print(f"📊 平均速度: {self._format_bytes(avg_speed)}/s")

def check_environment():
    """检查运行环境"""
    print("🔍 检查运行环境...")

    # 检查Python版本
    if sys.version_info < (3, 8):
        logger.error("❌ 需要Python 3.8或更高版本")
        return False

    print(f"✅ Python版本: {sys.version}")

    # 检查网络连接
    try:
        response = requests.get("https://huggingface.co", timeout=10)
        if response.status_code == 200:
            print("✅ 网络连接正常")
        else:
            logger.warning("⚠️ 网络连接可能不稳定")
    except:
        logger.error("❌ 无法连接到Hugging Face")
        return False

    return True

def check_disk_space(path, required_gb=20):
    """检查磁盘空间"""
    try:
        stat = os.statvfs(path)
        free_gb = (stat.f_bavail * stat.f_frsize) / (1024**3)
        if free_gb < required_gb:
            logger.error(".1f"            return False
        print(".1f"        return True
    except:
        # Windows兼容性
        try:
            import shutil
            total, used, free = shutil.disk_usage(path)
            free_gb = free / (1024**3)
            if free_gb < required_gb:
                logger.error(".1f"                return False
            print(".1f"            return True
        except:
            logger.warning("⚠️ 无法检查磁盘空间，请确保有足够空间")
            return True

def download_model(model_id, save_path, resume_download=True):
    """下载模型"""
    print(f"📥 开始下载模型: {model_id}")
    print(f"📍 保存路径: {save_path}")

    start_time = time.time()

    try:
        # 使用Hugging Face Hub下载
        api = HfApi()

        # 获取模型信息
        model_info = api.model_info(model_id)
        print(f"  📊 模型大小: {model_info.size_in_bytes / (1024**3):.1f} GB" if hasattr(model_info, 'size_in_bytes') and model_info.size_in_bytes else "  📊 模型大小: Unknown")
        print(f"  🔗 下载地址: https://huggingface.co/{model_id}")
        print(f"  📅 更新时间: {model_info.last_modified}")
        print()

        # 初始化进度跟踪器
        progress_tracker = DownloadProgress()
        print("🚀 开始下载，请耐心等待...")
        print("💡 提示: 下载过程中可以最小化窗口，下载完成后会有提示")
        print()

        # 开始下载
        downloaded_path = snapshot_download(
            repo_id=model_id,
            local_dir=save_path,
            local_dir_use_symlinks=False,
            resume_download=resume_download,
            max_workers=4,  # 增加并行下载数
        )

        # 完成下载
        progress_tracker.finish()
        download_time = time.time() - start_time
        print(f"📁 文件保存位置: {downloaded_path}")

        return downloaded_path

    except Exception as e:
        logger.error(f"❌ 下载失败: {e}")
        return None

def verify_download(save_path):
    """验证下载的文件"""
    print("🔍 验证下载文件...")

    required_files = [
        "config.json",
        "tokenizer.json",
        "tokenizer_config.json"
    ]

    missing_files = []
    for file in required_files:
        if not os.path.exists(os.path.join(save_path, file)):
            missing_files.append(file)

    if missing_files:
        logger.error(f"❌ 缺少必要文件: {', '.join(missing_files)}")
        return False

    # 检查模型文件
    model_files = [f for f in os.listdir(save_path) if f.endswith(('.safetensors', '.bin', '.pth'))]
    if not model_files:
        logger.warning("⚠️ 未找到模型权重文件，可能仍在下载中")

    print(f"✅ 验证完成，发现 {len(model_files)} 个模型文件")
    return True

def create_model_info(save_path, model_id):
    """创建模型信息文件"""
    info_file = os.path.join(save_path, "model_info.txt")

    info_content = f"""Qwen Coder 模型信息
==================

模型名称: {model_id}
下载时间: {time.strftime('%Y-%m-%d %H:%M:%S')}
保存路径: {save_path}

使用方法:
1. 在Python中加载:
   from transformers import AutoTokenizer, AutoModelForCausalLM
   tokenizer = AutoTokenizer.from_pretrained("{save_path}")
   model = AutoModelForCausalLM.from_pretrained("{save_path}")

2. 使用QwenCoder-Project:
   python qwen_coder.py --model "{save_path}"

注意事项:
- 确保有足够的RAM (建议16GB+)
- GPU使用会显著提升性能
- 首次加载模型可能需要几分钟

如有问题，请查看日志文件: qwen_model_download.log
"""

    try:
        with open(info_file, 'w', encoding='utf-8') as f:
            f.write(info_content)
        print(f"📝 已创建模型信息文件: {info_file}")
    except Exception as e:
        logger.warning(f"⚠️ 无法创建信息文件: {e}")

def main():
    print("🤖 Qwen Coder 模型下载器")
    print("=" * 50)

    # 配置参数
    model_id = "Qwen/Qwen2.5-Coder-7B-Instruct"
    save_path = r"D:\Gitstars\models\QwenCoder"

    print(f"🎯 目标模型: {model_id}")
    print(f"📍 保存路径: {save_path}")
    print()

    # 检查环境
    if not check_environment():
        return 1

    # 检查磁盘空间
    if not check_disk_space(save_path, required_gb=20):
        return 1

    # 确认下载
    print("⚠️  即将开始下载，模型文件较大(约15GB)")
    try:
        confirm = input("是否继续? (y/N): ").strip().lower()
        if confirm not in ['y', 'yes']:
            print("❌ 用户取消下载")
            return 0
    except KeyboardInterrupt:
        print("\n❌ 用户中断下载")
        return 0

    print()

    # 开始下载
    downloaded_path = download_model(model_id, save_path)

    if downloaded_path:
        # 验证下载
        if verify_download(downloaded_path):
            # 创建信息文件
            create_model_info(downloaded_path, model_id)

            print()
            print("🎉 模型下载和验证全部完成！")
            print()
            print("📋 下一步:")
            print("1. 返回QwenCoder-Project目录")
            print("2. 运行: python qwen_coder.py --model \"{save_path}\"")
            print("3. 享受AI编程助手！")
            return 0
        else:
            logger.error("❌ 下载验证失败")
            return 1
    else:
        logger.error("❌ 下载失败")
        return 1

if __name__ == "__main__":
    sys.exit(main())
