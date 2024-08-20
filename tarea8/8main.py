from flask import Flask
from flask_mail import Mail, Message
from celery import Celery
import os

app = Flask(__name__)

# Configuraciones de Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('EMAIL_USER')
mail = Mail(app)

# Configuración de Celery con Redis
def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
celery = make_celery(app)

@celery.task
def send_async_email(msg):
    with app.app_context():
        mail.send(msg)

@app.route('/send-email')
def send_email():
    msg = Message("Hello", recipients=["to@example.com"])
    msg.body = "This is a test email sent from a background Celery task."
    send_async_email.delay(msg)
    return "Email sent!"
