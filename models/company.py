from extensions import db
from datetime import datetime

class Company(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    min_cgpa = db.Column(db.Float, nullable=False)
    backlogs_allowed = db.Column(db.Integer, default=0)
    required_skills = db.Column(db.JSON)
    min_package = db.Column(db.Float)
    eligible_branches = db.Column(db.String(200))