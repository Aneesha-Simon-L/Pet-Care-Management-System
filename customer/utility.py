import uuid

import string

import random

from .models import Customer

#email related imports

from django.core.mail import EmailMultiAlternatives

from django.template.loader import  render_to_string

from django.conf import settings

def get_password():
 
    password = ''.join(random.choices(string.ascii_letters + string.digits,k=8))

    return password

#email sending

def send_email(subject,recepients,template,context):

    email_obj = EmailMultiAlternatives(subject,from_email=settings.EMAIL_HOST_USER,to=recepients)

    content = render_to_string(template,context)

    email_obj.attach_alternative(content,'text/html')

    email_obj.send()

