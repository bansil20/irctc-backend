from pymongo import MongoClient
from django.conf import settings

client = MongoClient("mongodb://localhost:27017/")

db = client["irctc_logs_db"]

api_logs_collection = db["api_logs"]