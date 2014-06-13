from flask.ext.restful import reqparse, Resource

import helpers
from uber import email


class EmailerService(Resource):
    def __init__(self):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument('from_email', dest='from_email',
                                      type=helpers.email_type, location='json',
                                      required=True)
        self.post_parser.add_argument('to_email', dest='to_email',
                                      type=helpers.email_type, location='json',
                                      required=True)
        self.post_parser.add_argument('subject', dest='subject',
                                      type=helpers.min_length_string('subject'), location='json',
                                      required=True)
        self.post_parser.add_argument('body', dest='body',
                                      type=helpers.min_length_string('body'), location='json',
                                      required=True)

    def post(self):
        args = self.post_parser.parse_args()
        success = email.send(args.from_email, args.to_email, args.subject, args.body)

        if success:
            return {
                'err': 0
            }

        return {
            'err': 1,
            'message': 'There was a problem sending your email! Please try again later.'
        }
