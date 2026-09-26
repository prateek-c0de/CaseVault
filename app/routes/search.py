from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import Case, Document, Evidence, User
from app.middleware.auth import login_required
from sqlalchemy import or_

search_bp = Blueprint('search', __name__)

@search_bp.route('/', methods=['GET'])
@login_required
def query():
    q = request.args.get('q', '').strip()
    if not q:
        return render_template('search/results.html', query=q, cases=[], documents=[], evidence=[])
        
    search_term = f"%{q}%"
    
    cases = Case.query.filter(
        or_(
            Case.case_number.ilike(search_term),
            Case.title.ilike(search_term),
            Case.case_type.ilike(search_term)
        )
    ).limit(20).all()
    
    documents = Document.query.filter(
        or_(
            Document.document_id.ilike(search_term),
            Document.title.ilike(search_term),
            Document.document_type.ilike(search_term)
        )
    ).limit(20).all()
    
    evidence = Evidence.query.filter(
        or_(
            Evidence.evidence_id.ilike(search_term),
            Evidence.name.ilike(search_term),
            Evidence.type.ilike(search_term)
        )
    ).limit(20).all()
    
    return render_template('search/results.html', query=q, cases=cases, documents=documents, evidence=evidence)
