from tasks.celery_app import app


@app.task(queue="hour")
def hourly():
    """
    Run command: celery -A tasks worker -B -l info -Q hour -n worker1
    :return:
    """
    print("Hello, i am second task")


@app.task(queue="day")
def daily():
    """
    Run command: celery -A tasks worker -B -l info -Q day -n worker2
    :return:
    """
    print("Hello, i am second")


@app.task(queue="week")
def weekly():
    """
    Run command: celery -A tasks worker -B -l info -Q week -n worker2
    :return:
    """
    print("Hello, i am third")