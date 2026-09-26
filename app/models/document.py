from app import db
from datetime import datetime
import uuid

class Document(db.Model):
    __tablename__ = 'documents'
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.String(50), unique=True, nullable=False, default=lambda: f"DOC-{datetime.utcnow().year}-{uuid.uuid4().hex[:6].upper()}")
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'), nullable=False)
    document_type = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    
    status = db.Column(db.String(50), default='ACTIVE')
    access_level = db.Column(db.String(50), default='RESTRICTED') # e.g. PUBLIC, RESTRICTED, CONFIDENTIAL
    
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Current version details denormalized for easy querying
    current_version = db.Column(db.Integer, default=1)
    file_name = db.Column(db.String(255))
    storage_path = db.Column(db.String(512))
    mime_type = db.Column(db.String(100))
    file_size = db.Column(db.Integer)
    sha256_hash = db.Column(db.String(64))
    
    # AI Intelligence Fields
    ai_summary = db.Column(db.Text, nullable=True)
    ai_classification = db.Column(db.String(100), nullable=True)
    ai_key_info = db.Column(db.Text, nullable=True)
    
    created_by = db.relationship('User', foreign_keys=[created_by_id])
    versions = db.relationship('DocumentVersion', backref='document', lazy=True, order_by="DocumentVersion.version_number")
    modification_requests = db.relationship('DocumentModificationRequest', backref='document', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Document {self.document_id}>'

class DocumentModificationRequest(db.Model):
    __tablename__ = 'document_modification_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.String(50), db.ForeignKey('documents.document_id'), nullable=False)
    requester_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    approver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    reason = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='PENDING') # PENDING, APPROVED, REJECTED
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    requester = db.relationship('User', foreign_keys=[requester_id])
    approver = db.relationship('User', foreign_keys=[approver_id])

class DocumentVersion(db.Model):
    __tablename__ = 'document_versions'
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id'), nullable=False)
    version_number = db.Column(db.Integer, nullable=False)
    
    file_name = db.Column(db.String(255), nullable=False)
    storage_path = db.Column(db.String(512), nullable=False)
    mime_type = db.Column(db.String(100))
    file_size = db.Column(db.Integer)
    sha256_hash = db.Column(db.String(64), nullable=False)
    
    uploaded_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    upload_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    change_summary = db.Column(db.String(255))
    
    uploaded_by = db.relationship('User', foreign_keys=[uploaded_by_id])
    
    def __repr__(self):
        return f'<DocumentVersion {self.document.document_id} v{self.version_number}>'
