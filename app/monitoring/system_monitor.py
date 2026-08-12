import os
import psutil
import platform
import requests

from datetime import datetime
from pymongo import MongoClient

from app.config.settings import settings


class SystemMonitor:

    def __init__(self):

        self.start_time = datetime.now()

    def cpu_usage(self):

        return psutil.cpu_percent(interval=None)

    def memory_usage(self):

        return psutil.virtual_memory().percent

    def disk_usage(self):

        return psutil.disk_usage("/").percent

    def python_version(self):

        return platform.python_version()

    def operating_system(self):

        return platform.system()

    def mongodb_status(self):

        try:

            client = MongoClient(

                settings.MONGODB_URI,

                serverSelectionTimeoutMS=1000

            )

            client.server_info()
            client.close()

            return "Online"

        except Exception:

            return "Offline"

    def fastapi_status(self):

        try:

            response = requests.get(

                "http://127.0.0.1:8000/health",
                timeout=1.5

            )

            return "Online" if response.status_code == 200 else "Offline"

        except Exception:

            return "Offline"

    def model_status(self):

        return (

            "Loaded"

            if os.path.exists(settings.PRODUCTION_MODEL)

            else "Not Found"

        )

    def groq_status(self):

        if os.getenv("GROQ_API_KEY"):

            return "Configured"

        return "Missing"

    def model_version(self):

        return settings.MODEL_VERSION

    def snapshot(self):

        return {
            "cpu_usage": self.cpu_usage(),
            "memory_usage": self.memory_usage(),
            "disk_usage": self.disk_usage(),
            "mongodb": self.mongodb_status(),
            "fastapi": self.fastapi_status(),
            "model": self.model_status(),
            "model_version": self.model_version(),
            "python_version": self.python_version(),
            "operating_system": self.operating_system(),
            "groq": self.groq_status(),
            "timestamp": datetime.utcnow().isoformat()
        }
