from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")

client = MongoClient(MONGO_URI)

db = client["irctc_logs"]           # Database name
logs_collection = db["api_logs"]    # Collection name