from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
from werkzeug.utils import secure_filename
from extensions import db
from models.resume import Resume
from services.resume_parser import extract_text, extract_skills_from_text
from services.ats_scorer import calculate_ats_score

resume_bp = Blueprint('resume', __name__)

ALLOWED_EXTENSIONS = {'pdf', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@resume_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_resume():
    user_id = get_jwt_identity()
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if not allowed_file(file.filename):
        return jsonify({'error': 'Only PDF and DOCX files allowed'}), 400
    
    filename = secure_filename(file.filename)
    upload_folder = current_app.config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)
    
    # Save with user_id prefix to avoid conflicts
    unique_name = f"{user_id}_{filename}"
    file_path = os.path.join(upload_folder, unique_name)
    file.save(file_path)
    
    # Parse and score
    try:
        text = extract_text(file_path)
        score_data = calculate_ats_score(text)
        
        resume = Resume(
            user_id=user_id,
            filename=filename,
            file_path=file_path,
            raw_text=text,
            ats_score=score_data['ats_score'],
            keywords_matched=score_data['keywords_matched'],
            missing_keywords=score_data['missing_keywords']
        )
        db.session.add(resume)
        db.session.commit()
        
        return jsonify({
            'resume_id': resume.id,
            'ats_score': score_data['ats_score'],
            'keywords_matched': score_data['keywords_matched'],
            'missing_keywords': score_data['missing_keywords'],
            'suggestions': generate_suggestions(score_data)
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_suggestions(score_data):
    suggestions = []
    if score_data['ats_score'] < 50:
        suggestions.append("Your resume score is low. Add more relevant technical keywords.")
    if score_data['missing_keywords']:
        suggestions.append(f"Consider adding these skills: {', '.join(score_data['missing_keywords'][:5])}")
    return suggestions