from app import db
from datetime import datetime

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    evidence_id = db.Column(db.Integer, db.ForeignKey('evidence.id'), nullable=True)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'), nullable=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), nullable=True)
    
    event_data = db.Column(db.JSON, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    previous_hash = db.Column(db.String(64))
    current_hash = db.Column(db.String(64), nullable=False)

    user = db.relationship('User')
    evidence = db.relationship('Evidence')
    case = db.relationship('Case')
    document = db.relationship('Document')

    def __repr__(self):
        return f'<AuditLog {self.event_type} at {self.timestamp}>'

