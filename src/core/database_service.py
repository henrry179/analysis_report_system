#!/usr/bin/env python3
"""
数据库服务模块
提供高层数据库操作接口，封装复杂的数据库操作
"""

import logging
from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc, func
from sqlalchemy.exc import IntegrityError

from .database import get_db
from .models import (
    UserDB, ReportDB, AnalysisTaskDB, DataSourceDB,
    UserSettingsDB, SystemLogDB, APIAccessLogDB
)

logger = logging.getLogger(__name__)

class UserService:
    """用户服务"""

    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[UserDB]:
        """根据用户名获取用户"""
        return db.query(UserDB).filter(UserDB.username == username).first()

    @staticmethod
    def get_user_by_id(db: Session, user_id: str) -> Optional[UserDB]:
        """根据用户ID获取用户"""
        return db.query(UserDB).filter(UserDB.id == user_id).first()

    @staticmethod
    def create_user(db: Session, user_data: Dict[str, Any]) -> UserDB:
        """创建用户"""
        try:
            db_user = UserDB(**user_data)
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            logger.info(f"用户创建成功: {db_user.username}")
            return db_user
        except IntegrityError as e:
            db.rollback()
            logger.error(f"用户创建失败（用户名或邮箱已存在）: {user_data.get('username')}")
            raise ValueError("用户名或邮箱已存在")
        except Exception as e:
            db.rollback()
            logger.error(f"用户创建失败: {str(e)}")
            raise

    @staticmethod
    def update_user(db: Session, user_id: str, update_data: Dict[str, Any]) -> Optional[UserDB]:
        """更新用户信息"""
        try:
            db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
            if not db_user:
                return None

            for key, value in update_data.items():
                if hasattr(db_user, key):
                    setattr(db_user, key, value)

            db.commit()
            db.refresh(db_user)
            logger.info(f"用户信息更新成功: {db_user.username}")
            return db_user
        except Exception as e:
            db.rollback()
            logger.error(f"用户信息更新失败: {str(e)}")
            raise

    @staticmethod
    def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> List[UserDB]:
        """获取所有用户"""
        return db.query(UserDB).offset(skip).limit(limit).all()


class ReportService:
    """报告服务"""

    @staticmethod
    def create_report(db: Session, report_data: Dict[str, Any]) -> ReportDB:
        """创建报告"""
        try:
            db_report = ReportDB(**report_data)
            db.add(db_report)
            db.commit()
            db.refresh(db_report)
            logger.info(f"报告创建成功: {db_report.title}")
            return db_report
        except Exception as e:
            db.rollback()
            logger.error(f"报告创建失败: {str(e)}")
            raise

    @staticmethod
    def get_report_by_id(db: Session, report_id: str) -> Optional[ReportDB]:
        """根据ID获取报告"""
        return db.query(ReportDB).filter(ReportDB.id == report_id).first()

    @staticmethod
    def get_reports_by_user(db: Session, user_id: str, skip: int = 0, limit: int = 100) -> List[ReportDB]:
        """获取用户的报告列表"""
        return db.query(ReportDB).filter(ReportDB.created_by_id == user_id)\
                .offset(skip).limit(limit).all()

    @staticmethod
    def get_reports_by_status(db: Session, status: str, skip: int = 0, limit: int = 100) -> List[ReportDB]:
        """根据状态获取报告列表"""
        return db.query(ReportDB).filter(ReportDB.status == status)\
                .offset(skip).limit(limit).all()

    @staticmethod
    def update_report_status(db: Session, report_id: str, status: str) -> Optional[ReportDB]:
        """更新报告状态"""
        try:
            db_report = db.query(ReportDB).filter(ReportDB.id == report_id).first()
            if not db_report:
                return None

            db_report.status = status
            db.commit()
            db.refresh(db_report)
            logger.info(f"报告状态更新成功: {db_report.title} -> {status}")
            return db_report
        except Exception as e:
            db.rollback()
            logger.error(f"报告状态更新失败: {str(e)}")
            raise

    @staticmethod
    def delete_report(db: Session, report_id: str) -> bool:
        """删除报告"""
        try:
            db_report = db.query(ReportDB).filter(ReportDB.id == report_id).first()
            if not db_report:
                return False

            db.delete(db_report)
            db.commit()
            logger.info(f"报告删除成功: {db_report.title}")
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"报告删除失败: {str(e)}")
            raise


class AnalysisTaskService:
    """分析任务服务"""

    @staticmethod
    def create_task(db: Session, task_data: Dict[str, Any]) -> AnalysisTaskDB:
        """创建分析任务"""
        try:
            db_task = AnalysisTaskDB(**task_data)
            db.add(db_task)
            db.commit()
            db.refresh(db_task)
            logger.info(f"分析任务创建成功: {db_task.task_name}")
            return db_task
        except Exception as e:
            db.rollback()
            logger.error(f"分析任务创建失败: {str(e)}")
            raise

    @staticmethod
    def get_task_by_id(db: Session, task_id: str) -> Optional[AnalysisTaskDB]:
        """根据ID获取任务"""
        return db.query(AnalysisTaskDB).filter(AnalysisTaskDB.id == task_id).first()

    @staticmethod
    def get_tasks_by_user(db: Session, user_id: str, status: Optional[str] = None,
                         skip: int = 0, limit: int = 100) -> List[AnalysisTaskDB]:
        """获取用户任务列表"""
        query = db.query(AnalysisTaskDB).filter(AnalysisTaskDB.created_by_id == user_id)
        if status:
            query = query.filter(AnalysisTaskDB.status == status)
        return query.order_by(desc(AnalysisTaskDB.created_at)).offset(skip).limit(limit).all()

    @staticmethod
    def update_task_status(db: Session, task_id: str, status: str,
                          progress: Optional[int] = None,
                          result: Optional[Dict[str, Any]] = None) -> Optional[AnalysisTaskDB]:
        """更新任务状态"""
        try:
            db_task = db.query(AnalysisTaskDB).filter(AnalysisTaskDB.id == task_id).first()
            if not db_task:
                return None

            db_task.status = status

            if progress is not None:
                db_task.progress = progress

            if result is not None:
                db_task.result = result

            if status in ['completed', 'failed']:
                db_task.completed_at = datetime.now()

            if status == 'running' and not db_task.started_at:
                db_task.started_at = datetime.now()

            db.commit()
            db.refresh(db_task)
            logger.info(f"任务状态更新成功: {db_task.task_name} -> {status}")
            return db_task
        except Exception as e:
            db.rollback()
            logger.error(f"任务状态更新失败: {str(e)}")
            raise


class DataSourceService:
    """数据源服务"""

    @staticmethod
    def create_data_source(db: Session, source_data: Dict[str, Any]) -> DataSourceDB:
        """创建数据源"""
        try:
            db_source = DataSourceDB(**source_data)
            db.add(db_source)
            db.commit()
            db.refresh(db_source)
            logger.info(f"数据源创建成功: {db_source.name}")
            return db_source
        except Exception as e:
            db.rollback()
            logger.error(f"数据源创建失败: {str(e)}")
            raise

    @staticmethod
    def get_data_source_by_id(db: Session, source_id: str) -> Optional[DataSourceDB]:
        """根据ID获取数据源"""
        return db.query(DataSourceDB).filter(DataSourceDB.id == source_id).first()

    @staticmethod
    def get_active_data_sources(db: Session, user_id: Optional[str] = None) -> List[DataSourceDB]:
        """获取活跃数据源"""
        query = db.query(DataSourceDB).filter(DataSourceDB.is_active == True)
        if user_id:
            query = query.filter(DataSourceDB.created_by_id == user_id)
        return query.all()

    @staticmethod
    def update_data_source(db: Session, source_id: str, update_data: Dict[str, Any]) -> Optional[DataSourceDB]:
        """更新数据源"""
        try:
            db_source = db.query(DataSourceDB).filter(DataSourceDB.id == source_id).first()
            if not db_source:
                return None

            for key, value in update_data.items():
                if hasattr(db_source, key):
                    setattr(db_source, key, value)

            db.commit()
            db.refresh(db_source)
            logger.info(f"数据源更新成功: {db_source.name}")
            return db_source
        except Exception as e:
            db.rollback()
            logger.error(f"数据源更新失败: {str(e)}")
            raise


class UserSettingsService:
    """用户设置服务"""

    @staticmethod
    def get_user_settings(db: Session, user_id: str) -> Optional[UserSettingsDB]:
        """获取用户设置"""
        return db.query(UserSettingsDB).filter(UserSettingsDB.user_id == user_id).first()

    @staticmethod
    def update_user_settings(db: Session, user_id: str, settings: Dict[str, Any]) -> UserSettingsDB:
        """更新用户设置"""
        try:
            db_settings = db.query(UserSettingsDB).filter(UserSettingsDB.user_id == user_id).first()

            if db_settings:
                db_settings.settings = settings
            else:
                db_settings = UserSettingsDB(user_id=user_id, settings=settings)
                db.add(db_settings)

            db.commit()
            db.refresh(db_settings)
            logger.info(f"用户设置更新成功: {user_id}")
            return db_settings
        except Exception as e:
            db.rollback()
            logger.error(f"用户设置更新失败: {str(e)}")
            raise


class SystemLogService:
    """系统日志服务"""

    @staticmethod
    def create_log(db: Session, level: str, message: str, module: Optional[str] = None,
                  user_id: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None):
        """创建系统日志"""
        try:
            log_data = {
                "level": level,
                "message": message,
                "module": module,
                "user_id": user_id,
                "metadata": metadata or {}
            }
            db_log = SystemLogDB(**log_data)
            db.add(db_log)
            db.commit()
            logger.debug(f"系统日志创建成功: {level} - {message}")
        except Exception as e:
            db.rollback()
            logger.error(f"系统日志创建失败: {str(e)}")

    @staticmethod
    def get_logs(db: Session, level: Optional[str] = None, module: Optional[str] = None,
                user_id: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[SystemLogDB]:
        """获取系统日志"""
        query = db.query(SystemLogDB)

        if level:
            query = query.filter(SystemLogDB.level == level)
        if module:
            query = query.filter(SystemLogDB.module == module)
        if user_id:
            query = query.filter(SystemLogDB.user_id == user_id)

        return query.order_by(desc(SystemLogDB.created_at)).offset(skip).limit(limit).all()


class APIAccessLogService:
    """API访问日志服务"""

    @staticmethod
    def create_access_log(db: Session, endpoint: str, method: str, status_code: int,
                         user_id: Optional[str] = None, response_time_ms: Optional[int] = None,
                         ip_address: Optional[str] = None, user_agent: Optional[str] = None):
        """创建API访问日志"""
        try:
            log_data = {
                "endpoint": endpoint,
                "method": method,
                "status_code": status_code,
                "user_id": user_id,
                "response_time_ms": response_time_ms,
                "ip_address": ip_address,
                "user_agent": user_agent
            }
            db_log = APIAccessLogDB(**log_data)
            db.add(db_log)
            db.commit()
            logger.debug(f"API访问日志创建成功: {method} {endpoint} {status_code}")
        except Exception as e:
            db.rollback()
            logger.error(f"API访问日志创建失败: {str(e)}")

    @staticmethod
    def get_access_logs(db: Session, endpoint: Optional[str] = None, method: Optional[str] = None,
                       user_id: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[APIAccessLogDB]:
        """获取API访问日志"""
        query = db.query(APIAccessLogDB)

        if endpoint:
            query = query.filter(APIAccessLogDB.endpoint == endpoint)
        if method:
            query = query.filter(APIAccessLogDB.method == method)
        if user_id:
            query = query.filter(APIAccessLogDB.user_id == user_id)

        return query.order_by(desc(APIAccessLogDB.created_at)).offset(skip).limit(limit).all()


# 全局服务实例
user_service = UserService()
report_service = ReportService()
analysis_task_service = AnalysisTaskService()
data_source_service = DataSourceService()
user_settings_service = UserSettingsService()
system_log_service = SystemLogService()
api_access_log_service = APIAccessLogService()
