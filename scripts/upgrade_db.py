import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import Role, User

app = create_app()

def upgrade_db():
    with app.app_context():
        # Create any new tables (e.g. documents, document_versions)
        db.create_all()
        print("Ensured all tables exist.")
        
        # Add new columns to cases table using raw SQL for SQLite
        try:
            db.session.execute(db.text("ALTER TABLE cases ADD COLUMN case_type VARCHAR(100) DEFAULT 'General Investigation'"))
            print("Added case_type to cases.")
        except Exception as e:
            print("case_type might already exist:", e)

        try:
            db.session.execute(db.text("ALTER TABLE cases ADD COLUMN investigating_officer_id INTEGER REFERENCES users(id)"))
            print("Added investigating_officer_id to cases.")
        except Exception as e:
            print("investigating_officer_id might already exist:", e)

        try:
            db.session.execute(db.text("ALTER TABLE cases ADD COLUMN created_by_id INTEGER REFERENCES users(id)"))
            print("Added created_by_id to cases.")
        except Exception as e:
            print("created_by_id might already exist:", e)

        # Seed new roles
        legal_officer_role = Role.query.filter_by(name='Legal Officer').first()
        if not legal_officer_role:
            legal_officer_role = Role(name='Legal Officer')
            db.session.add(legal_officer_role)
            db.session.commit()
            print("Added Legal Officer role.")

        db.session.commit()
        print("Upgrade complete.")

if __name__ == '__main__':
    upgrade_db()
