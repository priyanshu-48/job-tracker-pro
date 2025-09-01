import sqlite3
import os
from datetime import datetime

DATABASE_PATH = 'data/job_tracker.db'

def get_db():
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  
    return conn

def init_db():
    with get_db() as db:
        cursor = db.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS resumes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                original_filename TEXT NOT NULL,
                upload_date TIMESTAMP NOT NULL,
                parsed_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company TEXT NOT NULL,
                position TEXT NOT NULL,
                job_description TEXT,
                application_date DATE NOT NULL,
                status TEXT DEFAULT 'applied',
                salary_range TEXT,
                resume_version TEXT,
                follow_up_notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs (status)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_jobs_application_date ON jobs (application_date)')
    

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS job_applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id INTEGER NOT NULL,
                resume_id INTEGER NOT NULL,
                application_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                match_score REAL,
                missing_keywords TEXT,
                FOREIGN KEY (job_id) REFERENCES jobs (id),
                FOREIGN KEY (resume_id) REFERENCES resumes (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS skills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                category TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS resume_skills (
                resume_id INTEGER NOT NULL,
                skill_id INTEGER NOT NULL,
                confidence_score REAL DEFAULT 1.0,
                PRIMARY KEY (resume_id, skill_id),
                FOREIGN KEY (resume_id) REFERENCES resumes (id),
                FOREIGN KEY (skill_id) REFERENCES skills (id)
            )
        ''')
        
        db.commit()
        
        print("Database initialized successfully!")

def close_db(db):
    if db:
        db.close()

def get_resume_by_id(resume_id):
    with get_db() as db:
        cursor = db.cursor()
        
        cursor.execute('SELECT * FROM resumes WHERE id = ?', (resume_id,))
        resume = cursor.fetchone()
        
        return resume

def get_job_by_id(job_id):
    with get_db() as db:
        cursor = db.cursor()
        
        cursor.execute('SELECT * FROM jobs WHERE id = ?', (job_id,))
        job = cursor.fetchone()
        
        return job

def get_all_resumes():
    with get_db() as db:
        cursor = db.cursor()
        
        cursor.execute('SELECT * FROM resumes ORDER BY upload_date DESC')
        resumes = cursor.fetchall()
        
        return resumes

def get_all_jobs():
    with get_db() as db:
        cursor = db.cursor()
        
        cursor.execute('SELECT * FROM jobs ORDER BY application_date DESC')
        jobs = cursor.fetchall()
        
        return jobs

def update_job_status(job_id, status):
    with get_db() as db:
        cursor = db.cursor()
        
        cursor.execute('''
            UPDATE jobs 
            SET status = ?, updated_at = CURRENT_TIMESTAMP 
            WHERE id = ?
        ''', (status, job_id))
        
        db.commit()

def add_follow_up_note(job_id, notes):
    with get_db() as db:
        cursor = db.cursor()
        
        cursor.execute('''
            UPDATE jobs 
            SET follow_up_notes = ?, updated_at = CURRENT_TIMESTAMP 
            WHERE id = ?
        ''', (notes, job_id))
        
        db.commit()

def get_job_statistics():
    with get_db() as db:
        cursor = db.cursor()
                        
        cursor.execute('''
            SELECT status, COUNT(*) as count 
            FROM jobs 
            GROUP BY status
        ''')
        status_counts = cursor.fetchall()
        
        cursor.execute('SELECT COUNT(*) as total FROM jobs')
        total_applications = cursor.fetchone()['total']
        
        cursor.execute('''
            SELECT strftime('%Y-%m', application_date) as month, COUNT(*) as count
            FROM jobs 
            GROUP BY month 
            ORDER BY month DESC 
            LIMIT 6
        ''')
        monthly_counts = cursor.fetchall()
        
        return {
            'status_counts': status_counts,
            'total_applications': total_applications,
            'monthly_counts': monthly_counts
        }

