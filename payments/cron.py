from . models import Payment

from django.utils import timezone

import threading

from pet_app. utility import sent_email

from apscheduler.schedulers.background import BackgroundScheduler

# cron to sent remainder email about payment
def remainder_email():

    current_date = timezone.now().date()

    five_days_before_date = current_date - timezone.timedelta(days = 5)

    pending_payments = Payment.objects.filter(status='Pending',pet__join_date__lte = five_days_before_date)         # doubt

    if pending_payments.exists():
        
        for payment in pending_payments:

    # sending login credentials to student through mail
            subject = 'Login Credentials'

            # sender = settings.EMAIL_HOST_USER

            recepients = [payment.student.email]

            template = 'email/payment-remainder.html'

            context = {'name' : f'{payment.student.first_name} {payment.student.last_name}'}
                    
            # sent_email(subject,recepients,template,context)

            thread = threading.Thread(target=sent_email,args=(subject,recepients,template,context))

            thread.start()

        print('all mail sent')

# apsheduler

def scheduler_start():

    scheduler = BackgroundScheduler()

    scheduler.add_job(remainder_email,'cron',hour=10,minute=0)

    scheduler.start()           # to start

  