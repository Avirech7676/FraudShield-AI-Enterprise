from typing import List, Optional
from datetime import datetime
from app.models.audit_log import AuditLog, AuditAction
from app.core.security import get_current_user

class AuditLogService:
    """Service for managing audit logs"""

    @staticmethod
    async def log_action(
        user_id: Optional[str] = None,
        username: Optional[str] = None,
        user_email: Optional[str] = None,
        action: AuditAction = None,
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        description: str = "",
        details: Optional[dict] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        success: bool = True,
        error_message: Optional[str] = None
    ) -> AuditLog:
        """Create and save an audit log entry"""

        audit_log = AuditLog(
            user_id=user_id,
            username=username,
            user_email=user_email,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            description=description,
            details=details or {},
            ip_address=ip_address,
            user_agent=user_agent,
            success=success,
            error_message=error_message,
            timestamp=datetime.utcnow()
        )

        await audit_log.insert()
        return audit_log

    @staticmethod
    async def get_audit_logs(
        skip: int = 0,
        limit: int = 100,
        user_id: Optional[str] = None,
        action: Optional[AuditAction] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        search: Optional[str] = None
    ) -> List[AuditLog]:
        """Retrieve audit logs with filtering options"""

        query = {}

        if user_id:
            query["user_id"] = user_id

        if action:
            query["action"] = action.value

        if start_date:
            query["timestamp"] = {"$gte": start_date}

        if end_date:
            if "timestamp" in query:
                query["timestamp"]["$lte"] = end_date
            else:
                query["timestamp"] = {"$lte": end_date}

        # Note: For text search on description, you'd need text indexes
        # This is a simplified version

        audit_logs = await AuditLog.find(query).skip(skip).limit(limit).sort(-AuditLog.timestamp).to_list()
        return audit_logs

    @staticmethod
    async def get_audit_logs_count(
        user_id: Optional[str] = None,
        action: Optional[AuditAction] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        search: Optional[str] = None
    ) -> int:
        """Get count of audit logs matching filters"""

        query = {}

        if user_id:
            query["user_id"] = user_id

        if action:
            query["action"] = action.value

        if start_date:
            query["timestamp"] = {"$gte": start_date}

        if end_date:
            if "timestamp" in query:
                query["timestamp"]["$lte"] = end_date
            else:
                query["timestamp"] = {"$lte": end_date}

        count = await AuditLog.find(query).count()
        return count

    @staticmethod
    async def log_user_login(user_id: str, username: str, email: str, ip_address: str, user_agent: str, success: bool = True):
        """Log user login"""
        await AuditLogService.log_action(
            user_id=user_id,
            username=username,
            user_email=email,
            action=AuditAction.USER_LOGIN,
            description=f"User {username} logged in",
            ip_address=ip_address,
            user_agent=user_agent,
            success=success
        )

    @staticmethod
    async def log_user_logout(user_id: str, username: str, email: str, ip_address: str, user_agent: str):
        """Log user logout"""
        await AuditLogService.log_action(
            user_id=user_id,
            username=username,
            user_email=email,
            action=AuditAction.USER_LOGOUT,
            description=f"User {username} logged out",
            ip_address=ip_address,
            user_agent=user_agent
        )

    @staticmethod
    async def log_user_created(admin_user_id: str, admin_username: str, target_user_id: str, target_username: str):
        """Log user creation"""
        await AuditLogService.log_action(
            user_id=admin_user_id,
            username=admin_username,
            action=AuditAction.USER_CREATED,
            resource_type="user",
            resource_id=target_user_id,
            description=f"User {target_username} created by admin {admin_username}"
        )

    @staticmethod
    async def log_transaction_updated(user_id: str, username: str, transaction_id: str, changes: dict):
        """Log transaction update"""
        await AuditLogService.log_action(
            user_id=user_id,
            username=username,
            action=AuditAction.TRANSACTION_UPDATED,
            resource_type="transaction",
            resource_id=transaction_id,
            description=f"Transaction {transaction_id} updated",
            details={"changes": changes}
        )

    @staticmethod
    async def log_fraud_status_changed(user_id: str, username: str, transaction_id: str, old_status: str, new_status: str):
        """Log fraud status change"""
        await AuditLogService.log_action(
            user_id=user_id,
            username=username,
            action=AuditAction.FRAUD_STATUS_CHANGED,
            resource_type="transaction",
            resource_id=transaction_id,
            description=f"Fraud status changed for transaction {transaction_id} from {old_status} to {new_status}",
            details={"old_status": old_status, "new_status": new_status}
        )