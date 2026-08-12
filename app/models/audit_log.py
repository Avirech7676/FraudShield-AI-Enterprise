import enum
from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
from motor.motor_asyncio import AsyncIOMotorCollection
from app.database.connection import MongoDBConnection


class AuditAction(str, enum.Enum):
    """Enumerates audit‑log actions used throughout the app."""
    USER_LOGIN = "USER_LOGIN"
    USER_LOGOUT = "USER_LOGOUT"
    USER_CREATED = "USER_CREATED"
    TRANSACTION_UPDATED = "TRANSACTION_UPDATED"
    FRAUD_STATUS_CHANGED = "FRAUD_STATUS_CHANGED"
    # Extend with any other actions required by the code base.


class AuditLog(BaseModel):
    """Pydantic model that also provides async persistence helpers.

    The model mirrors the fields used in ``app.services.audit_log_service``.
    It uses a lightweight ODM‑style pattern: ``insert`` persists the document
    and returns a new instance with the generated ``_id``. ``find`` and
    ``find_one`` expose Motor cursors for the service layer.
    """
    user_id: Optional[str] = None
    username: Optional[str] = None
    user_email: Optional[str] = None
    action: Optional[AuditAction] = None
    resource_type: Optional[str] = None
    resource_id: Optional[str] = None
    description: str = ""
    details: Dict[str, Any] = Field(default_factory=dict)
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    success: bool = True
    error_message: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    # ------------------------------------------------------------------
    # MongoDB helpers – a minimal async ODM.
    # ------------------------------------------------------------------
    @property
    def _collection(self):
        """Lazily obtain the ``audit_logs`` collection."""
        from app.database.connection import LazyCollection
        return LazyCollection("audit_logs")

    async def insert(self) -> "AuditLog":
        """Insert the document into MongoDB and return a new instance."""
        result = await self._collection.insert_one(self.dict())
        data = self.dict()
        data["_id"] = result.inserted_id
        return self.__class__(**data)

    @classmethod
    async def find(cls, filter_query: dict):
        """Return a Motor/PyMongo cursor for the supplied query."""
        from app.database.connection import LazyCollection
        return LazyCollection("audit_logs").find(filter_query)

    @classmethod
    async def find_one(cls, filter_query: dict) -> Optional[Dict[str, Any]]:
        """Convenient wrapper returning a single document (or ``None``)."""
        from app.database.connection import LazyCollection
        return await cls.find_one_doc(filter_query)

    @classmethod
    async def find_one_doc(cls, filter_query: dict) -> Optional[Dict[str, Any]]:
        from app.database.connection import LazyCollection
        return LazyCollection("audit_logs").find_one(filter_query)

