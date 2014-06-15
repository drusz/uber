from flask import abort
from flask.ext.restful import Resource

from uber.email import models


class EmailStatus(Resource):
    def get(self, task_id):
        email_status = models.EmailStatus.objects.get_or_404(task_id=task_id)
        if email_status:
            return {
                'err': 0,
                'task_id': task_id,
                'status': email_status.friendly_status
            }

        abort(404)
