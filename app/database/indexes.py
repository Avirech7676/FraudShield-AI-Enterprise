import asyncio
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.config.logging_config import logger

async def ensure_indexes(db: AsyncIOMotorDatabase) -> None:
    """Create required MongoDB indexes for the FraudShield collections.
    This function is idempotent – MongoDB will ignore duplicate index creation.
    """
    try:
        # Users collection
        await db["users"].create_index("username", unique=True)
        await db["users"].create_index("email", unique=True)
        # Predictions collection
        await db["predictions"].create_index("transaction_id")
        await db["predictions"].create_index([("created_at", -1)])
        # Cases collection
        await db["cases"].create_index("case_id", unique=True)
        await db["cases"].create_index("transaction_id")
        # Alerts collection
        await db["alerts"].create_index("alert_id", unique=True)
        await db["alerts"].create_index("transaction_id")
        logger.info("MongoDB indexes ensured successfully")
    except Exception as e:
        logger.exception(f"Failed to ensure MongoDB indexes: {e}")
        raise

def ensure_indexes_sync(db):
    """Run the async ensure_indexes in a new event loop for sync callers."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(ensure_indexes(db))
