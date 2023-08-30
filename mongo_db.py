import os
from pymongo import MongoClient
from config import mongo_settings

# Connect to MongoDB
client = MongoClient(mongo_settings.MONGO_URI or os.environ['MONGO_URI'])

# Access the database
db = client["lbanams"]