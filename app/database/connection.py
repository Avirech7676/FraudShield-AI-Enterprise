from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import PyMongoError
import asyncio

from app.config.settings import settings
from app.config.logging_config import logger


class MongoDBConnection:
    _client = None
    _db = None

    def __init__(self):

        self.uri = settings.MONGODB_URI

        self.database_name = settings.DATABASE_NAME

        self.client = None

        self.db = None

    ###################################################

    async def connect(self):

        if MongoDBConnection._db is not None:
            self.client = MongoDBConnection._client
            self.db = MongoDBConnection._db
            return self.db

        try:

            self.client = AsyncIOMotorClient(
                self.uri,
                serverSelectionTimeoutMS=5000,
                maxPoolSize=50,
                retryWrites=True,
            )
            await self.client.admin.command("ping")
            logger.info(
                f"Connected Database : {self.database_name}"
            )

            self.db = self.client[self.database_name]
            MongoDBConnection._client = self.client
            MongoDBConnection._db = self.db

            logger.info(
                "MongoDB Connected Successfully"
            )

            return self.db

        except PyMongoError as e:

            logger.exception(
                f"MongoDB Connection Failed : {e}"
            )

            raise

    ###################################################

    def connect_sync(self):
        """Synchronous wrapper for async connect, for legacy code paths."""
        from pymongo import MongoClient
        client = MongoClient(self.uri)
        db = client[self.database_name]
        logger.info("MongoDB Connected Synchronously via PyMongo")
        return db

    def close_sync(self):
        """Synchronous wrapper for async close."""
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop.run_until_complete(self.close())


class LazyCollection:
    """Lazy proxy wrapper for PyMongo/Motor collections to prevent top-level module import connections."""

    def __init__(self, collection_name: str):
        self.collection_name = collection_name

    @property
    def _collection(self):
        if MongoDBConnection._db is not None:
            return MongoDBConnection._db[self.collection_name]
        conn = MongoDBConnection()
        db = conn.connect_sync()
        MongoDBConnection._db = db
        return db[self.collection_name]

    def __getattr__(self, item):
        return getattr(self._collection, item)

    def __getitem__(self, item):
        return self._collection[item]

