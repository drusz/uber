from flask import Flask
from celery import Celery


def create_app(package_name, settings_override=None):
    from uber import db

    app = Flask(package_name)

    app.config.from_object('settings')
    app.config.update(settings_override or {})

    db.init_app(app)

    return app


def make_celery(task_modules):
    app = create_app('uber_tasks')

    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'],
                    include=task_modules)
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery
