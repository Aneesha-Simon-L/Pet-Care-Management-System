from django.shortcuts import render,redirect, get_object_or_404

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

from . models import Customer

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
        
class CustomerListView(View):

    def get(self, request, *args, **kwargs):
    
        # customers = Customer.objects.all()

        customers = Customer.objects.filter(active_status = True)

        return render(request, 'customer/customer_list.html', {'customers': customers})
    
# Update View
class CustomerUpdateView(View):

    def get(self, request, uuid, *args, **kwargs):
       
        customer = get_object_or_404(Customer, uuid=uuid)            # Fetch customer using uuid
        
        form = CustomerRegisterForm(instance=customer)

        return render(request, 'customer/customer_form.html', {'form': form})

    def post(self, request, uuid, *args, **kwargs):
        
        customer = get_object_or_404(Customer, uuid=uuid)           

        form = CustomerRegisterForm(request.POST, request.FILES, instance=customer)

        if form.is_valid():

            form.save()
            
            return redirect('customer-list')         # Redirect to customer list after saving

        return render(request, 'customer/customer_form.html', {'form': form})

# Delete View
class CustomerDeleteView(View):

    def get(self, request, uuid, *args, **kwargs):
        
        customer = get_object_or_404(Customer, uuid=uuid)

        return render(request, 'customer/customer_confirm_delete.html', {'customer': customer})
    
    def post(self, request, uuid, *args, **kwargs):

        customers = get_object_or_404(Customer, uuid=uuid)

        customers.active_status = False
        
        customers.save()

        return redirect('customer-list')

    # def post(self, request, uuid, *args, **kwargs):
        
    #     customer = get_object_or_404(Customer, uuid=uuid,active_status = False)

    #     customer.delete()
        
    #     return redirect('customer-list')        # Redirect to customer list after deletion
