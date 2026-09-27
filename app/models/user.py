from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Made nullable so new sign-ups don't crash if they don't have a role assigned yet
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=True) 
    
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # New column for our Passkey feature!
    recovery_passkey = db.Column(db.String(64), unique=True, nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_recovery_passkey(self):
        # Generates a 16-character code like A7B2-9F81-C4D3-E6H5
        hex_str = secrets.token_hex(8).upper()
        self.recovery_passkey = f"{hex_str[:4]}-{hex_str[4:8]}-{hex_str[8:12]}-{hex_str[12:]}"
        return self.recovery_passkey

    def __repr__(self):
        return f'<User {self.email}>'
