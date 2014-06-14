from uber.email import constants
from uber.email.models import EmailStatus
from uber.queue import celery


@celery.task()
def send_email(from_email, to_email, subject, body):
    from uber import email
    success = email.send(from_email, to_email, subject, body)

    task_id = send_email.request.id
    email_status = EmailStatus.objects.get(task_id=task_id)

    if success:
        email_status.status = constants.EMAIL_STATUS['success']
    else:
        email_status.status = constants.EMAIL_STATUS['failure']

    email_status.save()
