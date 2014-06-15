from flask.ext.restful import reqparse, Resource

import helpers
from uber.email.models import EmailStatus
from uber.email.tasks import send_email


class EmailerService(Resource):
    def __init__(self):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument('from_email', dest='from_email', type=helpers.email_type,
                                      required=True)
        self.post_parser.add_argument('to_email', dest='to_email', type=helpers.email_type,
                                      required=True)
        self.post_parser.add_argument('subject', dest='subject',
                                      type=helpers.string_type('subject', max_length=255),
                                      required=True)
        self.post_parser.add_argument('body', dest='body',
                                      type=helpers.string_type('body', max_length=500),
                                      required=True)

    def post(self):
        args = self.post_parser.parse_args()
        task = send_email.delay(args.from_email, args.to_email, args.subject, args.body)

        email_status = EmailStatus(task_id=task.id)
        email_status.save()

        if task:
            return {
                'err': 0,
                'task_id': task.id,
                'message': 'The email has been queued!'
            }

        return {
            'err': 1,
            'message': 'There was a problem sending your email! Please try again later.'
        }, 422
