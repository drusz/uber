from flask import Flask


def create_app(package_name, settings_override=None):
    from uber import db

    app = Flask(package_name)

    app.config.from_object('settings')
    app.config.update(settings_override or {})

    db.init_app(app)

    return app
