from pymongo import MongoClient
import certifi, os

uri = os.getenv("MONGO_URI", "mongodb+srv://priyanshus204_db_user:sonu2004@job-tracker.avh3xtp.mongodb.net/?appName=job-tracker")
try:
    client = MongoClient(uri)
    print("✅ Connected successfully!")
    print("Databases:", client.list_database_names())
except Exception as e:
    print("❌ Connection failed:", e)
