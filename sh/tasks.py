import time
from celery import Celery, platforms

platforms.C_FORCE_ROOT = True

app= Celery(broker='redis://0.0.0.0',
            backend='redis://0.0.0.0',)



@app.task
def add(x, y):
    print(x,y)
    return x + y


@app.task
def sendmail(mail):
    print('sending mail to %s...' % mail['to'])
    time.sleep(2.0)
    print('mail sent.')
    return mail['to']


