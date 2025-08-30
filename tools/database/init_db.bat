@echo off
echo 正在初始化数据库...
python -c "from src.core.database import db_manager; db_manager.init_database(); print('数据库初始化完成')"
echo 数据库初始化完成
pause
