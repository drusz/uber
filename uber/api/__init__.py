from flask.ext.restful import Api

from uber import factory


api = Api(prefix='/1')

def create_app(settings_override=None):
    app = factory.create_app(__name__, settings_override=settings_override)
    api.init_app(app)

    return app


from uber.api import emailer
api.add_resource(emailer.EmailerService, '/email')
