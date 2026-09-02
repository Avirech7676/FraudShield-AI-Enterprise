from pymongo import MongoClient
from pymongo.errors import PyMongoError

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

    def connect(self):

        if MongoDBConnection._db is not None:
            self.client = MongoDBConnection._client
            self.db = MongoDBConnection._db
            return self.db

        try:

            self.client = MongoClient(
                self.uri,
                serverSelectionTimeoutMS=2000,
                connectTimeoutMS=2000,
                socketTimeoutMS=3000,
                maxPoolSize=50,
            )

            self.db = self.client[self.database_name]
            MongoDBConnection._client = self.client
            MongoDBConnection._db = self.db

            logger.info(
                "MongoDB Connected Successfully"
            )

            return self.db

        except Exception as e:

            logger.warning(
                f"MongoDB Connection Failed (falling back to memory/mock): {e}"
            )

            return None

    ###################################################

    def close(self):

        if self.client:

            self.client.close()
            MongoDBConnection._client = None
            MongoDBConnection._db = None

            logger.info(
                "MongoDB Connection Closed"
            )
