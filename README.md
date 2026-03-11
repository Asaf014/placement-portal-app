# Placement Portal Application

A comprehensive web-based placement management system built with Flask, VueJS, SQLite, Redis, and Celery. This application enables Institutes, Companies, and Students to collaborate efficiently in the campus recruitment process.

## Technology Stack

**Backend:**
- Flask 2.3.3
- Flask-SQLAlchemy for ORM
- Flask-JWT-Extended for authentication
- Flask-CORS for cross-origin requests
- SQLite for database
- Redis for caching
- Celery for background jobs

**Frontend:**
- VueJS 3
- Vue Router 4
- Axios for HTTP requests
- Bootstrap 5 for styling

**Additional Tools:**
- Celery Beat for scheduled jobs
- PyPDF2 for PDF generation
- ReportLab for advanced PDF creation

## Project Structure

```
MAD2/
├── backend/
│   ├── models/
│   │   └── __init__.py           (Database models)
│   ├── routes/
│   │   ├── auth.py                (Authentication routes)
│   │   ├── admin.py               (Admin routes)
│   │   ├── company.py             (Company routes)
│   │   └── student.py             (Student routes)
│   ├── services/
│   │   └── user_service.py        (Business logic)
│   ├── tasks/
│   │   └── celery_tasks.py        (Background jobs)
│   ├── utils/
│   │   ├── auth.py                (Authentication utilities)
│   │   ├── cache.py               (Redis caching)
│   │   └── email.py               (Email notifications)
│   ├── app.py                     (Flask application)
│   ├── config.py                  (Configuration)
│   └── requirements.txt           (Python dependencies)
├── frontend/
│   ├── src/
│   │   ├── components/            (Reusable components)
│   │   ├── views/
│   │   │   ├── auth/              (Login, Register)
│   │   │   ├── admin/             (Admin pages)
│   │   │   ├── company/           (Company pages)
│   │   │   ├── student/           (Student pages)
│   │   │   └── Home.vue
│   │   ├── router/
│   │   │   └── index.js           (Route configuration)
│   │   ├── services/
│   │   │   └── api.js             (API client)
│   │   ├── App.vue
│   │   └── main.js
│   ├── public/
│   │   └── index.html
│   ├── package.json
│   └── vue.config.js
├── setup.bat                      (Windows setup script)
├── setup.ps1                      (PowerShell setup script)
└── README.md                      (This file)
```

## Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- Redis server
- Git

## Installation and Setup

### Quick Setup (Windows)

#### Using Batch Script:
```bash
setup.bat
```

#### Using PowerShell Script:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\setup.ps1
```

### Manual Setup

#### Backend Setup:
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate  (on Windows)
source venv/bin/activate (on macOS/Linux)
pip install -r requirements.txt
python app.py
```

#### Frontend Setup:
```bash
cd frontend
npm install
npm run dev
```

#### Initialize Database:
```bash
cd backend
.\venv\Scripts\activate
python -c "from app import create_app; app = create_app(); app.app_context().push(); from models import db; db.create_all()"
```

## Running the Application

### 1. Start Redis Server
```bash
redis-server
```

### 2. Start Backend Server
```bash
cd backend
.\venv\Scripts\activate
python app.py
```

### 3. Start Celery Worker
```bash
cd backend
.\venv\Scripts\activate
celery -A tasks.celery_tasks worker --loglevel=info
```

### 4. Start Frontend Development Server
```bash
cd frontend
npm run dev
```

### 5. Access the Application

- Frontend: http://localhost:8080
- Backend API: http://localhost:5000

## Default Admin Credentials

- Email: admin@placementportal.com
- Password: admin123

## API Endpoints

### Authentication
- POST /auth/register - Register new user
- POST /auth/login - Login user
- GET /auth/verify-token - Verify JWT token

### Admin Routes
- GET /admin/dashboard - Admin dashboard statistics
- GET /admin/companies/pending - Pending company approvals
- PUT /admin/companies/<id>/approve - Approve company
- PUT /admin/companies/<id>/reject - Reject company
- GET /admin/drives/pending - Pending drive approvals
- PUT /admin/drives/<id>/approve - Approve drive
- PUT /admin/drives/<id>/reject - Reject drive
- GET /admin/students - List all students
- GET /admin/companies - List all companies
- GET /admin/applications - List all applications
- GET /admin/statistics - Placement statistics

### Company Routes
- POST /company/register - Register company profile
- GET /company/profile - Get company profile
- PUT /company/profile - Update company profile
- POST /company/drives - Create placement drive
- GET /company/drives - List company drives
- GET /company/applications/<drive_id> - Get drive applications
- PUT /company/applications/<app_id>/shortlist - Shortlist applicant
- PUT /company/applications/<app_id>/select - Select applicant
- PUT /company/applications/<app_id>/reject - Reject applicant
- GET /company/dashboard - Company dashboard

### Student Routes
- POST /student/register - Register student profile
- GET /student/profile - Get student profile
- PUT /student/profile - Update student profile
- GET /student/available-drives - Get eligible drives
- GET /student/applications - Get my applications
- POST /student/apply/<drive_id> - Apply to drive
- POST /student/export-applications - Export application history
- GET /student/placement-history - Get placement history
- GET /student/search-drives - Search placement drives
- GET /student/dashboard - Student dashboard

## Database Schema

### User Table
- id (Primary Key)
- email (Unique)
- password
- role (admin/company/student)
- is_active
- is_blacklisted
- created_at
- updated_at

### Company Table
- id (Primary Key)
- user_id (Foreign Key)
- company_name (Unique)
- website
- hr_contact
- hr_phone
- description
- approval_status (pending/approved/rejected)
- is_active
- created_at
- updated_at

### Student Table
- id (Primary Key)
- user_id (Foreign Key)
- first_name
- last_name
- roll_number (Unique)
- branch
- batch
- cgpa
- phone
- resume_url
- is_active
- created_at
- updated_at

### PlacementDrive Table
- id (Primary Key)
- company_id (Foreign Key)
- job_title
- job_description
- min_cgpa
- max_applicants
- eligible_branches
- eligible_batches
- application_deadline
- status
- salary_package
- interview_date
- created_at
- updated_at

### Application Table
- id (Primary Key)
- student_id (Foreign Key)
- drive_id (Foreign Key)
- status (applied/shortlisted/selected/rejected)
- applied_at
- shortlisted_at
- selected_at
- rejected_at
- updated_at

### ActivityLog Table
- id (Primary Key)
- user_id
- action
- entity_type
- entity_id
- timestamp

### Notification Table
- id (Primary Key)
- user_id (Foreign Key)
- title
- message
- is_read
- created_at

## Features Implemented

### Core Features
- User authentication with JWT tokens
- Role-based access control (Admin, Company, Student)
- Company registration and approval workflow
- Placement drive creation and approval
- Student application management
- Eligibility validation
- Duplicate application prevention
- Application status tracking

### Admin Features
- Dashboard with statistics
- Company approval/rejection management
- Placement drive approval/rejection
- Student and company search functionality
- User blacklisting capability
- Activity monitoring

### Company Features
- Company profile management
- Placement drive creation (after approval)
- Application management
- Student shortlisting and selection
- Interview scheduling

### Student Features
- Student profile management
- Resume upload
- Browse eligible placement drives
- Apply for placements
- Track application status
- View placement history
- Export application history as CSV

### Background Jobs
- Daily application deadline reminders
- Monthly activity reports for admin
- Interview reminders
- Async CSV export

### Performance Features
- Redis caching for frequently accessed data
- Cache invalidation strategies
- Optimized API responses

## Authentication

The application uses JWT (JSON Web Tokens) for stateless authentication. All protected routes require a valid JWT token in the Authorization header:

```
Authorization: Bearer <token>
```

## Caching Strategy

- User profiles cached for 3600 seconds
- Company information cached for 3600 seconds
- Student data cached for 3600 seconds
- Placement drives cached for 3600 seconds
- Cache invalidation on data updates

## Email Configuration

To enable email notifications, set the following environment variables:

```
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_USE_TLS=True
```

## Troubleshooting

### Redis Connection Error
- Ensure Redis server is running: `redis-server`
- Check Redis is accessible on localhost:6379

### Database Lock Issues
- Delete the placement_portal.db file and restart the backend

### CORS Errors
- Ensure frontend is on http://localhost:8080 and backend on http://localhost:5000

### Module Not Found
- Ensure all dependencies are installed: `pip install -r requirements.txt`

### Port Already in Use
- Backend: Change PORT in app.py and vue.config.js
- Frontend: Use `npm run dev -- --port 8081`

## Development Notes

- The application follows a modular architecture for easy maintenance
- All code is organized by functionality (routes, services, models)
- Database models use SQLAlchemy ORM for type safety
- Frontend components are reusable and independent
- Background tasks are managed through Celery

## Future Enhancements

- PDF report generation for interviews
- Resume parsing and skill extraction
- Email verification
- Two-factor authentication
- Advanced analytics and dashboards
- Mobile responsive improvements
- Notification system with real-time updates
- Interview scheduling calendar view

## License

This project is created for educational purposes.

## Support

For issues or questions, please ensure:
1. Redis is running
2. All dependencies are installed
3. Database is properly initialized
4. Ports 5000 and 8080 are available
