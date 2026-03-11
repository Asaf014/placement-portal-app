from flask import Blueprint, request, jsonify
from routes.auth import token_required, company_required
from services.user_service import CompanyService, PlacementDriveService, ApplicationService
from models import db, Company, PlacementDrive, Application, Student
from datetime import datetime

company_bp = Blueprint('company', __name__, url_prefix='/company')

@company_bp.route('/register', methods=['POST'])
@token_required
@company_required
def register_company(user_id, role):
    data = request.get_json()
    company_name = data.get('company_name')
    website = data.get('website')
    hr_contact = data.get('hr_contact')
    hr_phone = data.get('hr_phone')
    description = data.get('description')
    
    company, message = CompanyService.register_company(
        user_id, company_name, website, hr_contact, hr_phone, description
    )
    
    if not company:
        return jsonify({'error': message}), 400
    
    return jsonify({
        'message': message,
        'company_id': company.id
    }), 201

@company_bp.route('/profile', methods=['GET'])
@token_required
@company_required
def get_profile(user_id, role):
    company = Company.query.filter_by(user_id=user_id).first()
    if not company:
        return jsonify({'error': 'Company profile not found'}), 404
    
    return jsonify({
        'id': company.id,
        'company_name': company.company_name,
        'website': company.website,
        'hr_contact': company.hr_contact,
        'hr_phone': company.hr_phone,
        'description': company.description,
        'approval_status': company.approval_status,
        'is_active': company.is_active
    }), 200

@company_bp.route('/profile', methods=['PUT'])
@token_required
@company_required
def update_profile(user_id, role):
    data = request.get_json()
    company = Company.query.filter_by(user_id=user_id).first()
    
    if not company:
        return jsonify({'error': 'Company profile not found'}), 404
    
    company.website = data.get('website', company.website)
    company.hr_contact = data.get('hr_contact', company.hr_contact)
    company.hr_phone = data.get('hr_phone', company.hr_phone)
    company.description = data.get('description', company.description)
    
    db.session.commit()
    return jsonify({'message': 'Profile updated'}), 200

@company_bp.route('/drives', methods=['POST'])
@token_required
@company_required
def create_drive(user_id, role):
    company = Company.query.filter_by(user_id=user_id).first()
    if not company:
        return jsonify({'error': 'Company profile not found'}), 404
    
    if company.approval_status != 'approved':
        return jsonify({'error': 'Company must be approved to create drives'}), 403
    
    data = request.get_json()
    job_title = data.get('job_title')
    job_description = data.get('job_description')
    min_cgpa = float(data.get('min_cgpa', 0.0))
    application_deadline = datetime.fromisoformat(data.get('application_deadline'))
    eligible_branches = data.get('eligible_branches')
    eligible_batches = data.get('eligible_batches')
    salary_package = data.get('salary_package')
    interview_date = data.get('interview_date')
    
    if interview_date:
        interview_date = datetime.fromisoformat(interview_date)
    
    drive = PlacementDriveService.create_drive(
        company.id, job_title, job_description, min_cgpa,
        application_deadline, eligible_branches, eligible_batches,
        salary_package, interview_date
    )
    
    return jsonify({
        'message': 'Drive created',
        'drive_id': drive.id,
        'status': drive.status
    }), 201

@company_bp.route('/drives', methods=['GET'])
@token_required
@company_required
def get_drives(user_id, role):
    company = Company.query.filter_by(user_id=user_id).first()
    if not company:
        return jsonify({'error': 'Company profile not found'}), 404
    
    drives = PlacementDriveService.get_all_drives(company_id=company.id)
    
    return jsonify({
        'drives': [{
            'id': d.id,
            'job_title': d.job_title,
            'job_description': d.job_description,
            'min_cgpa': d.min_cgpa,
            'status': d.status,
            'application_deadline': d.application_deadline.isoformat(),
            'salary_package': d.salary_package,
            'interview_date': d.interview_date.isoformat() if d.interview_date else None,
            'applicants_count': len(d.applications)
        } for d in drives]
    }), 200

@company_bp.route('/applications/<int:drive_id>', methods=['GET'])
@token_required
@company_required
def get_drive_applications(user_id, role, drive_id):
    drive = PlacementDrive.query.get(drive_id)
    if not drive:
        return jsonify({'error': 'Drive not found'}), 404
    
    company = Company.query.filter_by(user_id=user_id).first()
    if not company or drive.company_id != company.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    applications = ApplicationService.get_drive_applications(drive_id)
    
    return jsonify({
        'applications': [{
            'id': a.id,
            'student_name': f"{a.student.first_name} {a.student.last_name}",
            'student_roll': a.student.roll_number,
            'student_cgpa': a.student.cgpa,
            'status': a.status,
            'applied_at': a.applied_at.isoformat()
        } for a in applications]
    }), 200

@company_bp.route('/applications/<int:application_id>/shortlist', methods=['PUT'])
@token_required
@company_required
def shortlist_applicant(user_id, role, application_id):
    application = ApplicationService.get_application(application_id)
    if not application:
        return jsonify({'error': 'Application not found'}), 404
    
    drive = application.placement_drive
    company = Company.query.filter_by(user_id=user_id).first()
    if not company or drive.company_id != company.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    ApplicationService.update_application_status(application_id, 'shortlisted')
    return jsonify({'message': 'Applicant shortlisted'}), 200

@company_bp.route('/applications/<int:application_id>/select', methods=['PUT'])
@token_required
@company_required
def select_applicant(user_id, role, application_id):
    application = ApplicationService.get_application(application_id)
    if not application:
        return jsonify({'error': 'Application not found'}), 404
    
    drive = application.placement_drive
    company = Company.query.filter_by(user_id=user_id).first()
    if not company or drive.company_id != company.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    ApplicationService.update_application_status(application_id, 'selected')
    return jsonify({'message': 'Applicant selected'}), 200

@company_bp.route('/applications/<int:application_id>/reject', methods=['PUT'])
@token_required
@company_required
def reject_applicant(user_id, role, application_id):
    application = ApplicationService.get_application(application_id)
    if not application:
        return jsonify({'error': 'Application not found'}), 404
    
    drive = application.placement_drive
    company = Company.query.filter_by(user_id=user_id).first()
    if not company or drive.company_id != company.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    ApplicationService.update_application_status(application_id, 'rejected')
    return jsonify({'message': 'Applicant rejected'}), 200

@company_bp.route('/dashboard', methods=['GET'])
@token_required
@company_required
def dashboard(user_id, role):
    company = Company.query.filter_by(user_id=user_id).first()
    if not company:
        return jsonify({'error': 'Company profile not found'}), 404
    
    drives = PlacementDriveService.get_all_drives(company_id=company.id)
    total_applications = 0
    total_shortlisted = 0
    total_selected = 0
    
    for drive in drives:
        total_applications += len(drive.applications)
        total_shortlisted += len([a for a in drive.applications if a.status == 'shortlisted'])
        total_selected += len([a for a in drive.applications if a.status == 'selected'])
    
    return jsonify({
        'total_drives': len(drives),
        'total_applications': total_applications,
        'total_shortlisted': total_shortlisted,
        'total_selected': total_selected
    }), 200
