from datetime import timedelta

from celery.schedules import crontab

BROKER_URL = 'amqp://guest:guest@localhost:5672//'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TIMEZONE = 'Europe/Oslo'
CELERY_ENABLE_UTC = True


CELERYBEAT_SCHEDULE = {
    'hourly': {
        'task': 'aggregate.first_task',
        'schedule': timedelta(hours=1),
        'options': {'queue': 'hour'}
    },
    'daily': {
        'task': 'aggregate.second_task',
        'schedule': timedelta(days=1),
        'options': {'queue': 'day'}
    },
    'weekly': {
        'task': 'aggregate.third_task',
        'schedule': crontab(day_of_week=1),
        'options': {'queue': 'week'}
    },
}
