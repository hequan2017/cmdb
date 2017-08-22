import time
from celery import task, platforms

platforms.C_FORCE_ROOT = True

@task
def add(x, y):
    return x + y


@task
def sendmail(mail):
    print('sending mail to %s...' % mail['to'])
    time.sleep(2.0)
    print('mail sent.')
    return mail['to']