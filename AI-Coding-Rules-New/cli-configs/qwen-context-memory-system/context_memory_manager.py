#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Qwen Coder Context Memory Manager
=================================

一个用于管理Qwen Coder提示词上下文记忆的系统，支持每日维护更新。

功能:
- 保存和加载对话上下文
- 按日期维护上下文记忆
- 支持添加、更新和检索上下文
- 自动生成上下文摘要
- 提供上下文清理功能

使用方法:
1. 将此脚本保存为 context_memory_manager.py
2. 在命令行中运行: python context_memory_manager.py --help
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional


# 默认配置
DEFAULT_MEMORY_DIR = "qwen_context_memory"
DEFAULT_MEMORY_FILE = "context_memory.json"
DEFAULT_SESSIONS_DIR = "sessions"


class ContextMemoryManager:
    def __init__(self, memory_dir: str = DEFAULT_MEMORY_DIR):
        self.memory_dir = memory_dir
        self.memory_file = os.path.join(memory_dir, DEFAULT_MEMORY_FILE)
        self.sessions_dir = os.path.join(memory_dir, DEFAULT_SESSIONS_DIR)
        self._ensure_directories_exist()
        self.memory_data = self._load_memory_data()
    
    def _ensure_directories_exist(self):
        """确保必要的目录存在"""
        os.makedirs(self.memory_dir, exist_ok=True)
        os.makedirs(self.sessions_dir, exist_ok=True)
    
    def _load_memory_data(self) -> Dict[str, Any]:
        """加载内存数据"""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"警告: 无法读取内存文件 {self.memory_file}: {e}")
                return self._get_default_memory_data()
        else:
            return self._get_default_memory_data()
    
    def _get_default_memory_data(self) -> Dict[str, Any]:
        """获取默认内存数据结构"""
        return {
            "version": "1.0",
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "total_sessions": 0,
            "sessions": {}
        }
    
    def _save_memory_data(self):
        """保存内存数据到文件"""
        self.memory_data["last_updated"] = datetime.now().isoformat()
        try:
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(self.memory_data, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"错误: 无法写入内存文件 {self.memory_file}: {e}")
    
    def create_session(self, session_id: Optional[str] = None, description: str = "") -> str:
        """创建新会话"""
        if session_id is None:
            session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 创建会话目录
        session_dir = os.path.join(self.sessions_dir, session_id)
        os.makedirs(session_dir, exist_ok=True)
        
        # 初始化会话数据
        session_data = {
            "session_id": session_id,
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "description": description,
            "contexts": [],
            "summary": ""
        }
        
        # 保存会话数据
        session_file = os.path.join(session_dir, "session_data.json")
        try:
            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"错误: 无法创建会话文件 {session_file}: {e}")
            return ""
        
        # 更新主内存数据
        today = datetime.now().strftime("%Y-%m-%d")
        if today not in self.memory_data["sessions"]:
            self.memory_data["sessions"][today] = []
        
        self.memory_data["sessions"][today].append({
            "session_id": session_id,
            "created_at": session_data["created_at"],
            "description": description
        })
        self.memory_data["total_sessions"] += 1
        
        self._save_memory_data()
        print(f"已创建新会话: {session_id}")
        return session_id
    
    def add_context(self, session_id: str, prompt: str, response: str, 
                   metadata: Optional[Dict[str, Any]] = None) -> bool:
        """添加上下文到指定会话"""
        session_dir = os.path.join(self.sessions_dir, session_id)
        session_file = os.path.join(session_dir, "session_data.json")
        
        if not os.path.exists(session_file):
            print(f"错误: 会话 {session_id} 不存在")
            return False
        
        # 加载会话数据
        try:
            with open(session_file, 'r', encoding='utf-8') as f:
                session_data = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"错误: 无法读取会话文件 {session_file}: {e}")
            return False
        
        # 添加新的上下文
        context_entry = {
            "timestamp": datetime.now().isoformat(),
            "prompt": prompt,
            "response": response,
            "metadata": metadata or {}
        }
        
        session_data["contexts"].append(context_entry)
        session_data["last_updated"] = datetime.now().isoformat()
        
        # 保存更新后的会话数据
        try:
            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"错误: 无法更新会话文件 {session_file}: {e}")
            return False
        
        print(f"已添加上下文到会话 {session_id}")
        return True
    
    def get_session_contexts(self, session_id: str) -> List[Dict[str, Any]]:
        """获取指定会话的所有上下文"""
        session_dir = os.path.join(self.sessions_dir, session_id)
        session_file = os.path.join(session_dir, "session_data.json")
        
        if not os.path.exists(session_file):
            print(f"错误: 会话 {session_id} 不存在")
            return []
        
        try:
            with open(session_file, 'r', encoding='utf-8') as f:
                session_data = json.load(f)
            return session_data.get("contexts", [])
        except (json.JSONDecodeError, IOError) as e:
            print(f"错误: 无法读取会话文件 {session_file}: {e}")
            return []
    
    def generate_session_summary(self, session_id: str) -> str:
        """为指定会话生成摘要"""
        contexts = self.get_session_contexts(session_id)
        if not contexts:
            return "无上下文数据"
        
        # 简单的摘要生成 - 实际应用中可以使用AI模型生成更智能的摘要
        summary = f"会话 {session_id} 包含 {len(contexts)} 个交互:\n"
        for i, ctx in enumerate(contexts[-3:], 1):  # 只显示最近3个交互
            prompt_preview = ctx['prompt'][:50] + "..." if len(ctx['prompt']) > 50 else ctx['prompt']
            summary += f"{i}. {prompt_preview}\n"
        
        if len(contexts) > 3:
            summary += f"... 还有 {len(contexts) - 3} 个早期交互\n"
        
        # 更新会话摘要
        session_dir = os.path.join(self.sessions_dir, session_id)
        session_file = os.path.join(session_dir, "session_data.json")
        
        try:
            with open(session_file, 'r', encoding='utf-8') as f:
                session_data = json.load(f)
            
            session_data["summary"] = summary
            session_data["last_updated"] = datetime.now().isoformat()
            
            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, ensure_ascii=False, indent=2)
        except (json.JSONDecodeError, IOError) as e:
            print(f"警告: 无法更新会话摘要 {session_file}: {e}")
        
        return summary
    
    def list_sessions(self, date: Optional[str] = None) -> List[Dict[str, Any]]:
        """列出会话"""
        if date is None:
            # 返回所有会话
            all_sessions = []
            for date_key, sessions in self.memory_data["sessions"].items():
                for session in sessions:
                    session["date"] = date_key
                    all_sessions.append(session)
            return all_sessions
        else:
            # 返回指定日期的会话
            return self.memory_data["sessions"].get(date, [])
    
    def get_todays_sessions(self) -> List[Dict[str, Any]]:
        """获取今天的会话"""
        today = datetime.now().strftime("%Y-%m-%d")
        return self.list_sessions(today)
    
    def cleanup_old_sessions(self, days_to_keep: int = 30) -> int:
        """清理旧会话"""
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        deleted_count = 0
        
        for date_str, sessions in list(self.memory_data["sessions"].items()):
            try:
                session_date = datetime.fromisoformat(date_str)
                if session_date < cutoff_date:
                    # 删除会话目录
                    for session in sessions:
                        session_dir = os.path.join(self.sessions_dir, session["session_id"])
                        if os.path.exists(session_dir):
                            import shutil
                            shutil.rmtree(session_dir)
                            deleted_count += 1
                    
                    # 从内存数据中移除
                    del self.memory_data["sessions"][date_str]
            except ValueError:
                # 日期格式不正确，跳过
                continue
        
        self._save_memory_data()
        return deleted_count
    
    def print_memory_summary(self):
        """打印内存摘要"""
        print("\n" + "="*60)
        print("Qwen Coder 上下文记忆系统摘要")
        print("="*60)
        print(f"系统版本: {self.memory_data['version']}")
        print(f"创建时间: {self.memory_data['created_at']}")
        print(f"最后更新: {self.memory_data['last_updated']}")
        print(f"总会话数: {self.memory_data['total_sessions']}")
        
        today_sessions = self.get_todays_sessions()
        print(f"今日会话数: {len(today_sessions)}")
        
        if today_sessions:
            print("\n今日会话:")
            for session in today_sessions:
                print(f"- {session['session_id']}: {session['description']}")
        
        print("="*60)


def main():
    parser = argparse.ArgumentParser(
        description="Qwen Coder Context Memory Manager - 管理Qwen Coder提示词上下文记忆",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  1. 创建新会话:
     python context_memory_manager.py --create-session --description "代码生成任务"
  
  2. 添加上下文到会话:
     python context_memory_manager.py --add-context --session-id 20250903_143022 --prompt "帮我写一个Python函数" --response "好的，这是一个Python函数..."
  
  3. 查看会话上下文:
     python context_memory_manager.py --view-context --session-id 20250903_143022
  
  4. 生成会话摘要:
     python context_memory_manager.py --generate-summary --session-id 20250903_143022
  
  5. 查看今日会话:
     python context_memory_manager.py --today
  
  6. 查看内存摘要:
     python context_memory_manager.py --summary
  
  7. 清理会话 (保留最近30天):
     python context_memory_manager.py --cleanup
        """
    )
    
    # 操作参数
    parser.add_argument('--create-session', action='store_true', 
                       help='创建新会话')
    parser.add_argument('--add-context', action='store_true', 
                       help='添加上下文到会话')
    parser.add_argument('--view-context', action='store_true', 
                       help='查看会话上下文')
    parser.add_argument('--generate-summary', action='store_true', 
                       help='生成会话摘要')
    parser.add_argument('--list-sessions', action='store_true', 
                       help='列出所有会话')
    parser.add_argument('--today', action='store_true', 
                       help='查看今日会话')
    parser.add_argument('--summary', action='store_true', 
                       help='显示内存摘要')
    parser.add_argument('--cleanup', action='store_true', 
                       help='清理旧会话 (默认保留30天)')
    
    # 参数
    parser.add_argument('--session-id', type=str, 
                       help='会话ID')
    parser.add_argument('--description', type=str, default="", 
                       help='会话描述')
    parser.add_argument('--prompt', type=str, 
                       help='提示词')
    parser.add_argument('--response', type=str, 
                       help='响应内容')
    parser.add_argument('--metadata', type=str, 
                       help='元数据 (JSON格式)')
    parser.add_argument('--date', type=str, 
                       help='指定日期 (YYYY-MM-DD)')
    parser.add_argument('--days-to-keep', type=int, default=30,
                       help='保留天数 (用于清理, 默认30天)')
    parser.add_argument('--memory-dir', type=str, default=DEFAULT_MEMORY_DIR,
                       help='内存目录路径')
    
    args = parser.parse_args()
    
    # 创建管理器实例
    manager = ContextMemoryManager(args.memory_dir)
    
    # 执行相应操作
    if args.create_session:
        session_id = manager.create_session(description=args.description)
        if session_id:
            print(f"会话ID: {session_id}")
    
    elif args.add_context:
        if not all([args.session_id, args.prompt, args.response]):
            print("错误: 使用 --add-context 时必须提供 --session-id, --prompt 和 --response 参数")
            sys.exit(1)
        
        metadata = None
        if args.metadata:
            try:
                metadata = json.loads(args.metadata)
            except json.JSONDecodeError:
                print("警告: 元数据不是有效的JSON格式")
        
        success = manager.add_context(args.session_id, args.prompt, args.response, metadata)
        if not success:
            sys.exit(1)
    
    elif args.view_context:
        if not args.session_id:
            print("错误: 使用 --view-context 时必须提供 --session-id 参数")
            sys.exit(1)
        
        contexts = manager.get_session_contexts(args.session_id)
        if contexts:
            print(f"\n会话 {args.session_id} 的上下文:")
            print("-" * 60)
            for i, ctx in enumerate(contexts, 1):
                print(f"交互 {i}:")
                print(f"时间: {ctx['timestamp']}")
                print(f"提示: {ctx['prompt']}")
                print(f"响应: {ctx['response']}")
                if ctx['metadata']:
                    print(f"元数据: {ctx['metadata']}")
                print("-" * 60)
        else:
            print(f"会话 {args.session_id} 无上下文数据或不存在")
    
    elif args.generate_summary:
        if not args.session_id:
            print("错误: 使用 --generate-summary 时必须提供 --session_id 参数")
            sys.exit(1)
        
        summary = manager.generate_session_summary(args.session_id)
        print(f"\n会话 {args.session_id} 的摘要:")
        print(summary)
    
    elif args.list_sessions:
        sessions = manager.list_sessions(args.date)
        if sessions:
            print(f"\n会话列表:")
            print("-" * 80)
            for session in sessions:
                date = session.get('date', 'N/A')
                print(f"日期: {date} | ID: {session['session_id']} | 描述: {session['description']}")
        else:
            print("无会话数据")
    
    elif args.today:
        sessions = manager.get_todays_sessions()
        if sessions:
            print(f"\n今日会话 ({datetime.now().strftime('%Y-%m-%d')}):")
            print("-" * 80)
            for session in sessions:
                print(f"ID: {session['session_id']} | 描述: {session['description']} | 创建时间: {session['created_at']}")
        else:
            print("今日无会话")
    
    elif args.summary:
        manager.print_memory_summary()
    
    elif args.cleanup:
        deleted_count = manager.cleanup_old_sessions(args.days_to_keep)
        print(f"已清理 {deleted_count} 个旧会话")
    
    else:
        # 默认显示摘要
        manager.print_memory_summary()


if __name__ == "__main__":
    main()