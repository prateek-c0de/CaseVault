from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.user import User
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        if User.query.filter_by(email=email).first():
            flash('Email already registered!', 'danger')
            return redirect(url_for('auth.register'))

        new_user = User(name=name, email=email)
        new_user.set_password(password)
        
        # Generate the secure recovery passkey
        passkey = new_user.generate_recovery_passkey()
        
        db.session.add(new_user)
        db.session.commit()

        return render_template('register_success.html', passkey=passkey)
        
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard.index'))
        else:
            flash('Invalid email or password', 'danger')

    return render_template('login.html')

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        passkey = request.form.get('passkey')
        new_password = request.form.get('new_password')

        user = User.query.filter_by(email=email).first()

        if user and user.recovery_passkey == passkey:
            user.set_password(new_password)
            db.session.commit()
            flash('Password successfully reset! You can now log in.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Invalid Email or Recovery Passkey. Access Denied.', 'danger')

    return render_template('forgot_password.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
