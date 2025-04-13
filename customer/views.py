from django.shortcuts import render,redirect

# Create your views here.

from django . views . generic import View

from .forms import CustomerRegisterForm

from django . db import transaction

from authentication.models import Profile

from .utility import get_password,send_email

from django.core.mail import EmailMultiAlternatives

from django.template.loader import  render_to_string

from django.conf import settings

import threading

import datetime

class CustomerView(View):
    
    def get(self,request,*args,**kwargs):

        form =  CustomerRegisterForm()

        data = {'form' : form}
        
        return render(request,'customer/customer_form.html',context=data)

    def post(self,request,*args,**kwargs):

        form  = CustomerRegisterForm(request.POST,request.FILES)

        if form.is_valid():

            with transaction.atomic():
            
                customer= form.save(commit=False)

                username = customer.email

                password = get_password()

                print(password)

                profile=Profile.objects.create_user(username=username,password=password,role= 'Customer')

                customer.profile = profile

                customer.save()

                #sending login credentails to customer through mail

                subject = 'Login Credentials'

                recepients = [customer.email]

                template = 'email/login-credentials.html'

                context = {'name' : f'{customer.name}','username':username,'password': password}

                # send_email(subject,recepients,template,context)

                thread = threading.Thread(target=send_email,args=(subject,recepients,template,context))

                thread.start()

                return redirect('home')
        else:

            data = {'form' : form}

            return render(request,'customer/customer_form.html',context=data)
        