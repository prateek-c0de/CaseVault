from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.utils import secure_filename
from app.models import Document, DocumentVersion, Case, User
from app import db
from app.services.storage_service import StorageService
from app.services.hash_service import HashService
from app.services.audit_service import AuditService
from app.services.qr_service import QRService
from app.middleware.auth import login_required, role_required
import os

documents_bp = Blueprint('documents', __name__)

@documents_bp.route('/case/<int:case_id>/upload', methods=['GET', 'POST'])
@login_required
@role_required(['Administrator', 'Investigating Officer', 'Forensic Analyst', 'Legal Officer'])
def upload(case_id):
    case = Case.query.get_or_404(case_id)
    if request.method == 'POST':
        document_type = request.form.get('document_type')
        title = request.form.get('title')
        description = request.form.get('description')
        access_level = request.form.get('access_level', 'RESTRICTED')
        file = request.files.get('file')
        
        if not file or file.filename == '':
            flash('No file selected', 'danger')
            return redirect(request.url)
            
        # Create Document
        user_id = session['user_id']
        document = Document(
            case_id=case.id,
            document_type=document_type,
            title=title,
            description=description,
            access_level=access_level,
            created_by_id=user_id,
            current_version=1,
            mime_type=file.content_type,
            file_name=secure_filename(file.filename)
        )
        db.session.add(document)
        db.session.flush() # get ID
        
        storage = StorageService()
        filepath = storage.save(file, f"{document.document_id}_v1")
        
        if filepath:
            document.storage_path = filepath
            document.file_size = os.path.getsize(filepath)
            document.sha256_hash = HashService.calculate_sha256(filepath)
            
            # --- AI Mock Integration ---
            document.ai_classification = "High-Confidence " + document_type
            document.ai_summary = f"Automated summary for {title}. This document pertains to {document_type.lower()} records and indicates standard investigative procedures."
            document.ai_key_info = "Entities: Suspect A, Location B.\nKeywords: Investigation, Evidence.\nRisk Level: Moderate."
            
            # --- QR Code Generation ---
            QRService.generate_qr(document.document_id)
            
            # Create Version record
            version = DocumentVersion(
                document_id=document.id,
                version_number=1,
                file_name=secure_filename(file.filename),
                storage_path=filepath,
                mime_type=file.content_type,
                file_size=document.file_size,
                sha256_hash=document.sha256_hash,
                uploaded_by_id=user_id,
                change_summary='Initial upload'
            )
            db.session.add(version)
            db.session.commit()
            
            AuditService.create_event(
                'DOCUMENT_UPLOADED', 
                {'document_id': document.document_id, 'version': 1, 'hash': document.sha256_hash}, 
                user_id=user_id, 
                case_id=case.id
            )
            flash('Document uploaded securely. AI intelligence generated and QR assigned.', 'success')
            return redirect(url_for('documents.view_document', document_id=document.document_id))
            
    return render_template('documents/upload.html', case=case)

@documents_bp.route('/<document_id>', methods=['GET'])
@login_required
def view_document(document_id):
    doc = Document.query.filter_by(document_id=document_id).first_or_404()
    
    # Audit log
    AuditService.create_event('DOCUMENT_VIEWED', {'document_id': doc.document_id}, user_id=session['user_id'], case_id=doc.case_id)
    return render_template('documents/view.html', document=doc)

@documents_bp.route('/<document_id>/download', methods=['GET'])
@login_required
def download_document(document_id):
    doc = Document.query.filter_by(document_id=document_id).first_or_404()
    import uuid
    fingerprint = str(uuid.uuid4())
    
    # Traceable fingerprint log
    AuditService.create_event(
        'DOCUMENT_DOWNLOADED', 
        {'document_id': doc.document_id, 'fingerprint_id': fingerprint}, 
        user_id=session['user_id'], 
        case_id=doc.case_id
    )
    from flask import send_file
    return send_file(doc.storage_path, as_attachment=True, download_name=doc.file_name)

from app.models import DocumentModificationRequest

@documents_bp.route('/<document_id>/request_modification', methods=['POST'])
@login_required
def request_modification(document_id):
    doc = Document.query.filter_by(document_id=document_id).first_or_404()
    reason = request.form.get('reason')
    
    if not reason:
        flash('Reason is required.', 'danger')
        return redirect(url_for('documents.view_document', document_id=document_id))
        
    req = DocumentModificationRequest(
        document_id=doc.document_id,
        requester_id=session['user_id'],
        reason=reason
    )
    db.session.add(req)
    db.session.commit()
    
    AuditService.create_event(
        'MODIFICATION_REQUESTED',
        {'document_id': doc.document_id, 'request_id': req.id},
        user_id=session['user_id'],
        case_id=doc.case_id
    )
    
    flash('Modification request submitted successfully. Pending approval.', 'success')
    return redirect(url_for('documents.view_document', document_id=document_id))

@documents_bp.route('/request/<int:request_id>/approve', methods=['POST'])
@login_required
@role_required(['Administrator', 'Investigating Officer'])
def approve_modification(request_id):
    req = DocumentModificationRequest.query.get_or_404(request_id)
    req.status = 'APPROVED'
    req.approver_id = session['user_id']
    db.session.commit()
    
    AuditService.create_event(
        'MODIFICATION_APPROVED',
        {'document_id': req.document_id, 'request_id': req.id},
        user_id=session['user_id']
    )
    flash('Modification request approved.', 'success')
    return redirect(url_for('documents.view_document', document_id=req.document_id))

@documents_bp.route('/request/<int:request_id>/reject', methods=['POST'])
@login_required
@role_required(['Administrator', 'Investigating Officer'])
def reject_modification(request_id):
    req = DocumentModificationRequest.query.get_or_404(request_id)
    req.status = 'REJECTED'
    req.approver_id = session['user_id']
    db.session.commit()
    
    AuditService.create_event(
        'MODIFICATION_REJECTED',
        {'document_id': req.document_id, 'request_id': req.id},
        user_id=session['user_id']
    )
    flash('Modification request rejected.', 'warning')
    return redirect(url_for('documents.view_document', document_id=req.document_id))
