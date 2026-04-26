def calculate_ats_score(resume_text, job_keywords=None):
    """
    ATS Score = (matched keywords / total keywords) × 100
    Plus bonus points for sections, contact info, etc.
    """
    # Default keywords if no job-specific ones provided
    if job_keywords is None:
        job_keywords = [
            'experience', 'education', 'skills', 'projects', 
            'achievements', 'certification', 'internship',
            'python', 'java', 'sql', 'machine learning', 'git'
        ]
    
    text_lower = resume_text.lower()
    
    # Check for important resume sections (structural bonus)
    section_keywords = ['education', 'experience', 'skills', 'projects', 'summary']
    section_score = sum(1 for s in section_keywords if s in text_lower)
    section_bonus = (section_score / len(section_keywords)) * 20  # max 20 points
    
    # Keyword matching score (max 70 points)
    matched = [kw for kw in job_keywords if kw.lower() in text_lower]
    keyword_score = (len(matched) / len(job_keywords)) * 70
    
    # Contact info check (max 10 points)
    has_email = bool(re.search(r'[\w.-]+@[\w.-]+\.\w+', resume_text))
    has_phone = bool(re.search(r'\+?[\d\s-]{10,}', resume_text))
    contact_score = (has_email + has_phone) * 5  # 5 points each
    
    total_score = round(keyword_score + section_bonus + contact_score, 1)
    missing = [kw for kw in job_keywords if kw.lower() not in text_lower]
    
    return {
        'ats_score': min(total_score, 100),  # cap at 100
        'keywords_matched': matched,
        'missing_keywords': missing[:10],    # top 10 missing
        'breakdown': {
            'keyword_score': round(keyword_score, 1),
            'section_bonus': round(section_bonus, 1),
            'contact_score': contact_score
        }
    }

import re  # add at top of file