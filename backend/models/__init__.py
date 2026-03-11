from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from enum import Enum

db = SQLAlchemy()

class UserRole(Enum):
    ADMIN = 'admin'
    COMPANY = 'company'
    STUDENT = 'student'

class ApprovalStatus(Enum):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'

class ApplicationStatus(Enum):
    APPLIED = 'applied'
    SHORTLISTED = 'shortlisted'
    SELECTED = 'selected'
    REJECTED = 'rejected'

class DriveStatus(Enum):
    PENDING = 'pending'
    APPROVED = 'approved'
    CLOSED = 'closed'

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_blacklisted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    company = db.relationship('Company', backref='user', uselist=False, cascade='all, delete-orphan')
    student = db.relationship('Student', backref='user', uselist=False, cascade='all, delete-orphan')

class Company(db.Model):
    __tablename__ = 'companies'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    company_name = db.Column(db.String(255), nullable=False, unique=True)
    website = db.Column(db.String(255))
    hr_contact = db.Column(db.String(120), nullable=False)
    hr_phone = db.Column(db.String(20))
    description = db.Column(db.Text)
    industry = db.Column(db.String(100))
    approval_status = db.Column(db.String(20), default='pending')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    placement_drives = db.relationship('PlacementDrive', backref='company', cascade='all, delete-orphan')

class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    roll_number = db.Column(db.String(50), unique=True)
    branch = db.Column(db.String(100))
    batch = db.Column(db.Integer)
    cgpa = db.Column(db.Float, default=0.0)
    phone = db.Column(db.String(20))
    resume_url = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    applications = db.relationship('Application', backref='student', cascade='all, delete-orphan')

class PlacementDrive(db.Model):
    __tablename__ = 'placement_drives'
    
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    job_title = db.Column(db.String(255), nullable=False)
    job_description = db.Column(db.Text, nullable=False)
    min_cgpa = db.Column(db.Float, default=0.0)
    max_applicants = db.Column(db.Integer)
    eligible_branches = db.Column(db.String(255))
    eligible_batches = db.Column(db.String(255))
    application_deadline = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='pending')
    salary_package = db.Column(db.Float)
    interview_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    applications = db.relationship('Application', backref='placement_drive', cascade='all, delete-orphan')

class Application(db.Model):
    __tablename__ = 'applications'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey('placement_drives.id'), nullable=False)
    status = db.Column(db.String(20), default='applied')
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    shortlisted_at = db.Column(db.DateTime)
    selected_at = db.Column(db.DateTime)
    rejected_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('student_id', 'drive_id', name='unique_student_drive'),)

class ActivityLog(db.Model):
    __tablename__ = 'activity_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action = db.Column(db.String(255), nullable=False)
    entity_type = db.Column(db.String(100))
    entity_id = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
