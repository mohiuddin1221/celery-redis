
from celery import shared_task
from django.core.mail import EmailMessage
from django.http import HttpResponse
from .models import *
from django.template.loader import render_to_string
from datetime import datetime


@shared_task(name='email_notification')
def send_email_task(subject, body, email):
        email = EmailMessage(subject, body, to=[email])
        email.send()
        return HttpResponse('Emails sent successfully')


@shared_task(name='monthly_newsletter')
def send_newsletter_task():
        subject = "Your Monthly Newsletter"
        subscribers = MessageBord.objects.get(id=1).suscribers.all()

        body = render_to_string('a_messageboard/newsletter.html', {'name': subscribers.profile.name})
        email = EmailMessage( subject, body, to=[subscribers.email] )
        email.content_subtype = "html"
        email.send()


        current_month = datetime.now().strftime('%B')
        subscriber_count = subscribers.count()   
        return f'{current_month} Newsletter to {subscriber_count} subs'