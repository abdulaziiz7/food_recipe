from django.core.mail import send_mail

from food_recipe import settings
from food_recipe.celery import app


@app.task(bind=True)
def send_email(self, subject, message, email, **kwargs):
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
