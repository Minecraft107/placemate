import pdfplumber
from docx import Document
import re

def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text(file_path):
    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        return extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file type")

def extract_skills_from_text(text):
    # Comprehensive skill keyword list
    skill_keywords = [
        'python', 'java', 'javascript', 'c++', 'c#', 'sql', 'mysql', 
        'postgresql', 'mongodb', 'react', 'angular', 'vue', 'node.js',
        'flask', 'django', 'spring', 'machine learning', 'deep learning',
        'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy',
        'git', 'docker', 'kubernetes', 'aws', 'azure', 'linux',
        'html', 'css', 'bootstrap', 'rest api', 'graphql', 'data analysis'
    ]
    
    text_lower = text.lower()
    found = [skill for skill in skill_keywords if skill in text_lower]
    return found