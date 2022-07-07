import os
from typing import List, Dict

from bson import ObjectId
from dotenv import load_dotenv
from pymongo import MongoClient

from models.services.model_results_storage_service import ModelResultsStorageService

load_dotenv()


class MongoDBResultsStorageService(ModelResultsStorageService):

    def __init__(self, db_name):
        self.db_client = MongoClient(os.environ['DATABASE_URL'])
        self.db = self.db_client[db_name]
        self.collection = self.db['results']

    def get_all(self) -> List[Dict]:
        cursor = self.collection.find()
        return [doc for doc in cursor]

    def get(self, result_id: str) -> Dict:
        return self.collection.find_one(ObjectId(result_id))

    def save(self, result: Dict) -> Dict:
        self.collection.insert_one(result)
        return result

    def remove_all(self):
        self.collection.delete_many({})
