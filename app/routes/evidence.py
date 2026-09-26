from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, send_file
from werkzeug.utils import secure_filename
from app.models import Evidence, Case, User, CustodyEvent
from app import db
from app.services.storage_service import StorageService
from app.services.hash_service import HashService
from app.services.qr_service import QRService
from app.services.audit_service import AuditService
from app.middleware.auth import login_required, role_required
import hashlib

evidence_bp = Blueprint('evidence', __name__)

@evidence_bp.route('/', methods=['GET'])
@login_required
def list_evidence():
    evidence_list = Evidence.query.order_by(Evidence.id.desc()).all()
    return render_template('evidence_list.html', evidence_list=evidence_list)

@evidence_bp.route('/<evidence_id>', methods=['GET'])
@login_required
def view_evidence(evidence_id):
    evidence = Evidence.query.filter_by(evidence_id=evidence_id).first_or_404()
    custody_events = CustodyEvent.query.filter_by(evidence_id=evidence.id).order_by(CustodyEvent.timestamp.asc()).all()
    
    AuditService.create_event('EVIDENCE_VIEWED', {'evidence_id': evidence_id}, user_id=session['user_id'])
    
    return render_template('evidence_details.html', evidence=evidence, custody_events=custody_events)

@evidence_bp.route('/register', methods=['GET', 'POST'])
@login_required
@role_required(['Administrator', 'Evidence Collector', 'Investigating Officer'])
def register():
    prefill_case = None
    case_id = request.args.get('case_id')
    if case_id:
        prefill_case = Case.query.get(case_id)
        
    if request.method == 'POST':
        case_number = request.form.get('case_number')
        name = request.form.get('name')
        evidence_type = request.form.get('type')
        description = request.form.get('description')
        location = request.form.get('collection_location')
        device = request.form.get('collection_device')
        file = request.files.get('file')
        
        if not file or file.filename == '':
            flash('No file selected', 'danger')
            return redirect(request.url)
            
        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mp3', 'wav', 'pdf', 'txt', 'doc', 'docx', 'csv', 'img', 'dd', 'raw'}
        if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in ALLOWED_EXTENSIONS:
            flash('File type not permitted for evidence.', 'danger')
            return redirect(request.url)
            
        case = Case.query.filter_by(case_number=case_number).first()
        if not case:
            case = Case(
                case_number=case_number, 
                title=f"Case {case_number}", 
                created_by_id=session['user_id']
            )
            db.session.add(case)
            db.session.commit()
            
        user_id = session['user_id']
        
        # --- NEW CLOUDINARY LOGIC ---
        
        # 1. Calculate the hash and file size in memory BEFORE uploading
        file_bytes = file.read()
        file_size = len(file_bytes)
        sha256_hash = hashlib.sha256(file_bytes).hexdigest()
        
        # 2. Reset the file pointer so the StorageService can read it
        file.seek(0)
        
        # 3. Create the database record
        evidence = Evidence(
            case_id=case.id,
            name=name,
            type=evidence_type,
            description=description,
            original_filename=secure_filename(file.filename),
            mime_type=file.content_type,
            collector_id=user_id,
            current_custodian_id=user_id,
            collection_location=location,
            collection_device=device,
            status='REGISTERED',
            sha256_hash=sha256_hash,
            file_size=file_size
        )
        db.session.add(evidence)
        db.session.commit()
        
        # 4. Upload file to Cloudinary
        storage = StorageService()
        cloud_url = storage.save(file, evidence.evidence_id)
        
        if cloud_url:
            evidence.storage_path = cloud_url
            
            # Generate QR
            QRService.generate_qr(evidence.evidence_id)
            
            # Initial custody event
            custody = CustodyEvent(
                evidence_id=evidence.id,
                receiver_id=user_id,
                action='REGISTERED',
                purpose='Initial Registration',
                location=location,
                evidence_hash=evidence.sha256_hash,
                previous_event_hash='GENESIS'
            )
            
            data = f"GENESIS{evidence.id}None{user_id}REGISTERED"
            custody.current_event_hash = hashlib.sha256(data.encode('utf-8')).hexdigest()
            db.session.add(custody)
            db.session.commit()
            
            AuditService.create_event(
                'EVIDENCE_REGISTERED', 
                {'evidence_id': evidence.evidence_id, 'hash': evidence.sha256_hash}, 
                user_id=user_id, 
                evidence_id=evidence.id,
                case_id=case.id
            )
            
            flash('Evidence registered successfully to Cloud Storage!', 'success')
            return redirect(url_for('evidence.view_evidence', evidence_id=evidence.evidence_id))
        else:
            flash('Failed to upload evidence to Cloudinary', 'danger')
            
    return render_template('register_evidence.html', prefill_case=prefill_case)