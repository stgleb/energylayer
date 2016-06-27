screen -S hour celery -A aggregate worker -B -l info -Q hour -n worker1
screen -S day celery -A aggregate worker -B -l info -Q day -n worker2
screen -S hour celery -A aggregate worker -B -l info -Q hour -n worker1
