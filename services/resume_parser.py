import PyPDF2
import docx
import re
import spacy
from typing import Dict, List, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResumeParser:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            logger.warning("spaCy model not found. Installing...")
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
            self.nlp = spacy.load("en_core_web_sm")
        self.tech_skills = {
            'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'go', 'rust', 'swift', 'kotlin'],
            'web': ['html', 'css', 'react', 'angular', 'vue', 'node.js', 'django', 'flask', 'spring'],
            'databases': ['mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'sqlite'],
            'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform'],
            'ml_ai': ['tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy', 'matplotlib'],
            'tools': ['git', 'jenkins', 'jira', 'confluence', 'postman', 'vscode']
        }
        self.patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            'linkedin': r'linkedin\.com/in/[\w-]+',
            'github': r'github\.com/[\w-]+',
            'url': r'https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?'
        }

    def parse_resume(self, file_path: str) -> Dict[str, Any]:
        try:
            if file_path.lower().endswith('.pdf'):
                text = self._extract_pdf_text(file_path)
            elif file_path.lower().endswith('.docx'):
                text = self._extract_docx_text(file_path)
            elif file_path.lower().endswith('.txt'):
                text = self._extract_txt_text(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_path}")
            parsed_data = self._parse_text(text)
            
            logger.info(f"Successfully parsed resume: {file_path}")
            return parsed_data
            
        except Exception as e:
            logger.error(f"Error parsing resume {file_path}: {str(e)}")
            raise

    def _extract_pdf_text(self, file_path: str) -> str:
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            logger.error(f"Error extracting PDF text: {str(e)}")
            raise

    def _extract_docx_text(self, file_path: str) -> str:
        try:
            doc = docx.Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            logger.error(f"Error extracting DOCX text: {str(e)}")
            raise

    def _extract_txt_text(self, file_path: str) -> str:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            logger.error(f"Error extracting TXT text: {str(e)}")
            raise

    def _parse_text(self, text: str) -> Dict[str, Any]:

        text = self._clean_text(text)
        parsed_data = {
            'contact_info': self._extract_contact_info(text),
            'skills': self._extract_skills(text),
            'experience': self._extract_experience(text),
            'education': self._extract_education(text),
            'projects': self._extract_projects(text),
            'certifications': self._extract_certifications(text),
            'raw_text': text[:1000] + "..." if len(text) > 1000 else text
        }
        
        return parsed_data

    def _clean_text(self, text: str) -> str:
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s\.\,\-\@\(\)\:\/]', '', text)
        return text.strip()

    def _extract_contact_info(self, text: str) -> Dict[str, str]:
        contact_info = {}
        email_match = re.search(self.patterns['email'], text)
        if email_match:
            contact_info['email'] = email_match.group()
        phone_match = re.search(self.patterns['phone'], text)
        if phone_match:
            contact_info['phone'] = phone_match.group()
        linkedin_match = re.search(self.patterns['linkedin'], text)
        if linkedin_match:
            contact_info['linkedin'] = linkedin_match.group()
        github_match = re.search(self.patterns['github'], text)
        if github_match:
            contact_info['github'] = github_match.group()
        name = self._extract_name(text)
        if name:
            contact_info['name'] = name
        
        return contact_info

    def _extract_name(self, text: str) -> str:
        lines = text.split('\n')
        for i, line in enumerate(lines[:5]):
            line = line.strip()
            if line and len(line.split()) <= 4:
                if re.match(r'^[A-Za-z\s]+$', line) and len(line) > 2:
                    return line
        
        return ""

    def _extract_skills(self, text: str) -> List[str]:
        skills = set()
        text_lower = text.lower()
        for category, skill_list in self.tech_skills.items():
            for skill in skill_list:
                if skill.lower() in text_lower:
                    skills.add(skill)
        doc = self.nlp(text)
        for ent in doc.ents:
            if ent.label_ in ['ORG', 'PRODUCT']:
                if len(ent.text) > 2 and ent.text.lower() not in skills:
                    skills.add(ent.text)
        
        return list(skills)

    def _extract_experience(self, text: str) -> List[Dict[str, str]]:
        experience = []
        experience_patterns = [
            r'(\w+)\s*[-–]\s*(\w+)\s*[-–]\s*(\d{4})\s*[-–]\s*(\d{4}|Present)',
            r'(\w+)\s*(\d{4})\s*[-–]\s*(\d{4}|Present)',
            r'(\w+)\s*[-–]\s*(\w+)\s*(\d{4})'
        ]
        
        for pattern in experience_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                exp = {
                    'company': match.group(1) if len(match.groups()) >= 1 else '',
                    'position': match.group(2) if len(match.groups()) >= 2 else '',
                    'start_date': match.group(3) if len(match.groups()) >= 3 else '',
                    'end_date': match.group(4) if len(match.groups()) >= 4 else 'Present'
                }
                experience.append(exp)
        
        return experience

    def _extract_education(self, text: str) -> List[Dict[str, str]]:
        education = []
        education_patterns = [
            r'(Bachelor|Master|PhD|B\.Tech|M\.Tech|B\.E|M\.E)\s+[^,\n]+',
            r'([A-Z][a-z]+)\s+University',
            r'([A-Z][a-z]+)\s+College'
        ]
        
        for pattern in education_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                edu = {
                    'degree': match.group(1) if match.group(1) else '',
                    'institution': match.group(2) if len(match.groups()) >= 2 else match.group(1),
                    'year': ''  
                }
                education.append(edu)
        
        return education

    def _extract_projects(self, text: str) -> List[Dict[str, str]]:
        projects = []
        project_keywords = ['project', 'developed', 'built', 'created', 'implemented']
        
        lines = text.split('\n')
        for i, line in enumerate(lines):
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in project_keywords):
                description = ""
                for j in range(i+1, min(i+4, len(lines))):
                    if lines[j].strip() and not lines[j].strip().startswith(('•', '-', '*', '1.', '2.')):
                        description += lines[j].strip() + " "
                    else:
                        break
                
                project = {
                    'title': line.strip(),
                    'description': description.strip()
                }
                projects.append(project)
        
        return projects

    def _extract_certifications(self, text: str) -> List[str]:
        certifications = []
        cert_patterns = [
            r'([A-Z][A-Za-z\s]+)\s+Certification',
            r'([A-Z][A-Za-z\s]+)\s+Certified',
            r'([A-Z][A-Za-z\s]+)\s+Certificate'
        ]
        
        for pattern in cert_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                cert = match.group(1).strip()
                if cert and len(cert) > 3:
                    certifications.append(cert)
        
        return certifications
