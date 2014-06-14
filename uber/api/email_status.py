from flask import abort
from flask.ext.restful import Resource

from uber.email import constants
from uber.email import models


class EmailStatus(Resource):
    def get(self, task_id):
        email_status = models.EmailStatus.objects.get_or_404(task_id=task_id)
        if email_status:
            return {
                'task_id': task_id,
                'status': constants.EMAIL_STATUS_LOOKUP[email_status.status]
            }

        abort(404)
