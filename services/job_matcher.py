import re
from typing import Dict, List, Any, Tuple
from collections import Counter
import logging
from models.config import skill_categories, experience_indicators, industry_keywords

logger = logging.getLogger(__name__)

class JobMatcher:
    def __init__(self):
        self.skill_categories = skill_categories
        
        self.experience_indicators = experience_indicators
        
        self.industry_keywords = industry_keywords

    def calculate_match_score(self, resume_data: Dict[str, Any], job_description: str) -> Tuple[float, Dict[str, Any]]:
        try:
            resume_skills = self._extract_resume_skills_enhanced(resume_data)
            
            job_analysis = self._analyze_job_description_enhanced(job_description)
            
            skill_match_score = self._calculate_skill_match_score(resume_skills, job_analysis['technical_skills'])
            experience_match_score = self._calculate_experience_match_score(resume_data, job_analysis['experience_level'])
            industry_match_score = self._calculate_industry_match_score(resume_data, job_analysis['industry_focus'])
            
            final_score = (
                skill_match_score * 0.6 +      
                experience_match_score * 0.25 + 
                industry_match_score * 0.15     
            )
            
            missing_skills = self._find_missing_skills_enhanced(resume_skills, job_analysis['technical_skills'])
            
            analysis = {
                'resume_skills': resume_skills,
                'job_skills': job_analysis['technical_skills'],
                'missing_skills': missing_skills,
                'skill_match_score': skill_match_score,
                'experience_match_score': experience_match_score,
                'industry_match_score': industry_match_score,
                'experience_level': job_analysis['experience_level'],
                'industry_focus': job_analysis['industry_focus'],
                'key_requirements': job_analysis['key_requirements'],
                'overall_analysis': self._generate_overall_analysis(final_score, skill_match_score, experience_match_score)
            }
            
            return round(final_score, 1), analysis
            
        except Exception as e:
            logger.error(f"Error calculating match score: {str(e)}")
            return 0.0, {}

    def _extract_resume_skills_enhanced(self, resume_data: Dict[str, Any]) -> List[str]:
        skills = set()
        
        if 'skills' in resume_data:
            for skill in resume_data['skills']:
                normalized_skill = self._normalize_skill(skill)
                if normalized_skill:
                    skills.add(normalized_skill)
        
        if 'experience' in resume_data:
            for exp in resume_data['experience']:
                if 'position' in exp:
                    position_skills = self._extract_skills_from_text(exp['position'])
                    skills.update(position_skills)
                
                if 'description' in exp:
                    desc_skills = self._extract_skills_from_text(exp['description'])
                    skills.update(desc_skills)
        
        if 'projects' in resume_data:
            for project in resume_data['projects']:
                if 'title' in project:
                    title_skills = self._extract_skills_from_text(project['title'])
                    skills.update(title_skills)
                
                if 'description' in project:
                    desc_skills = self._extract_skills_from_text(project['description'])
                    skills.update(desc_skills)
        
        if 'education' in resume_data:
            for edu in resume_data['education']:
                if 'degree' in edu:
                    degree_skills = self._extract_skills_from_text(edu['degree'])
                    skills.update(degree_skills)
        
        return list(skills)

    def _normalize_skill(self, skill: str) -> str:
        skill = skill.lower().strip()
        
        skill = re.sub(r'^(expert in|proficient in|skilled in|experience with|knowledge of)\s+', '', skill)
        skill = re.sub(r'\s+(expert|proficient|skilled|experienced|knowledge)$', '', skill)
        
        skill = re.sub(r'\s+', ' ', skill)  
        
        return skill if len(skill) > 1 else None

    def _extract_skills_from_text(self, text: str) -> List[str]:
        if not text:
            return []
        
        text = text.lower()
        skills = set()
        
        for category, skill_dict in self.skill_categories.items():
            for skill_name, variations in skill_dict.items():
                for variation in variations:
                    if variation in text:
                        skills.add(skill_name)
                        break
        
        return list(skills)

    def _analyze_job_description_enhanced(self, job_description: str) -> Dict[str, Any]:
        text_lower = job_description.lower()
        
        analysis = {
            'technical_skills': [],
            'experience_level': 'mid',
            'industry_focus': [],
            'key_requirements': [],
            'total_skills': 0
        }
        
        for category, skill_dict in self.skill_categories.items():
            for skill_name, variations in skill_dict.items():
                for variation in variations:
                    if variation in text_lower:
                        analysis['technical_skills'].append(skill_name)
                        break
        
        for level, indicators in self.experience_indicators.items():
            if any(indicator in text_lower for indicator in indicators):
                analysis['experience_level'] = level
                break
        
        for industry, keywords in self.industry_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                analysis['industry_focus'].append(industry)
        
        requirement_patterns = [
            r'requirements?[:\s]+(.*?)(?=\n|\.|;|responsibilities)',
            r'must have[:\s]+(.*?)(?=\n|\.|;)',
            r'looking for[:\s]+(.*?)(?=\n|\.|;)',
            r'qualifications?[:\s]+(.*?)(?=\n|\.|;)',
            r'experience with[:\s]+(.*?)(?=\n|\.|;)'
        ]
        
        for pattern in requirement_patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            analysis['key_requirements'].extend(matches)
        
        analysis['total_skills'] = len(analysis['technical_skills'])
        
        return analysis

    def _calculate_skill_match_score(self, resume_skills: List[str], job_skills: List[str]) -> float:
        if not job_skills:
            return 0.0
        
        resume_set = set(resume_skills)
        job_set = set(job_skills)
        
        exact_matches = len(resume_set.intersection(job_set))
        
        partial_matches = 0
        for job_skill in job_set:
            if job_skill in resume_set:
                continue
            
            for resume_skill in resume_set:
                if self._are_skills_related(job_skill, resume_skill):
                    partial_matches += 0.5
                    break
        
        total_matches = exact_matches + partial_matches
        base_score = total_matches / len(job_set)
        
        skill_coverage_bonus = min(len(resume_set) / max(len(job_set), 1), 1.5) - 1.0
        
        final_score = min(base_score + skill_coverage_bonus * 0.1, 1.0)
        return final_score * 100

    def _get_skill_base_and_category(self, skill: str) -> Tuple[str | None, str | None]:
        normalized_skill = skill.lower().strip()
        for category, skill_dict in self.skill_categories.items():
            if normalized_skill in skill_dict:  
                return normalized_skill, category
            for base_skill, variations in skill_dict.items():
                if normalized_skill in variations: 
                    return base_skill, category
        return None, None

    def _are_skills_related(self, skill1: str, skill2: str) -> bool:
        base_skill1, category1 = self._get_skill_base_and_category(skill1)
        base_skill2, category2 = self._get_skill_base_and_category(skill2)

        if category1 and category2 and category1 == category2:
            return True
        
        if skill1.startswith(skill2) or skill2.startswith(skill1):
            return True
        
        return False

    def _calculate_experience_match_score(self, resume_data: Dict[str, Any], job_level: str) -> float:
        total_years = 0
        
        if 'experience' in resume_data:
            for exp in resume_data['experience']:
                if 'duration' in exp:
                    duration = exp['duration']
                    years = self._extract_years_from_duration(duration)
                    total_years += years
        
        if job_level == 'entry':
            if total_years <= 2:
                return 100.0
            elif total_years <= 5:
                return 70.0
            else:
                return 40.0
        elif job_level == 'mid':
            if 2 <= total_years <= 7:
                return 100.0
            elif total_years < 2:
                return 60.0
            else:
                return 80.0
        else:  
            if total_years >= 5:
                return 100.0
            elif total_years >= 3:
                return 80.0
            else:
                return 50.0

    def _extract_years_from_duration(self, duration: str) -> float:
        if not duration:
            return 0.0
        
        duration = duration.lower()
        
        year_patterns = [
            r'(\d+)\s*years?',
            r'(\d+)\s*yr',
            r'(\d+)\s*mos?',  
            r'(\d+)\s*months?'
        ]
        
        total_years = 0.0
        
        for pattern in year_patterns:
            matches = re.findall(pattern, duration)
            for match in matches:
                if 'mos' in pattern or 'months' in pattern:
                    total_years += float(match) / 12
                else:
                    total_years += float(match)
        
        return total_years

    def _calculate_industry_match_score(self, resume_data: Dict[str, Any], job_industries: List[str]) -> float:
        if not job_industries:
            return 50.0
        resume_industries = set()
        if 'experience' in resume_data:
            for exp in resume_data['experience']:
                company = exp.get('company', '').lower()
                description = exp.get('description', '').lower()
                
                for industry, keywords in self.industry_keywords.items():
                    if any(keyword in company or keyword in description for keyword in keywords):
                        resume_industries.add(industry)
        
        if 'projects' in resume_data:
            for project in resume_data['projects']:
                title = project.get('title', '').lower()
                description = project.get('description', '').lower()
                
                for industry, keywords in self.industry_keywords.items():
                    if any(keyword in title or keyword in description for keyword in keywords):
                        resume_industries.add(industry)
        
        if not resume_industries:
            return 30.0
        
        matches = len(resume_industries.intersection(set(job_industries)))
        if matches > 0:
            return 100.0
        else:
            return 40.0

    def _find_missing_skills_enhanced(self, resume_skills: List[str], job_skills: List[str]) -> List[str]:
        resume_set = set(resume_skills)
        job_set = set(job_skills)
        
        missing = job_set - resume_set
        
        critical_missing = []
        important_missing = []
        nice_to_have = []
        
        for skill in missing:
            skill_importance = 0
            for category, skills in self.skill_categories.items():
                if skill in skills:
                    skill_importance += 1
            
            if skill_importance >= 2:
                critical_missing.append(skill)
            elif skill_importance == 1:
                important_missing.append(skill)
            else:
                nice_to_have.append(skill)
        return critical_missing + important_missing + nice_to_have

    def _generate_overall_analysis(self, final_score: float, skill_score: float, experience_score: float) -> str:
        if final_score >= 85:
            return "Excellent match! Your skills and experience align very well with this position."
        elif final_score >= 70:
            return "Good match! You have most of the required skills and experience."
        elif final_score >= 55:
            return "Moderate match. You have some relevant skills but may need to develop others."
        elif final_score >= 40:
            return "Limited match. Consider focusing on developing the missing skills before applying."
        else:
            return "Low match. This position may not be the best fit for your current skill set."

    def get_skill_suggestions(self, missing_keywords: List[str]) -> Dict[str, List[str]]:
        suggestions = {}
        
        for keyword in missing_keywords:
            for category, skills in self.skill_categories.items():
                if keyword in skills:
                    if category not in suggestions:
                        suggestions[category] = []
                    suggestions[category].append(keyword)
                    break
            else:
                if 'general' not in suggestions:
                    suggestions['general'] = []
                suggestions['general'].append(keyword)
        
        return suggestions
