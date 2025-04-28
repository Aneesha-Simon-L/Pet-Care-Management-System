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

from django.contrib import messages

import random

from django.utils import timezone

from datetime import timedelta

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

                messages.success(request, 'Registration successful! Login credentials have been sent to your email.')

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

class ForgotPasswordView(View):

    def get(self, request):

        return render(request, 'customer/forgot-password.html')
    
    def post(self, request):

        email = request.POST.get('email')
        
        try:
            user = Customer.objects.get(email=email, active_status=True)
            
            # Generate a 6-digit OTP
            otp = random.randint(100000, 999999)

            # Save OTP and expiry in session or database (Here using session for simplicity)
            request.session['reset_email'] = email

            request.session['reset_otp'] = otp
            
            request.session['otp_expiry'] = (timezone.now() + timedelta(minutes=5)).timestamp()  # OTP valid for 5 minutes

            # Send email with OTP
            subject = 'Password Reset OTP'
            
            recipients = [email]

            template = 'email/password-reset-otp.html'

            context = {'name': user.name,'otp': otp,}

            thread = threading.Thread(target=send_email, args=(subject, recipients, template, context))

            thread.start()

            messages.success(request, 'An OTP has been sent to your email. Please check your inbox.')

            return redirect('verify-otp')

        except Customer.DoesNotExist:

            messages.error(request, 'No account found with this email.')

            return render(request, 'customer/forgot-password.html')
        
class OTPVerificationView(View):

    def get(self, request):

        return render(request, 'customer/verify-otp.html')

    def post(self, request):

        entered_otp = request.POST.get('otp')

        reset_email = request.session.get('reset_email')
        
        session_otp = request.session.get('reset_otp')

        otp_expiry = request.session.get('otp_expiry')

        if not (reset_email and session_otp and otp_expiry):

            messages.error(request, 'Session expired. Please try again.')

            return redirect('forgot-password')

        if timezone.now().timestamp() > otp_expiry:

            messages.error(request, 'OTP expired. Please request again.')

            return redirect('forgot-password')

        if int(entered_otp) == int(session_otp):

            # OTP correct -> redirect to reset password page
            return redirect('reset-password')
        
        else:
            messages.error(request, 'Invalid OTP. Please try again.')

            return render(request, 'customer/verify-otp.html')

class ResetPasswordView(View):

    def get(self, request):

        return render(request, 'customer/reset-password.html')

    def post(self, request):

        password = request.POST.get('password')

        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:

            messages.error(request, 'Passwords do not match.')

            return render(request, 'customer/reset-password.html')

        reset_email = request.session.get('reset_email')

        if not reset_email:

            messages.error(request, 'Session expired. Please try again.')

            return redirect('forgot-password')

        try:

            user = Customer.objects.get(email=reset_email, active_status=True)

            profile = user.profile

            profile.set_password(password)

            profile.save()

            # Send email notification
            subject = 'Password Changed Successfully'

            recipients = [reset_email]

            template = 'email/password-changed-confirmation.html'
            
            context = {'name': user.name,}

            thread = threading.Thread(target=send_email, args=(subject, recipients, template, context))

            thread.start()

            # Clear session
            request.session.flush()

            messages.success(request, 'Password reset successfully! Please login.')

            return redirect('login')

        except Customer.DoesNotExist:

            messages.error(request, 'Something went wrong. Please try again.')

            return redirect('forgot-password')
        
        