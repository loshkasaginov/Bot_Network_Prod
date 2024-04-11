from celery import Celery
from celery.schedules import crontab



app = Celery('celery_app', broker='redis://127.0.0.1:6379')


# Конфигурация приложения
# app.conf.update(   celery -A celery_app:app worker --loglevel=INFO 
#     broker_url='redis://127.0.0.1:6379',  # Адрес Redis
#     result_backend='redis://127.0.0.1:6379',  # Backend для результатов
#     task_serializer='json',
#     accept_content=['json'],  # Принимаемый формат контента
#     result_serializer='json',
#     timezone='Europe/Moscow',  # Временная зона
#     enable_utc=True,  # Использование UTC времени
# )

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

    # Calls test('hello') every 30 seconds.
    # It uses the same signature of previous task, an explicit name is
    # defined to avoid this task replacing the previous one defined.
    sender.add_periodic_task(30.0, test.s('hello'), name='add every 30')

    # Calls test('world') every 30 seconds
    sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        test.s('Happy Mondays!'),
    )

@app.task
def test(arg):
    print(arg)