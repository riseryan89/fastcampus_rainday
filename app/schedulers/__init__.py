from apscheduler.schedulers.background import BackgroundScheduler

from app.schedulers.emailer import *
from app.schedulers.weather_data_collector import *


def scheduled_jobs():
    scheduler = BackgroundScheduler()

    scheduler.add_job(send_email, "cron", hour=1, minute=0)
    scheduler.add_job(scheduled_collection, "cron", hour=0, minute=0)

    # scheduler.add_job(scheduled_collection, "interval", seconds=30)
    # scheduler.add_job(send_email, "interval", minutes=1)

    scheduler.start()
