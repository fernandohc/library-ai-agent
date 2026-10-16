import os

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.database import Database

load_dotenv()


class MongoDB:
    def __init__(self):
        uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
        database_name = os.getenv("MONGODB_DATABASE", "library_ai")

        self.client = MongoClient(uri)
        self.database: Database = self.client[database_name]

    def get_database(self) -> Database:
        return self.database

    def close(self):
        self.client.close()
