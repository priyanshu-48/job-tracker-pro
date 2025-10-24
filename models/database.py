from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("MONGO_URI not set in environment variables")
DB_NAME = "job_tracker"

def get_db():
    import certifi
    from pymongo import MongoClient

    client = MongoClient(
        MONGO_URI,
        tls=True,
        tlsCAFile=certifi.where()
    )
    return client[DB_NAME]


def init_db():
    db = get_db()

    for collection in ["resumes", "jobs", "job_applications", "skills", "resume_skills"]:
        if collection not in db.list_collection_names():
            db.create_collection(collection)

    db.jobs.create_index("status")              
    db.jobs.create_index("application_date")   
    db.resumes.create_index("upload_date")       
    db.skills.create_index("name", unique=True)  

    print("MongoDB database initialized successfully.")



def get_resume_by_id(resume_id):
    db = get_db()
    return db.resumes.find_one({"_id": ObjectId(resume_id)})

def get_all_resumes():
    db = get_db()
    resumes = list(db.resumes.find().sort("upload_date", -1))
    return resumes

def get_job_by_id(job_id):
    db = get_db()
    return db.jobs.find_one({"_id": ObjectId(job_id)})

def get_all_jobs():
    db = get_db()
    jobs = list(db.jobs.find().sort("application_date", -1))
    return jobs

def update_job_status(job_id, status):
    db = get_db()
    db.jobs.update_one(
        {"_id": ObjectId(job_id)},
        {"$set": {"status": status, "updated_at": datetime.utcnow()}}
    )

def add_follow_up_note(job_id, notes):
    db = get_db()
    db.jobs.update_one(
        {"_id": ObjectId(job_id)},
        {"$set": {"follow_up_notes": notes, "updated_at": datetime.utcnow()}}
    )

def get_job_statistics():
    db = get_db()

    status_counts = list(db.jobs.aggregate([
        {"$group": {"_id": "$status", "count": {"$sum": 1}}}
    ]))

    total_applications = db.jobs.count_documents({})

    monthly_counts = list(db.jobs.aggregate([
        {
            "$group": {
                "_id": {"$substr": ["$application_date", 0, 7]},
                "count": {"$sum": 1}
            }
        },
        {"$sort": {"_id": -1}},
        {"$limit": 6}
    ]))

    return {
        "status_counts": status_counts,
        "total_applications": total_applications,
        "monthly_counts": monthly_counts
    }

def add_job_application(job_id, resume_id, match_score=None, missing_keywords=None):
    db = get_db()
    data = {
        "job_id": ObjectId(job_id),
        "resume_id": ObjectId(resume_id),
        "application_date": datetime.utcnow(),
        "match_score": match_score,
        "missing_keywords": missing_keywords or []
    }
    db.job_applications.insert_one(data)

def add_skill(name, category=None):
    db = get_db()
    db.skills.update_one(
        {"name": name},
        {"$setOnInsert": {
            "category": category,
            "created_at": datetime.utcnow()
        }},
        upsert=True
    )

def link_resume_skill(resume_id, skill_id, confidence_score=1.0):
    db = get_db()
    db.resume_skills.update_one(
        {"resume_id": ObjectId(resume_id), "skill_id": ObjectId(skill_id)},
        {"$set": {"confidence_score": confidence_score}},
        upsert=True
    )

def close_db(_):
    pass
