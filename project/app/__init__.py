import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from celery import Celery

# import config
from . import custom_filters

app = Flask(__name__)
app.config.from_object(os.environ.get('FLASK_ENV') or 'config.DevelopementConfig')

custom_filters.generate_custom_filter(app)

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend='redis://redis:6379/0',
        broker='amqp://myuser:mypass@rabbitmq:5672/myvhost',
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

celery = make_celery(app)

db = SQLAlchemy(app)
migrate = Migrate(app,  db)


from . import views
