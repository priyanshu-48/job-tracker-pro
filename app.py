from services.job_scraper import search_timesjobs_jobs
import os
from dotenv import load_dotenv
import logging
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime
from services.resume_parser import ResumeParser
from services.job_matcher import JobMatcher
from models.database import init_db, get_db
import spacy
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")


load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
PORT = int(os.getenv('PORT', 5000))
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

logging.basicConfig(level=logging.DEBUG if DEBUG else logging.INFO, 
                   format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_resume():
    if request.method == 'GET':
        return render_template('index.html')
    logger.debug(f"Upload method: {request.method}")
    logger.debug(f"Files: {request.files}")
    if 'resume' not in request.files:
        flash('No file selected')
        return redirect(url_for('index'))
    file = request.files['resume']
    if file.filename == '':
        flash('No file selected')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        try:
            parser = ResumeParser()
            parsed_data = parser.parse_resume(filepath)
            db = get_db()
            db.resumes.insert_one({
                "filename": filename,
                "original_filename": file.filename,
                "upload_date": datetime.utcnow(),
                "parsed_data": parsed_data,
                "created_at": datetime.utcnow()
            })
            os.remove(filepath)
            logger.info(f"Resume {filename} uploaded and parsed successfully.")
            flash('Resume uploaded and parsed successfully!')
            return redirect(url_for('dashboard'))
        except Exception as e:
            logger.error(f"Error parsing resume {filename}: {str(e)}", exc_info=True)
            flash(f'Error parsing resume: {str(e)}')
            return redirect(url_for('index'))
    flash('Invalid file type. Please upload PDF, DOCX, or TXT files.')
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    db = get_db()
    resumes = list(db.resumes.find().sort("upload_date", -1))
    jobs = list(db.jobs.find().sort("application_date", -1))
    for r in resumes:
        r["_id"] = str(r["_id"])
    for j in jobs:
        j["_id"] = str(j["_id"])
    return render_template('dashboard.html', resumes=resumes, jobs=jobs)

@app.route('/add_job', methods=['GET', 'POST'])
def add_job():
    if request.method == 'POST':
        company = request.form['company']
        position = request.form['position']
        job_description = request.form['job_description']
        application_date = request.form['application_date']
        status = request.form['status']
        db = get_db()
        db.jobs.insert_one({
            "company": company,
            "position": position,
            "job_description": job_description,
            "application_date": application_date,
            "status": status,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        })
        flash('Job added successfully!')
        return redirect(url_for('dashboard'))
    return render_template('add_job.html')

@app.route('/api/parse_resume', methods=['POST'])
def api_parse_resume():
    if 'resume' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['resume']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    if file and allowed_file(file.filename):
        try:
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{timestamp}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            parser = ResumeParser()
            parsed_data = parser.parse_resume(filepath)
            os.remove(filepath)
            return jsonify({
                'success': True,
                'data': parsed_data
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/find_jobs', methods=['GET', 'POST'])
def find_jobs():
    results = []
    query = ''
    location = ''
    page = 1
    if request.method == 'POST':
        query = request.form.get('query', '').strip()
        location = request.form.get('location', '').strip()
        page = int(request.form.get('page', '1') or '1')
        if not query:
            flash('Please enter a search query')
        else:
            try:
                results = search_timesjobs_jobs(query=query, location=location, page=page, max_results=20)
                if not results:
                    flash('No results found. Try a simpler keyword or leave location empty.')
            except Exception as e:
                flash(f'Error fetching jobs: {str(e)}')
    return render_template('find_jobs.html', results=results, query=query, location=location, page=page)

@app.route('/import_job', methods=['POST'])
def import_job():
    company = request.form.get('company', '').strip() or 'N/A'
    title = request.form.get('title', '').strip() or 'N/A'
    description_snippet = request.form.get('snippet', '').strip() or ''
    job_link = request.form.get('link', '').strip() or ''
    job_location = request.form.get('location', '').strip() or ''
    description = description_snippet
    if job_location:
        description = f"Location: {job_location}\n\n{description}"
    if job_link:
        description = f"Link: {job_link}\n\n{description}"
    db = get_db()
    application_date = datetime.utcnow().date().isoformat()
    status = "applied"

    db.jobs.insert_one({
        "company": company,
        "position": title,
        "job_description": description,
        "application_date": application_date,
        "status": status,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    })
    flash('Job imported successfully!')
    return redirect(url_for('dashboard'))

from bson import ObjectId
import ast

@app.route('/check_match/<string:job_id>')
def check_match(job_id):
    db = get_db()

    # --- Fetch job document ---
    try:
        job = db.jobs.find_one({"_id": ObjectId(job_id)})
    except Exception:
        flash("Invalid Job ID.")
        return redirect(url_for('dashboard'))

    if not job:
        flash('Job not found')
        return redirect(url_for('dashboard'))

    logger.debug(f"Job data: {job}")

    # --- Fetch latest resume document ---
    resume = db.resumes.find_one(sort=[("upload_date", -1)])
    if not resume:
        flash('No resume found. Please upload a resume first.')
        return redirect(url_for('index'))

    logger.debug(f"Resume data: {resume}")

    try:
        # Parse stored resume data
        parsed_data_field = resume.get("parsed_data", "{}")
        if isinstance(parsed_data_field, str):
            resume_data = ast.literal_eval(parsed_data_field)
        else:
            resume_data = parsed_data_field

        from services.job_matcher import JobMatcher
        matcher = JobMatcher()

        # Compute match score and analysis
        match_score, analysis_details = matcher.calculate_match_score(
            resume_data, job.get("job_description", "")
        )

        missing_skills = matcher._find_missing_skills_enhanced(
            resume_data, analysis_details.get("job_skills", [])
        )
        skill_suggestions = matcher.get_skill_suggestions(missing_skills)

        logger.debug(f"Resume data type: {type(resume_data)}")
        logger.debug(f"Job description type: {type(job.get('job_description'))}")
        logger.debug(f"Match score value: {match_score}")
        logger.debug(f"Missing skills: {missing_skills}")
        logger.debug(f"Analysis details: {analysis_details}")

        # Convert ObjectIds to strings for Jinja
        job["_id"] = str(job["_id"])
        resume["_id"] = str(resume["_id"])

        return render_template(
            'job_match.html',
            job=job,
            resume=resume_data,
            match_score=match_score,
            missing_skills=missing_skills,
            skill_suggestions=skill_suggestions,
            analysis=analysis_details
        )

    except Exception as e:
        logger.error(f'Error analyzing match for job ID {job_id}: {str(e)}', exc_info=True)
        flash(f'Error analyzing match: {str(e)}')
        return redirect(url_for('dashboard'))


if __name__ == '__main__':
    init_db()
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=DEBUG)
