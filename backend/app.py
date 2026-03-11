from flask import Flask
from flask_cors import CORS
from config import config
from models import db, User
from utils.cache import init_redis
from tasks.celery_tasks import init_celery
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.company import company_bp
from routes.student import student_bp
import os
from datetime import datetime

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    CORS(app, resources={
        r"/*": {
            "origins": ["http://localhost:8080", "http://localhost:5173", "http://127.0.0.1:8080"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True,
            "max_age": 3600
        }
    })
    
    db.init_app(app)
    init_redis(app)
    init_celery(app)
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(company_bp)
    app.register_blueprint(student_bp)
    
    @app.before_request
    def create_tables():
        db.create_all()
    
    @app.cli.command()
    def init_db():
        db.create_all()
        
        admin_user = User.query.filter_by(role='admin').first()
        if not admin_user:
            from utils.auth import hash_password
            admin = User(
                email='admin@placementportal.com',
                password=hash_password('admin123'),
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()
            print('Admin user created: admin@placementportal.com')
        
        print('Database initialized')
    
    @app.route('/health', methods=['GET'])
    def health():
        return {'status': 'healthy'}, 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
