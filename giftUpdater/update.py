from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .giftUpdate import update_picked


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_picked, 'interval', hours=48)
    scheduler.start()