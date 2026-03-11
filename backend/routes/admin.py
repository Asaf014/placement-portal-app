from flask import Blueprint, request, jsonify
from routes.auth import token_required, admin_required
from services.user_service import UserService, CompanyService, StudentService, PlacementDriveService, ApplicationService
from models import db, User, Company, Student, PlacementDrive, Application, Notification
from utils.email import send_notification

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard', methods=['GET'])
@token_required
@admin_required
def dashboard(user_id, role):
    total_students = Student.query.count()
    total_companies = Company.query.count()
    total_drives = PlacementDrive.query.count()
    total_applications = Application.query.count()
    
    return jsonify({
        'total_students': total_students,
        'total_companies': total_companies,
        'total_drives': total_drives,
        'total_applications': total_applications
    }), 200

@admin_bp.route('/companies/pending', methods=['GET'])
@token_required
@admin_required
def get_pending_companies(user_id, role):
    companies = CompanyService.get_all_companies(approval_status='pending')
    return jsonify({
        'companies': [{
            'id': c.id,
            'company_name': c.company_name,
            'website': c.website,
            'hr_contact': c.hr_contact,
            'approval_status': c.approval_status,
            'created_at': c.created_at.isoformat()
        } for c in companies]
    }), 200

@admin_bp.route('/companies/<int:company_id>/approve', methods=['PUT'])
@token_required
@admin_required
def approve_company(user_id, role, company_id):
    success = CompanyService.approve_company(company_id)
    if success:
        return jsonify({'message': 'Company approved'}), 200
    return jsonify({'error': 'Company not found'}), 404

@admin_bp.route('/companies/<int:company_id>/reject', methods=['PUT'])
@token_required
@admin_required
def reject_company(user_id, role, company_id):
    success = CompanyService.reject_company(company_id)
    if success:
        return jsonify({'message': 'Company rejected'}), 200
    return jsonify({'error': 'Company not found'}), 404

@admin_bp.route('/drives/pending', methods=['GET'])
@token_required
@admin_required
def get_pending_drives(user_id, role):
    drives = PlacementDriveService.get_all_drives(status='pending')
    return jsonify({
        'drives': [{
            'id': d.id,
            'job_title': d.job_title,
            'company_name': d.company.company_name,
            'status': d.status,
            'application_deadline': d.application_deadline.isoformat(),
            'created_at': d.created_at.isoformat()
        } for d in drives]
    }), 200

@admin_bp.route('/drives', methods=['GET'])
@token_required
@admin_required
def get_all_drives(user_id, role):
    drives = PlacementDriveService.get_all_drives()
    return jsonify({
        'drives': [{
            'id': d.id,
            'job_title': d.job_title,
            'company_name': d.company.company_name,
            'status': d.status,
            'application_deadline': d.application_deadline.isoformat()
        } for d in drives]
    }), 200

@admin_bp.route('/drives/<int:drive_id>/approve', methods=['PUT'])
@token_required
@admin_required
def approve_drive(user_id, role, drive_id):
    success = PlacementDriveService.approve_drive(drive_id)
    if success:
        return jsonify({'message': 'Drive approved'}), 200
    return jsonify({'error': 'Drive not found'}), 404

@admin_bp.route('/drives/<int:drive_id>/reject', methods=['PUT'])
@token_required
@admin_required
def reject_drive(user_id, role, drive_id):
    success = PlacementDriveService.reject_drive(drive_id)
    if success:
        return jsonify({'message': 'Drive rejected'}), 200
    return jsonify({'error': 'Drive not found'}), 404

@admin_bp.route('/students', methods=['GET'])
@token_required
@admin_required
def get_all_students(user_id, role):
    search = request.args.get('search', '')
    students = Student.query.filter(
        (Student.first_name.ilike(f'%{search}%')) |
        (Student.last_name.ilike(f'%{search}%')) |
        (Student.roll_number.ilike(f'%{search}%'))
    ).all()
    
    return jsonify({
        'students': [{
            'id': s.id,
            'first_name': s.first_name,
            'last_name': s.last_name,
            'roll_number': s.roll_number,
            'branch': s.branch,
            'cgpa': s.cgpa,
            'is_active': s.is_active
        } for s in students]
    }), 200

@admin_bp.route('/companies', methods=['GET'])
@token_required
@admin_required
def get_all_companies(user_id, role):
    search = request.args.get('search', '')
    companies = Company.query.filter(
        (Company.company_name.ilike(f'%{search}%')) |
        (Company.website.ilike(f'%{search}%'))
    ).all()
    
    return jsonify({
        'companies': [{
            'id': c.id,
            'company_name': c.company_name,
            'website': c.website,
            'hr_contact': c.hr_contact,
            'approval_status': c.approval_status,
            'is_active': c.is_active
        } for c in companies]
    }), 200

@admin_bp.route('/students/<int:student_id>/blacklist', methods=['PUT'])
@token_required
@admin_required
def blacklist_student(user_id, role, student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    
    UserService.blacklist_user(student.user_id)
    return jsonify({'message': 'Student blacklisted'}), 200

@admin_bp.route('/companies/<int:company_id>/blacklist', methods=['PUT'])
@token_required
@admin_required
def blacklist_company(user_id, role, company_id):
    company = Company.query.get(company_id)
    if not company:
        return jsonify({'error': 'Company not found'}), 404
    
    UserService.blacklist_user(company.user_id)
    return jsonify({'message': 'Company blacklisted'}), 200

@admin_bp.route('/applications', methods=['GET'])
@token_required
@admin_required
def get_all_applications(user_id, role):
    applications = Application.query.all()
    return jsonify({
        'applications': [{
            'id': a.id,
            'student_name': f"{a.student.first_name} {a.student.last_name}",
            'drive_title': a.placement_drive.job_title,
            'company': a.placement_drive.company.company_name,
            'status': a.status,
            'applied_at': a.applied_at.isoformat()
        } for a in applications]
    }), 200

@admin_bp.route('/statistics', methods=['GET'])
@token_required
@admin_required
def get_statistics(user_id, role):
    total_students = Student.query.count()
    total_companies = Company.query.count()
    approved_companies = Company.query.filter_by(approval_status='approved').count()
    total_drives = PlacementDrive.query.count()
    approved_drives = PlacementDrive.query.filter_by(status='approved').count()
    total_applications = Application.query.count()
    selected = Application.query.filter_by(status='selected').count()
    
    return jsonify({
        'total_students': total_students,
        'total_companies': total_companies,
        'approved_companies': approved_companies,
        'total_drives': total_drives,
        'approved_drives': approved_drives,
        'total_applications': total_applications,
        'selected_students': selected
    }), 200
