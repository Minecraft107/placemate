from extensions import db
from datetime import datetime

class Resume(db.Model):
    __tablename__ = 'resumes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    filename = db.Column(db.String(255))
    file_path = db.Column(db.String(500))
    ats_score = db.Column(db.Float)
    keywords_matched = db.Column(db.JSON)
    missing_keywords = db.Column(db.JSON)
    raw_text = db.Column(db.Text)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)