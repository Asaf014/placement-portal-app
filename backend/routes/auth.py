from flask import Blueprint, request, jsonify
from functools import wraps
from utils.auth import create_access_token, decode_access_token
from services.user_service import UserService
from models import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        payload = decode_access_token(token)
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        user = UserService.get_user(payload['user_id'])
        if not user or user.is_blacklisted:
            return jsonify({'error': 'User not authorized'}), 401
        
        return f(payload['user_id'], payload['role'], *args, **kwargs)
    
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(user_id, role, *args, **kwargs):
        if role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(user_id, role, *args, **kwargs)
    return decorated

def company_required(f):
    @wraps(f)
    def decorated(user_id, role, *args, **kwargs):
        if role != 'company':
            return jsonify({'error': 'Company access required'}), 403
        return f(user_id, role, *args, **kwargs)
    return decorated

def student_required(f):
    @wraps(f)
    def decorated(user_id, role, *args, **kwargs):
        if role != 'student':
            return jsonify({'error': 'Student access required'}), 403
        return f(user_id, role, *args, **kwargs)
    return decorated

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')
    
    if not email or not password or not role:
        return jsonify({'error': 'Email, password, and role are required'}), 400
    
    if role == 'admin':
        return jsonify({'error': 'Admin registration not allowed'}), 403
    
    user, message = UserService.create_user(email, password, role)
    if not user:
        return jsonify({'error': message}), 400
    
    try:
        if role == 'student' and data.get('student_data'):
            student_data = data.get('student_data')
            student, student_msg = UserService.register_student(
                user.id,
                student_data.get('first_name'),
                student_data.get('last_name'),
                student_data.get('roll_number'),
                student_data.get('phone'),
                student_data.get('branch'),
                student_data.get('cgpa'),
                student_data.get('resume_url')
            )
            if not student:
                return jsonify({'error': student_msg}), 400
                
        elif role == 'company' and data.get('company_data'):
            company_data = data.get('company_data')
            company, company_msg = UserService.register_company(
                user.id,
                company_data.get('company_name'),
                company_data.get('website'),
                company_data.get('hr_contact'),
                company_data.get('hr_phone'),
                company_data.get('description'),
                company_data.get('industry')
            )
            if not company:
                return jsonify({'error': company_msg}), 400
    except Exception as e:
        return jsonify({'error': f'Error creating profile: {str(e)}'}), 400
    
    return jsonify({
        'message': message,
        'user_id': user.id,
        'email': user.email,
        'role': user.role
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400
    
    user = UserService.authenticate(email, password)
    if not user:
        return jsonify({'error': 'Invalid email or password'}), 401
    
    if user.is_blacklisted:
        return jsonify({'error': 'User account is blacklisted'}), 403
    
    token = create_access_token(user.id, user.role)
    return jsonify({
        'token': token,
        'user_id': user.id,
        'email': user.email,
        'role': user.role
    }), 200

@auth_bp.route('/verify-token', methods=['GET'])
@token_required
def verify_token(user_id, role):
    return jsonify({
        'user_id': user_id,
        'role': role
    }), 200
