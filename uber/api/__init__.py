from flask.ext.restful import Api

from uber import factory


api_v1 = Api(prefix='/1')


def create_app(settings_override=None):
    app = factory.create_app(__name__, settings_override=settings_override)
    api_v1.init_app(app)

    return app


from uber.api import email_status, emailer
api_v1.add_resource(email_status.EmailStatus, '/email_status/<task_id>')
api_v1.add_resource(emailer.EmailerService, '/email')
