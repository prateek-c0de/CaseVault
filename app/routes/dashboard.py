from flask import Blueprint, render_template, session
from app.models import Evidence, CustodyEvent, Case, User
from app.middleware.auth import login_required

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required
def index():
    user = User.query.get(session['user_id'])
    
    # Stats
    total_evidence = Evidence.query.count()
    total_cases = Case.query.count()
    my_evidence = Evidence.query.filter_by(current_custodian_id=user.id).count()
    pending_transfers = CustodyEvent.query.filter_by(receiver_id=user.id, status='PENDING').count()
    
    # Tamper alerts
    tamper_alerts = Evidence.query.filter(Evidence.status.ilike('%TAMPER%')).all()
    
    # Recent activity
    recent_evidence = Evidence.query.order_by(Evidence.id.desc()).limit(5).all()
    
    # Pending items for this user
    my_pending_transfers = CustodyEvent.query.filter_by(
        receiver_id=user.id, status='PENDING'
    ).order_by(CustodyEvent.id.desc()).all()
    
    return render_template(
        'dashboard.html', 
        user=user,
        stats={
            'total_evidence': total_evidence,
            'total_cases': total_cases,
            'my_evidence': my_evidence,
            'pending_transfers': pending_transfers,
            'tamper_alerts_count': len(tamper_alerts)
        },
        recent_evidence=recent_evidence,
        my_pending_transfers=my_pending_transfers,
        tamper_alerts=tamper_alerts
    )

@dashboard_bp.route('/qr/evidence/<path:qr_data>')
@login_required
def qr_lookup(qr_data):
    # Strip any prefix like "EVIDENCE_ID:" if present
    evidence_id = qr_data.replace('EVIDENCE_ID:', '').strip()
    
    # Check if the evidence exists
    evidence = Evidence.query.filter_by(evidence_id=evidence_id).first()
    if not evidence:
        from flask import flash, redirect, url_for
        flash(f'Evidence {evidence_id} not found from QR scan.', 'danger')
        return redirect(url_for('dashboard.index'))
        
    from flask import redirect, url_for
    return redirect(url_for('evidence.view_evidence', evidence_id=evidence.evidence_id))

