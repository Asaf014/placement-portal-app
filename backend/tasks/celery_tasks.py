from celery import Celery
from flask import current_app
import csv
import io
from datetime import datetime, timedelta
from models import db, Student, PlacementDrive, Application, User, Company
from utils.email import send_email, send_notification

def make_celery(app):
    celery = Celery(app.import_name)
    celery.conf.update(app.config)
    
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    
    celery.Task = ContextTask
    return celery

celery = None

def init_celery(app):
    global celery
    celery = make_celery(app)
    return celery

def send_daily_reminders():
    try:
        drives = PlacementDrive.query.filter(
            PlacementDrive.application_deadline > datetime.utcnow(),
            PlacementDrive.status == 'approved'
        ).all()
        
        for drive in drives:
            days_left = (drive.application_deadline - datetime.utcnow()).days
            
            if days_left in [1, 3, 7]:
                students = Student.query.all()
                
                for student in students:
                    existing_app = Application.query.filter_by(
                        student_id=student.id,
                        drive_id=drive.id
                    ).first()
                    
                    if not existing_app:
                        user = User.query.get(student.user_id)
                        subject = f"Reminder: Application Deadline for {drive.job_title} in {days_left} days"
                        body = f"""
                        <p>Hi {student.first_name},</p>
                        <p>This is a reminder that the application deadline for <strong>{drive.job_title}</strong> 
                        at {drive.company.company_name} is in {days_left} days.</p>
                        <p>Apply now to not miss this opportunity!</p>
                        """
                        send_email(user.email, subject, body, is_html=True)
        
        return {'status': 'success', 'message': 'Daily reminders sent'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

def generate_monthly_report():
    try:
        admin = User.query.filter_by(role='admin').first()
        if not admin:
            return {'status': 'error', 'message': 'Admin not found'}
        
        current_month = datetime.utcnow().month
        current_year = datetime.utcnow().year
        
        drives_conducted = PlacementDrive.query.filter(
            db.extract('month', PlacementDrive.created_at) == current_month,
            db.extract('year', PlacementDrive.created_at) == current_year,
            PlacementDrive.status == 'approved'
        ).count()
        
        total_applicants = Application.query.filter(
            db.extract('month', Application.applied_at) == current_month,
            db.extract('year', Application.applied_at) == current_year
        ).count()
        
        total_selected = Application.query.filter(
            db.extract('month', Application.selected_at) == current_month,
            db.extract('year', Application.selected_at) == current_year,
            Application.status == 'selected'
        ).count()
        
        html_content = f"""
        <html>
        <head><title>Monthly Placement Report</title></head>
        <body>
            <h1>Monthly Placement Activity Report</h1>
            <p>Report for {current_month}/{current_year}</p>
            <table border="1" cellpadding="10">
                <tr><td>Drives Conducted</td><td>{drives_conducted}</td></tr>
                <tr><td>Total Applicants</td><td>{total_applicants}</td></tr>
                <tr><td>Students Selected</td><td>{total_selected}</td></tr>
            </table>
        </body>
        </html>
        """
        
        send_email(admin.email, 'Monthly Placement Report', html_content, is_html=True)
        return {'status': 'success', 'message': 'Monthly report generated and sent'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

def export_student_applications_csv(student_id):
    try:
        student = Student.query.get(student_id)
        if not student:
            return {'status': 'error', 'message': 'Student not found'}
        
        applications = Application.query.filter_by(student_id=student_id).all()
        
        csv_buffer = io.StringIO()
        writer = csv.writer(csv_buffer)
        writer.writerow(['Student ID', 'Company Name', 'Drive Title', 'Application Status', 'Applied Date', 'Status Updated'])
        
        for app in applications:
            writer.writerow([
                student.roll_number,
                app.placement_drive.company.company_name,
                app.placement_drive.job_title,
                app.status,
                app.applied_at.strftime('%Y-%m-%d %H:%M:%S'),
                app.updated_at.strftime('%Y-%m-%d %H:%M:%S')
            ])
        
        user = User.query.get(student.user_id)
        subject = 'Your Application Export'
        body = '<p>Please find your application history attached below:</p>'
        send_email(user.email, subject, body + f'<pre>{csv_buffer.getvalue()}</pre>', is_html=True)
        
        send_notification(student.user_id, 'Export Completed', 'Your application history has been exported and sent to your email.')
        
        return {'status': 'success', 'message': 'Export completed'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

def send_interview_reminders():
    try:
        selected_apps = Application.query.filter_by(status='selected').all()
        
        for app in selected_apps:
            drive = app.placement_drive
            if drive.interview_date and drive.interview_date > datetime.utcnow():
                student = Student.query.get(app.student_id)
                user = User.query.get(student.user_id)
                
                subject = f"Interview Reminder: {drive.job_title} at {drive.company.company_name}"
                body = f"""
                <p>Hi {student.first_name},</p>
                <p>Interview is scheduled for <strong>{drive.interview_date.strftime('%Y-%m-%d %H:%M')}</strong></p>
                <p>Company: {drive.company.company_name}</p>
                <p>Position: {drive.job_title}</p>
                """
                send_email(user.email, subject, body, is_html=True)
        
        return {'status': 'success', 'message': 'Interview reminders sent'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}
