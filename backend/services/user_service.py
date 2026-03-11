from models import db, User, Company, Student, PlacementDrive, Application, ActivityLog
from utils.auth import hash_password, verify_password
from utils.cache import cache_set, cache_get, cache_delete
from datetime import datetime

class UserService:
    @staticmethod
    def create_user(email, password, role):
        if User.query.filter_by(email=email).first():
            return None, 'Email already exists'
        
        user = User(email=email, password=hash_password(password), role=role)
        db.session.add(user)
        db.session.commit()
        return user, 'User created successfully'
    
    @staticmethod
    def get_user(user_id):
        user = User.query.get(user_id)
        return user
    
    @staticmethod
    def authenticate(email, password):
        user = User.query.filter_by(email=email).first()
        if user and verify_password(user.password, password):
            return user
        return None
    
    @staticmethod
    def get_all_users(role=None):
        query = User.query
        if role:
            query = query.filter_by(role=role)
        return query.all()
    
    @staticmethod
    def blacklist_user(user_id):
        user = User.query.get(user_id)
        if user:
            user.is_blacklisted = True
            db.session.commit()
            cache_delete(f"user:{user_id}")
            return True
        return False
    
    @staticmethod
    def activate_user(user_id):
        user = User.query.get(user_id)
        if user:
            user.is_blacklisted = False
            db.session.commit()
            cache_delete(f"user:{user_id}")
            return True
        return False

    @staticmethod
    def register_student(user_id, first_name, last_name, roll_number, phone=None, branch=None, cgpa=None, resume_url=None):
        if Student.query.filter_by(roll_number=roll_number).first():
            return None, 'Roll number already exists'
        
        student = Student(
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            roll_number=roll_number,
            phone=phone,
            branch=branch,
            cgpa=cgpa if cgpa else 0.0,
            resume_url=resume_url
        )
        db.session.add(student)
        db.session.commit()
        return student, 'Student registered successfully'

    @staticmethod
    def register_company(user_id, company_name, website, hr_contact, hr_phone=None, description=None, industry=None):
        if Company.query.filter_by(company_name=company_name).first():
            return None, 'Company name already exists'
        
        company = Company(
            user_id=user_id,
            company_name=company_name,
            website=website,
            hr_contact=hr_contact,
            hr_phone=hr_phone,
            description=description,
            industry=industry,
            approval_status='pending'
        )
        db.session.add(company)
        db.session.commit()
        return company, 'Company registered successfully'

class CompanyService:
    @staticmethod
    def register_company(user_id, company_name, website, hr_contact, hr_phone=None, description=None):
        if Company.query.filter_by(company_name=company_name).first():
            return None, 'Company name already exists'
        
        company = Company(
            user_id=user_id,
            company_name=company_name,
            website=website,
            hr_contact=hr_contact,
            hr_phone=hr_phone,
            description=description,
            approval_status='pending'
        )
        db.session.add(company)
        db.session.commit()
        return company, 'Company registered successfully'
    
    @staticmethod
    def get_company(company_id):
        cache_key = f"company:{company_id}"
        company = cache_get(cache_key)
        if company:
            return company
        
        company = Company.query.get(company_id)
        if company:
            cache_set(cache_key, {
                'id': company.id,
                'company_name': company.company_name,
                'approval_status': company.approval_status
            })
        return company
    
    @staticmethod
    def get_all_companies(approval_status=None):
        query = Company.query
        if approval_status:
            query = query.filter_by(approval_status=approval_status)
        return query.all()
    
    @staticmethod
    def approve_company(company_id):
        company = Company.query.get(company_id)
        if company:
            company.approval_status = 'approved'
            db.session.commit()
            cache_delete(f"company:{company_id}")
            return True
        return False
    
    @staticmethod
    def reject_company(company_id):
        company = Company.query.get(company_id)
        if company:
            company.approval_status = 'rejected'
            db.session.commit()
            cache_delete(f"company:{company_id}")
            return True
        return False

class StudentService:
    @staticmethod
    def register_student(user_id, first_name, last_name, roll_number, branch=None, batch=None, cgpa=0.0):
        if Student.query.filter_by(roll_number=roll_number).first():
            return None, 'Roll number already exists'
        
        student = Student(
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            roll_number=roll_number,
            branch=branch,
            batch=batch,
            cgpa=cgpa
        )
        db.session.add(student)
        db.session.commit()
        return student, 'Student registered successfully'
    
    @staticmethod
    def get_student(student_id):
        cache_key = f"student:{student_id}"
        student = cache_get(cache_key)
        if student:
            return student
        
        student = Student.query.get(student_id)
        if student:
            cache_set(cache_key, {
                'id': student.id,
                'first_name': student.first_name,
                'last_name': student.last_name,
                'roll_number': student.roll_number
            })
        return student
    
    @staticmethod
    def get_all_students():
        return Student.query.all()
    
    @staticmethod
    def update_student(student_id, **kwargs):
        student = Student.query.get(student_id)
        if student:
            for key, value in kwargs.items():
                if hasattr(student, key):
                    setattr(student, key, value)
            db.session.commit()
            cache_delete(f"student:{student_id}")
            return student
        return None

class PlacementDriveService:
    @staticmethod
    def create_drive(company_id, job_title, job_description, min_cgpa, 
                    application_deadline, eligible_branches=None, eligible_batches=None,
                    salary_package=None, interview_date=None):
        drive = PlacementDrive(
            company_id=company_id,
            job_title=job_title,
            job_description=job_description,
            min_cgpa=min_cgpa,
            application_deadline=application_deadline,
            eligible_branches=eligible_branches,
            eligible_batches=eligible_batches,
            salary_package=salary_package,
            interview_date=interview_date,
            status='pending'
        )
        db.session.add(drive)
        db.session.commit()
        return drive
    
    @staticmethod
    def get_drive(drive_id):
        cache_key = f"drive:{drive_id}"
        drive = cache_get(cache_key)
        if drive:
            return drive
        
        drive = PlacementDrive.query.get(drive_id)
        if drive:
            cache_set(cache_key, {
                'id': drive.id,
                'job_title': drive.job_title,
                'status': drive.status
            })
        return drive
    
    @staticmethod
    def get_all_drives(status=None, company_id=None):
        query = PlacementDrive.query
        if status:
            query = query.filter_by(status=status)
        if company_id:
            query = query.filter_by(company_id=company_id)
        return query.all()
    
    @staticmethod
    def approve_drive(drive_id):
        drive = PlacementDrive.query.get(drive_id)
        if drive:
            drive.status = 'approved'
            db.session.commit()
            cache_delete(f"drive:{drive_id}")
            return True
        return False
    
    @staticmethod
    def reject_drive(drive_id):
        drive = PlacementDrive.query.get(drive_id)
        if drive:
            drive.status = 'rejected'
            db.session.commit()
            cache_delete(f"drive:{drive_id}")
            return True
        return False

class ApplicationService:
    @staticmethod
    def apply_to_drive(student_id, drive_id):
        existing = Application.query.filter_by(student_id=student_id, drive_id=drive_id).first()
        if existing:
            return None, 'Already applied to this drive'
        
        application = Application(student_id=student_id, drive_id=drive_id, status='applied')
        db.session.add(application)
        db.session.commit()
        return application, 'Applied successfully'
    
    @staticmethod
    def get_application(application_id):
        return Application.query.get(application_id)
    
    @staticmethod
    def get_student_applications(student_id):
        return Application.query.filter_by(student_id=student_id).all()
    
    @staticmethod
    def get_drive_applications(drive_id):
        return Application.query.filter_by(drive_id=drive_id).all()
    
    @staticmethod
    def update_application_status(application_id, status):
        application = Application.query.get(application_id)
        if application:
            application.status = status
            if status == 'shortlisted':
                application.shortlisted_at = datetime.utcnow()
            elif status == 'selected':
                application.selected_at = datetime.utcnow()
            elif status == 'rejected':
                application.rejected_at = datetime.utcnow()
            db.session.commit()
            return application
        return None
