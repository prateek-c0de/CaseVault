from app import create_app, db
from app.models import user, role, case, evidence, custody, audit, verification

app = create_app()

with app.app_context():
    db.create_all()
    
    # --- AUTO-ASSIGN ADMIN ROLE FOR DEMO ---
    try:
        # 1. Create the Admin role in the database if it doesn't exist
        admin_role = role.Role.query.filter_by(name='Admin').first()
        if not admin_role:
            admin_role = role.Role(name='Admin')
            db.session.add(admin_role)
            db.session.commit()
        
        # 2. Find any users without a role (like you!) and make them an Admin
        users_without_roles = user.User.query.filter_by(role_id=None).all()
        for u in users_without_roles:
            u.role_id = admin_role.id
        db.session.commit()
    except Exception as e:
        print("Role auto-assign skipped:", e)
    # ----------------------------------------

if __name__ == '__main__':
    import os
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')
    app.run(debug=debug_mode)
