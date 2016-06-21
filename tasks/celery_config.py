from datetime import timedelta

BROKER_URL = 'amqp://guest:guest@localhost:5672//'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TIMEZONE = 'Europe/Oslo'
CELERY_ENABLE_UTC = True


CELERYBEAT_SCHEDULE = {
    'hourly': {
        'task': 'aggregate.hourly',
        'schedule': timedelta(seconds=20),
        'options': {'queue': 'hour'}
    },
    'daily': {
        'task': 'aggregate.daily',
        'schedule': timedelta(seconds=480),
        'options': {'queue': 'day'}
    },
    'weekly': {
        'task': 'aggregate.weekly',
        'schedule': timedelta(seconds=3360),
        'options': {'queue': 'week'}
    },
}
