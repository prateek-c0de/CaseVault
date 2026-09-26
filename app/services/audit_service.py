import json
import hashlib
from datetime import datetime
from app import db
from app.models import AuditLog

class AuditService:
    @staticmethod
    def _calculate_hash(previous_hash, event_type, user_id, evidence_id, case_id, document_id, canonical_event_data):
        data = f"{previous_hash}{event_type}{user_id}{evidence_id}{case_id}{document_id}{canonical_event_data}"
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    @staticmethod
    def create_event(event_type, event_data, user_id=None, evidence_id=None, case_id=None, document_id=None):
        last_event = AuditLog.query.order_by(AuditLog.id.desc()).first()
        prev_hash = last_event.current_hash if last_event else 'GENESIS'
        
        canonical_event_data = json.dumps(event_data, sort_keys=True)
        current_hash = AuditService._calculate_hash(
            prev_hash, event_type, user_id, evidence_id, case_id, document_id, canonical_event_data
        )
        
        audit_log = AuditLog(
            event_type=event_type,
            user_id=user_id,
            evidence_id=evidence_id,
            case_id=case_id,
            document_id=document_id,
            event_data=event_data,
            previous_hash=prev_hash,
            current_hash=current_hash
        )
        db.session.add(audit_log)
        db.session.commit()
        return audit_log

    @staticmethod
    def verify_chain():
        logs = AuditLog.query.order_by(AuditLog.id.asc()).all()
        if not logs:
            return True, []
            
        invalid_blocks = []
        expected_previous = "GENESIS"
        
        for log in logs:
            canonical_event_data = json.dumps(log.event_data, sort_keys=True)
            calculated_hash = AuditService._calculate_hash(
                expected_previous, log.event_type, log.user_id, log.evidence_id, log.case_id, log.document_id, canonical_event_data
            )
            
            if log.previous_hash != expected_previous or log.current_hash != calculated_hash:
                invalid_blocks.append(log.id)
                
            expected_previous = log.current_hash
            
        return len(invalid_blocks) == 0, invalid_blocks

