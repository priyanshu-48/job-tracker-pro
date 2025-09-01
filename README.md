# Job Tracker Pro 🚀

An intelligent Resume Parser + Job Tracker built with Python Flask, featuring AI-powered text extraction, smart job matching, and comprehensive application tracking.

## ✨ Features

### 🔍 Resume Parser
- **Multi-format Support**: PDF, DOCX, and TXT files
- **AI-Powered Extraction**: Uses spaCy NER for intelligent field identification
- **Structured Data**: Extracts contact info, skills, experience, education, projects, and certifications
- **Smart Skills Detection**: Categorized skill extraction with confidence scoring

### 📊 Job Tracker
- **Application Management**: Track job applications with detailed status updates
- **Smart Matching**: AI-powered resume-job matching with skill gap analysis
- **Progress Tracking**: Monitor application status from applied to offered
- **Follow-up Reminders**: Keep track of important dates and notes

### 🎯 Smart Matching Engine
- **Keyword Analysis**: Intelligent extraction of job requirements
- **Match Scoring**: Percentage-based compatibility scoring
- **Skill Gap Analysis**: Identify missing skills for each application
- **Improvement Suggestions**: Get recommendations to enhance your resume

### 📈 Analytics Dashboard
- **Visual Statistics**: Beautiful charts and progress indicators
- **Application Metrics**: Success rates, response times, and status distribution
- **Performance Tracking**: Monitor your job search effectiveness over time

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite (with PostgreSQL support planned)
- **AI/NLP**: spaCy, NLTK for text processing
- **Frontend**: Bootstrap 5, Chart.js, Font Awesome
- **File Processing**: PyPDF2, python-docx
- **Data Analysis**: Custom matching algorithms

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd job-tracker
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download spaCy model**
   ```bash
   python -m spacy download en_core_web_sm
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open your browser**
   Navigate to `http://localhost:5000`

## 📁 Project Structure

```
job-tracker/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── services/             # Business logic services
│   ├── resume_parser.py  # Resume parsing engine
│   └── job_matcher.py    # Job matching algorithms
├── models/               # Database models
│   └── database.py       # Database initialization and queries
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Home page with resume upload
│   ├── dashboard.html    # Main dashboard
│   └── add_job.html      # Job entry form
├── uploads/              # Resume file uploads
├── data/                 # SQLite database files
└── static/               # Static assets (CSS, JS, images)
```

## 🎯 Usage Guide

### 1. Upload Your Resume
- Navigate to the home page
- Drag & drop or click to upload your resume (PDF/DOCX/TXT)
- The system will automatically parse and extract information
- View parsed data in the dashboard

### 2. Add Job Applications
- Click "Add Job" from the dashboard
- Fill in company details, position, and application date
- Paste the full job description for better matching
- Add optional notes and salary information

### 3. Track Applications
- Monitor application status in the dashboard
- Update status as you progress through the hiring process
- Add follow-up notes and important dates
- View match scores and skill gaps

### 4. Analyze Performance
- Check your success rates and response times
- Identify which skills are most in demand
- Track application trends over time
- Get insights to improve your job search strategy

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:

```env
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///data/job_tracker.db
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216
```

### Database Configuration
The application uses SQLite by default. To use PostgreSQL:

1. Install PostgreSQL dependencies
2. Update database configuration in `models/database.py`
3. Set environment variables for database connection

## 🧪 Testing

### Test Resume Parsing
1. Upload a sample resume (PDF/DOCX)
2. Check parsed data accuracy
3. Verify skill extraction
4. Test contact information parsing

### Test Job Matching
1. Add a job with detailed description
2. Compare with uploaded resume
3. Verify match score calculation
4. Check missing skills identification

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
1. Set `FLASK_ENV=production`
2. Use production WSGI server (Gunicorn)
3. Configure reverse proxy (Nginx)
4. Set up SSL certificates
5. Configure database for production

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

## 🔮 Future Enhancements

### Phase 2: Advanced Features
- [ ] Resume tailoring and customization
- [ ] Job board integration (Indeed, LinkedIn)
- [ ] Email notifications and reminders
- [ ] Advanced analytics and reporting

### Phase 3: AI Improvements
- [ ] Machine learning for better parsing
- [ ] Predictive job success scoring
- [ ] Automated resume optimization
- [ ] Industry-specific skill analysis

### Phase 4: Enterprise Features
- [ ] Multi-user support and authentication
- [ ] Team collaboration features
- [ ] Advanced reporting and exports
- [ ] API for third-party integrations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **spaCy** for natural language processing capabilities
- **Bootstrap** for the beautiful UI components
- **Chart.js** for interactive data visualization
- **Font Awesome** for the amazing icons

## 📞 Support

- **Issues**: Report bugs and feature requests via GitHub Issues
- **Discussions**: Join community discussions on GitHub Discussions
- **Email**: Contact the development team for enterprise support

---

**Built with ❤️ and Python for job seekers worldwide**

*Make your job search smarter, not harder! 🎯*

