from flask_jwt_extended import decode_token
from datetime import datetime, timedelta
import jwt
import os

def create_access_token(user_id, user_role):
    from flask import current_app
    payload = {
        'user_id': user_id,
        'role': user_role,
        'exp': datetime.utcnow() + timedelta(hours=24),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')

def decode_access_token(token):
    from flask import current_app
    try:
        payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def hash_password(password):
    from werkzeug.security import generate_password_hash
    return generate_password_hash(password)

def verify_password(password_hash, password):
    from werkzeug.security import check_password_hash
    return check_password_hash(password_hash, password)

def verify_admin_role(role):
    return role == 'admin'

def verify_company_role(role):
    return role == 'company'

def verify_student_role(role):
    return role == 'student'
