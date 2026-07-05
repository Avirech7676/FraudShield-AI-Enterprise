import os
import psutil
import platform
import requests

from datetime import datetime
from pymongo import MongoClient


class SystemMonitor:

    def __init__(self):

        self.start_time = datetime.now()

    def cpu_usage(self):

        return psutil.cpu_percent(interval=1)

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

                "mongodb://localhost:27017",

                serverSelectionTimeoutMS=3000

            )

            client.server_info()

            return "Online"

        except:

            return "Offline"

    def fastapi_status(self):

        try:

            response = requests.get(

                "http://127.0.0.1:8000/health"

            )

            return "Online" if response.status_code == 200 else "Offline"

        except:

            return "Offline"

    def model_status(self):

        return (

            "Loaded"

            if os.path.exists("models/fraud_model.pkl")

            else "Not Found"

        )

    def groq_status(self):

        if os.getenv("GROQ_API_KEY"):

            return "Configured"

        return "Missing"