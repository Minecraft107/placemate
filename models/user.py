from extensions import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    cgpa = db.Column(db.Float)
    backlogs = db.Column(db.Integer, default=0)
    branch = db.Column(db.String(50))
    skills = db.Column(db.Text)          # store as comma-separated string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    resumes = db.relationship('Resume', backref='user', lazy=True)
    predictions = db.relationship('Prediction', backref='user', lazy=True)