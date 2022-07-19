from celery import shared_task
from celery.utils.log import get_task_logger

from note_app.celery import app
from user.emails import Email

logger = get_task_logger(__name__)


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


@shared_task
def send_email(token, email):
    try:
        Email.send_email(token=token, email_id=email)
        return "task complete"
    except Exception as e:
        print("task fail")
        logger.error(e)
