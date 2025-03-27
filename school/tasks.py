from celery import shared_task
import time

@shared_task
def sleep_task(seconds):
    time.sleep(seconds)
    return f"Slept for {seconds} seconds."
