from celery.schedules import crontab

beat_schedule = {
    'send-daily-reminders': {
        'task': 'tasks.celery_tasks.send_daily_reminders',
        'schedule': crontab(hour=9, minute=0),
    },
    'send-interview-reminders': {
        'task': 'tasks.celery_tasks.send_interview_reminders',
        'schedule': crontab(hour=8, minute=0),
    },
    'generate-monthly-report': {
        'task': 'tasks.celery_tasks.generate_monthly_report',
        'schedule': crontab(day_of_month=1, hour=0, minute=0),
    },
}

timezone = 'UTC'
enable_utc = True
