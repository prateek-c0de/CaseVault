from app import create_app, db
from app.models import user, role, case, evidence, custody, audit, verification

app = create_app()

# Automatically create the fresh database and all tables when the app starts!
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    import os
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')
    app.run(debug=debug_mode)
