from extensions import db
from datetime import datetime

class Prediction(db.Model):
    __tablename__ = 'predictions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    cgpa = db.Column(db.Float)
    backlogs = db.Column(db.Integer)
    skills_score = db.Column(db.Float)
    ats_score = db.Column(db.Float)
    predicted_outcome = db.Column(db.String(20))   # "Placed" or "Not Placed"
    confidence = db.Column(db.Float)
    model_used = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)