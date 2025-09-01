import PyPDF2
import docx
import re
import spacy
from typing import Dict, List, Any, Tuple
import logging
from models.config import skill_categories, experience_indicators, industry_keywords

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
        
        self.skill_categories = skill_categories
        self.experience_indicators = experience_indicators
        self.industry_keywords = industry_keywords
        
        self.all_skills = self._flatten_skills()
        
        self.patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            'linkedin': r'linkedin\.com/in/[\w-]+',
            'github': r'github\.com/[\w-]+',
            'url': r'https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?',
            'years_experience': r'(\d+)[\+\-\s]*years?\s*(?:of\s*)?(?:experience|exp)',
        }

    def _flatten_skills(self) -> Dict[str, str]:
        """Flatten skill categories into a single dict with all variations"""
        flattened = {}
        for category, skills in self.skill_categories.items():
            for skill_name, variations in skills.items():
                flattened[skill_name.lower()] = skill_name
                for variation in variations:
                    flattened[variation.lower()] = skill_name
        return flattened

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
            'skills': self._extract_skills_enhanced(text),
            'experience_level': self._determine_experience_level(text),
            'industry_focus': self._identify_industry(text),
            'years_experience': self._extract_years_experience(text),
            'experience': self._extract_experience(text),
            'education': self._extract_education(text),
            'projects': self._extract_projects(text),
            'certifications': self._extract_certifications(text),
            'raw_text': text[:1000] + "..." if len(text) > 1000 else text
        }
        
        return parsed_data

    def _clean_text(self, text: str) -> str:
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s\.\,\-\@\(\)\:\/\+\#]', '', text)
        return text.strip()

    def _extract_skills_enhanced(self, text: str) -> Dict[str, List[str]]:
        """Enhanced skill extraction using config data"""
        found_skills = {
            'programming_languages': [],
            'frameworks': [],
            'databases': [],
            'cloud_platforms': [],
            'devops_tools': [],
            'ml_ai_tools': []
        }
        
        text_lower = text.lower()
        
        for category, skills in self.skill_categories.items():
            for skill_name, variations in skills.items():
                for variation in variations:
                    if variation.lower() in text_lower:
                        if skill_name not in found_skills[category]:
                            found_skills[category].append(skill_name)
                        break  
        
        found_skills = {k: v for k, v in found_skills.items() if v}
        
        return found_skills

    def _determine_experience_level(self, text: str) -> str:
        """Determine experience level based on keywords"""
        text_lower = text.lower()
        
        for level, indicators in self.experience_indicators.items():
            for indicator in indicators:
                if indicator in text_lower:
                    return level
        
        return 'unknown'

    def _identify_industry(self, text: str) -> List[str]:
        """Identify potential industry focus"""
        text_lower = text.lower()
        industries = []
        
        for industry, keywords in self.industry_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    if industry not in industries:
                        industries.append(industry)
                    break
        
        return industries

    def _extract_years_experience(self, text: str) -> int:
        """Extract years of experience from text"""
        matches = re.findall(self.patterns['years_experience'], text, re.IGNORECASE)
        if matches:
            return max([int(match) for match in matches])
        return 0

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

    def _extract_experience(self, text: str) -> List[Dict[str, str]]:
        experience = []
        experience_patterns = [
            r'(\w+(?:\s+\w+)*)\s*[-–]\s*(\w+(?:\s+\w+)*)\s*[-–]\s*(\d{4})\s*[-–]\s*(\d{4}|Present)',
            r'(\w+(?:\s+\w+)*)\s*(\d{4})\s*[-–]\s*(\d{4}|Present)',
            r'(\w+(?:\s+\w+)*)\s*[-–]\s*(\w+(?:\s+\w+)*)\s*(\d{4})'
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
            r'(Bachelor|Master|PhD|B\.Tech|M\.Tech|B\.E|M\.E|B\.S|M\.S|B\.A|M\.A)\s+[^,\n]+',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+University',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+College'
        ]
        
        for pattern in education_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                edu = {
                    'degree': match.group(1) if match.group(1) else '',
                    'institution': match.group(2) if len(match.groups()) >= 2 else match.group(1),
                    'year': self._extract_year_from_context(text, match.start())
                }
                education.append(edu)
        
        return education

    def _extract_year_from_context(self, text: str, position: int) -> str:
        """Extract year from surrounding context"""
        context = text[max(0, position-100):position+100]
        year_match = re.search(r'\b(19|20)\d{2}\b', context)
        return year_match.group() if year_match else ''

    def _extract_projects(self, text: str) -> List[Dict[str, str]]:
        projects = []
        project_keywords = ['project', 'developed', 'built', 'created', 'implemented', 'designed']
        
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
                    'description': description.strip(),
                    'technologies': self._extract_technologies_from_text(line + " " + description)
                }
                projects.append(project)
        
        return projects

    def _extract_technologies_from_text(self, text: str) -> List[str]:
        """Extract technologies mentioned in a specific text block"""
        technologies = []
        text_lower = text.lower()
        
        for skill in self.all_skills:
            if skill in text_lower:
                tech_name = self.all_skills[skill]
                if tech_name not in technologies:
                    technologies.append(tech_name)
        
        return technologies

    def _extract_certifications(self, text: str) -> List[str]:
        certifications = []
        cert_patterns = [
            r'([A-Z][A-Za-z\s]+)\s+Certification',
            r'([A-Z][A-Za-z\s]+)\s+Certified',
            r'([A-Z][A-Za-z\s]+)\s+Certificate',
            r'AWS\s+[A-Za-z\s]+',
            r'Azure\s+[A-Za-z\s]+',
            r'Google\s+[A-Za-z\s]+\s+Certificate'
        ]
        
        for pattern in cert_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                cert = match.group(1).strip() if len(match.groups()) >= 1 else match.group(0).strip()
                if cert and len(cert) > 3 and cert not in certifications:
                    certifications.append(cert)
        
        return certifications