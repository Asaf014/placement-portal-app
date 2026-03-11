from flask import Blueprint, request, jsonify
from routes.auth import token_required, student_required
from services.user_service import StudentService, PlacementDriveService, ApplicationService
from models import db, Student, PlacementDrive, Application, Company, User
from datetime import datetime
from tasks.celery_tasks import export_student_applications_csv

student_bp = Blueprint('student', __name__, url_prefix='/student')

@student_bp.route('/register', methods=['POST'])
@token_required
@student_required
def register_student(user_id, role):
    data = request.get_json()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    roll_number = data.get('roll_number')
    branch = data.get('branch')
    batch = data.get('batch')
    cgpa = float(data.get('cgpa', 0.0))
    
    student, message = StudentService.register_student(
        user_id, first_name, last_name, roll_number, branch, batch, cgpa
    )
    
    if not student:
        return jsonify({'error': message}), 400
    
    return jsonify({
        'message': message,
        'student_id': student.id
    }), 201

@student_bp.route('/profile', methods=['GET'])
@token_required
@student_required
def get_profile(user_id, role):
    student = Student.query.filter_by(user_id=user_id).first()
    if not student:
        return jsonify({'error': 'Student profile not found'}), 404
    
    return jsonify({
        'id': student.id,
        'first_name': student.first_name,
        'last_name': student.last_name,
        'roll_number': student.roll_number,
        'branch': student.branch,
        'batch': student.batch,
        'cgpa': student.cgpa,
        'phone': student.phone,
        'resume_url': student.resume_url,
        'is_active': student.is_active
    }), 200

@student_bp.route('/profile', methods=['PUT'])
@token_required
@student_required
def update_profile(user_id, role):
    data = request.get_json()
    student = Student.query.filter_by(user_id=user_id).first()
    
    if not student:
        return jsonify({'error': 'Student profile not found'}), 404
    
    student = StudentService.update_student(
        student.id,
        first_name=data.get('first_name', student.first_name),
        last_name=data.get('last_name', student.last_name),
        branch=data.get('branch', student.branch),
        batch=data.get('batch', student.batch),
        cgpa=data.get('cgpa', student.cgpa),
        phone=data.get('phone', student.phone),
        resume_url=data.get('resume_url', student.resume_url)
    )
    
    return jsonify({'message': 'Profile updated'}), 200

@student_bp.route('/available-drives', methods=['GET'])
@token_required
@student_required
def get_available_drives(user_id, role):
    student = Student.query.filter_by(user_id=user_id).first()
    if not student:
        return jsonify({'error': 'Student profile not found'}), 404
    
    drives = PlacementDriveService.get_all_drives(status='approved')
    
    eligible_drives = []
    for drive in drives:
        if datetime.utcnow() > drive.application_deadline:
            continue
        
        if drive.min_cgpa and student.cgpa < drive.min_cgpa:
            continue
        
        already_applied = Application.query.filter_by(
            student_id=student.id,
            drive_id=drive.id
        ).first()
        
        if already_applied:
            continue
        
        eligible_drives.append({
            'id': drive.id,
            'job_title': drive.job_title,
            'job_description': drive.job_description,
            'company_name': drive.company.company_name,
            'min_cgpa': drive.min_cgpa,
            'salary_package': drive.salary_package,
            'application_deadline': drive.application_deadline.isoformat(),
            'interview_date': drive.interview_date.isoformat() if drive.interview_date else None
        })
    
    return jsonify({'drives': eligible_drives}), 200

@student_bp.route('/applications', methods=['GET'])
@token_required
@student_required
def get_my_applications(user_id, role):
    student = Student.query.filter_by(user_id=user_id).first()
    if not student:
        return jsonify({'error': 'Student profile not found'}), 404
    
    applications = ApplicationService.get_student_applications(student.id)
    
    return jsonify({
        'applications': [{
            'id': a.id,
            'job_title': a.placement_drive.job_title,
            'company_name': a.placement_drive.company.company_name,
            'status': a.status,
            'applied_at': a.applied_at.isoformat(),
            'shortlisted_at': a.shortlisted_at.isoformat() if a.shortlisted_at else None,
            'selected_at': a.selected_at.isoformat() if a.selected_at else None,
            'rejected_at': a.rejected_at.isoformat() if a.rejected_at else None
        } for a in applications]
    }), 200

@student_bp.route('/apply/<int:drive_id>', methods=['POST'])
@token_required
@student_required
def apply_to_drive(user_id, role, drive_id):
    student = Student.query.filter_by(user_id=user_id).first()
    if not student:
        return jsonify({'error': 'Student profile not found'}), 404
    
    drive = PlacementDriveService.get_drive(drive_id)
    if not drive:
        return jsonify({'error': 'Drive not found'}), 404
    
    if drive.status != 'approved':
        return jsonify({'error': 'Drive is not approved'}), 403
    
    if datetime.utcnow() > drive.application_deadline:
        return jsonify({'error': 'Application deadline has passed'}), 403
    
    if student.cgpa < drive.min_cgpa:
        return jsonify({'error': 'CGPA does not meet minimum requirement'}), 403
    
    application, message = ApplicationService.apply_to_drive(student.id, drive_id)
    if not application:
        return jsonify({'error': message}), 400
    
    return jsonify({'message': message}), 201

@student_bp.route('/dashboard', methods=['GET'])
@token_required
@student_required
def dashboard(user_id, role):
    student = Student.query.filter_by(user_id=user_id).first()
    if not student:
        return jsonify({'error': 'Student profile not found'}), 404
    
    applications = ApplicationService.get_student_applications(student.id)
    total_applied = len(applications)
    total_selected = len([a for a in applications if a.status == 'selected'])
    total_rejected = len([a for a in applications if a.status == 'rejected'])
    
    available_drives = PlacementDriveService.get_all_drives(status='approved')
    available_count = sum(1 for d in available_drives if datetime.utcnow() < d.application_deadline)
    
    return jsonify({
        'total_applications': total_applied,
        'selected': total_selected,
        'rejected': total_rejected,
        'available_drives': available_count
    }), 200

@student_bp.route('/export-applications', methods=['POST'])
@token_required
@student_required
def export_applications(user_id, role):
    student = Student.query.filter_by(user_id=user_id).first()
    if not student:
        return jsonify({'error': 'Student profile not found'}), 404
    
    export_student_applications_csv.delay(student.id)
    
    return jsonify({'message': 'Export initiated. You will receive the CSV via email'}), 202

@student_bp.route('/placement-history', methods=['GET'])
@token_required
@student_required
def get_placement_history(user_id, role):
    student = Student.query.filter_by(user_id=user_id).first()
    if not student:
        return jsonify({'error': 'Student profile not found'}), 404
    
    selected_apps = Application.query.filter_by(
        student_id=student.id,
        status='selected'
    ).all()
    
    return jsonify({
        'selected_placements': [{
            'company_name': a.placement_drive.company.company_name,
            'job_title': a.placement_drive.job_title,
            'salary_package': a.placement_drive.salary_package,
            'selected_at': a.selected_at.isoformat()
        } for a in selected_apps]
    }), 200

@student_bp.route('/search-drives', methods=['GET'])
@token_required
@student_required
def search_drives(user_id, role):
    student = Student.query.filter_by(user_id=user_id).first()
    if not student:
        return jsonify({'error': 'Student profile not found'}), 404
    
    search_query = request.args.get('q', '')
    
    drives = PlacementDrive.query.filter(
        PlacementDrive.status == 'approved',
        (PlacementDrive.job_title.ilike(f'%{search_query}%')) |
        (PlacementDrive.company.has(Company.company_name.ilike(f'%{search_query}%')))
    ).all()
    
    return jsonify({
        'drives': [{
            'id': d.id,
            'job_title': d.job_title,
            'company_name': d.company.company_name,
            'salary_package': d.salary_package,
            'application_deadline': d.application_deadline.isoformat()
        } for d in drives if datetime.utcnow() < d.application_deadline]
    }), 200
