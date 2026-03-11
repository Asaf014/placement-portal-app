from app import create_app
from models import db, User
from utils.auth import hash_password
import os

def init_database():
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    
    with app.app_context():
        db.create_all()
        print('Database tables created successfully')
        
        existing_admin = User.query.filter_by(email='admin@admin').first()
        if not existing_admin:
            admin = User(
                email='admin@admin',
                password=hash_password('admin'),
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()
            print('Admin user created successfully')
            print('Admin Email: admin@admin')
            print('Admin Password: admin')
        else:
            print('Admin user already exists')

if __name__ == '__main__':
    init_database()
