from apscheduler.schedulers.background import BackgroundScheduler
from random import randint

from app.schedulers.emailer import *


def scheduled_jobs():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_email, "interval", minutes=1)
    # scheduler.add_job(send_email, "cron", hour=1, minute=0)

    scheduler.start()


scheduled_jobs()
