import datetime

from uber import db
from uber.email import constants


class EmailServiceResult(db.Document):
    timestamp = db.DateTimeField(default=datetime.datetime.now, required=True)
    service_name = db.StringField(max_length=40, required=True)
    from_email = db.StringField(max_length=255, required=True)
    to_email = db.StringField(max_length=255, required=True)
    subject = db.StringField(max_length=255, required=True)
    body = db.StringField(max_length=512, required=True)
    success = db.BooleanField(required=True)

    @property
    def full_service_name(self):
        from uber import email
        service = email.get_service(self.service_name)
        return service.full_name if service else 'unknown'

    @property
    def friendly_date(self):
        return self.timestamp.strftime('%B %d %Y %I:%M%p')


class EmailStatus(db.Document):
    timestamp = db.DateTimeField(default=datetime.datetime.now, required=True)
    task_id = db.StringField(required=True)
    status = db.IntField(default=constants.EMAIL_STATUS['pending'])
