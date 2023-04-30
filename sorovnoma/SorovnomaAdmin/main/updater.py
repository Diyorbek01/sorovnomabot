from urllib import request

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from main.views import CronJob


def start():
    schedular = BackgroundScheduler()
    cron = CronJob()
    trigger = CronTrigger(
        year="*", month="*", day="*", hour="0", minute="1", second="0"
    )
    schedular.add_job(cron.get, "interval", hours=23,  kwargs={'request': request})

    schedular.start()
