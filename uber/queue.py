import factory


celery = factory.make_celery([
    'uber.email.tasks'
])

