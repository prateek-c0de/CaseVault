from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import Case, User, Document, Evidence
from app import db
from app.middleware.auth import login_required, role_required

cases_bp = Blueprint('cases', __name__)

@cases_bp.route('/', methods=['GET'])
@login_required
def list_cases():
    cases = Case.query.order_by(Case.created_at.desc()).all()
    return render_template('cases/list.html', cases=cases)

@cases_bp.route('/<int:case_id>', methods=['GET'])
@login_required
def view_case(case_id):
    case = Case.query.get_or_404(case_id)
    documents = Document.query.filter_by(case_id=case_id).order_by(Document.created_at.desc()).all()
    evidence_items = Evidence.query.filter_by(case_id=case_id).order_by(Evidence.created_at.desc()).all()
    return render_template('cases/view.html', case=case, documents=documents, evidence_items=evidence_items)

@cases_bp.route('/create', methods=['GET', 'POST'])
@login_required
@role_required(['Administrator', 'Investigating Officer'])
def create():
    if request.method == 'POST':
        case_number = request.form.get('case_number')
        title = request.form.get('title')
        description = request.form.get('description')
        case_type = request.form.get('case_type')
        investigating_officer_name = request.form.get('investigating_officer_name')

        if Case.query.filter_by(case_number=case_number).first():
            flash('Case number already exists.', 'danger')
            return redirect(request.url)
            
        case = Case(
            case_number=case_number,
            title=title,
            description=description,
            case_type=case_type,
            investigating_officer_name=investigating_officer_name,
            created_by_id=session['user_id']
        )
        db.session.add(case)
        db.session.commit()
        
        flash('Case created successfully', 'success')
        return redirect(url_for('cases.view_case', case_id=case.id))
        
    officers = User.query.join(User.role).filter(User.role.has(name='Investigating Officer')).all()
    return render_template('cases/create.html', officers=officers)
