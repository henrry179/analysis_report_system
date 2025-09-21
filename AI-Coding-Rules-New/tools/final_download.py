#!/usr/bin/env python3
"""
Qwen Coder 最终下载脚本
"""

import time
from huggingface_hub import snapshot_download

print('🤖 Qwen Coder 模型下载器')
print('=' * 50)
print('🎯 下载: Qwen/Qwen2.5-Coder-7B-Instruct')
print('📍 保存: D:\\Gitstars\\models\\QwenCoder')
print('💾 大小: ~15GB')
print()
print('🚀 开始下载...')
print('💡 提示: 可以最小化窗口，下载完成后会有提示')
print()

start_time = time.time()
downloaded_path = snapshot_download(
    repo_id='Qwen/Qwen2.5-Coder-7B-Instruct',
    local_dir='D:\\Gitstars\\models\\QwenCoder',
    local_dir_use_symlinks=False,
    resume_download=True,
    max_workers=4
)

elapsed = time.time() - start_time
print(f'\n✅ 下载完成! 耗时: {elapsed:.1f}秒')
print(f'📁 保存位置: {downloaded_path}')
print()
print('🎉 Qwen Coder 模型下载成功！')
print()
print('📋 下一步:')
print('1. cd D:\\Gitstars\\QwenCoder-Project')
print('2. python qwen_coder.py --model "D:\\Gitstars\\models\\QwenCoder"')
print('3. 开始使用AI编程助手！')
