from app import create_app, db
from app.models import user, role, case, evidence, custody, audit, verification

app = create_app()

with app.app_context():
    db.create_all()
    # 1. Create the Admin role in the database if it doesn't exist
    admin_role = role.Role.query.filter_by(name='Admin').first()
    if not admin_role:
        admin_role = role.Role(name='Admin')
        db.session.add(admin_role)
        db.session.commit()

# 2. Check on EVERY click to make sure you have your Admin privileges
@app.before_request
def auto_assign_roles():
    try:
        admin_role = role.Role.query.filter_by(name='Admin').first()
        if admin_role:
            users_without_roles = user.User.query.filter_by(role_id=None).all()
            if users_without_roles:
                for u in users_without_roles:
                    u.role_id = admin_role.id
                db.session.commit()
    except Exception:
        pass

if __name__ == '__main__':
    import os
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')
    app.run(debug=debug_mode)
