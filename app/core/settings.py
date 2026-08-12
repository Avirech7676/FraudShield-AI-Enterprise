import os
from pydantic import BaseSettings, Field
from typing import Optional

class Settings(BaseSettings):
    # Application settings
    APP_NAME: str = Field(default="FraudShield AI Enterprise", env="APP_NAME")
    DEBUG: bool = Field(default=False, env="DEBUG")
    # MongoDB
    MONGODB_URI: str = Field(default="mongodb://localhost:27017", env="MONGODB_URI")
    MONGODB_DB_NAME: str = Field(default="fraudshield", env="MONGODB_DB_NAME")
    # JWT
    JWT_SECRET_KEY: str = Field(default="supersecretkey", env="JWT_SECRET_KEY")
    JWT_ALGORITHM: str = Field(default="HS256", env="JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    # Kafka
    KAFKA_BOOTSTRAP_SERVERS: str = Field(default="localhost:9092", env="KAFKA_BOOTSTRAP_SERVERS")
    KAFKA_CLIENT_ID: str = Field(default="fraudshield-client", env="KAFKA_CLIENT_ID")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
