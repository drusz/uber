from uber import factory


def create_app(settings_override=None):
    from uber.frontend.emailer import app as emailer_app

    app = factory.create_app(__name__, settings_override=settings_override)

    app.register_blueprint(emailer_app)

    return app


import emailer.views
