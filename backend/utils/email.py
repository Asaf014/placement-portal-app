import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app
import requests

def send_email(to_email, subject, body, is_html=False):
    try:
        msg = MIMEMultipart()
        msg['From'] = current_app.config.get('MAIL_DEFAULT_SENDER', 'noreply@placementportal.com')
        msg['To'] = to_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'html' if is_html else 'plain'))
        
        server = smtplib.SMTP(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT'])
        server.starttls()
        server.login(current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Email send error: {str(e)}")
        return False

def send_google_chat_notification(message):
    webhook_url = current_app.config.get('GOOGLE_CHAT_WEBHOOK', '')
    if not webhook_url:
        return False
    
    try:
        payload = {
            'text': message
        }
        response = requests.post(webhook_url, json=payload, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"Google Chat notification error: {str(e)}")
        return False

def send_sms(phone_number, message):
    return True

def send_notification(user_id, title, message):
    from models import Notification, db
    notification = Notification(user_id=user_id, title=title, message=message)
    db.session.add(notification)
    db.session.commit()
    return notification
