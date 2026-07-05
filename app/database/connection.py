from pymongo import MongoClient


class MongoDBConnection:

    def __init__(self):

        self.uri = "mongodb://localhost:27017"

        self.client = None

        self.db = None

    ###################################################

    def connect(self):

        self.client = MongoClient(self.uri)

        self.db = self.client["FraudShieldDB"]

        print("=" * 60)
        print("MongoDB Connected Successfully")
        print("=" * 60)

        return self.db

    ###################################################

    def close(self):

        if self.client:

            self.client.close()

            print("MongoDB Connection Closed")