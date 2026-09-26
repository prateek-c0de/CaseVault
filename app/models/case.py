from app import db
from datetime import datetime

class Case(db.Model):
    __tablename__ = 'cases'
    id = db.Column(db.Integer, primary_key=True)
    case_number = db.Column(db.String(50), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    case_type = db.Column(db.String(100), default='General Investigation')
    status = db.Column(db.String(50), default='OPEN')
    investigating_officer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    investigating_officer_name = db.Column(db.String(255), nullable=True)
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    evidence_items = db.relationship('Evidence', backref='case', lazy=True)
    documents = db.relationship('Document', backref='case', lazy=True)

    investigating_officer = db.relationship('User', foreign_keys=[investigating_officer_id])
    created_by = db.relationship('User', foreign_keys=[created_by_id])

    def __repr__(self):
        return f'<Case {self.case_number}>'
