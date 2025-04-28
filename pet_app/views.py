from django.shortcuts import render,redirect,get_object_or_404

from django . views . generic import View

from django . db import transaction

from .forms import PetRegistrationForm , Pets 

from customer . forms import CustomerRegisterForm

from customer . models import Customer

from .utility import sent_email

from authentication.models import Profile

import threading

from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponseBadRequest

from payments . models import Payment

# Create your views here.

class HomeView(View):

    def get(self,request,*args,**kwargs):

        return render(request,'pet_app/home.html')
    
class AboutusView(View):

    def get(self,request,*args,**kwargs):

        return render(request,'pet_app/about.html')
    
class ContactusView(View):

    def get(self,request,*args,**kwargs):

        return render(request,'pet_app/contact.html')
    
    def post(self,request,*args,**kwargs):

        return redirect('contact-success')
    
class ContactSuccessView(View):

    def get(self,request,*args,**kwargs):

        return render(request,'pet_app/contact_success.html')
    
    # def post(self,request,*args,**kwargs):

    #     return redirect('contact-success')
                
class ServiceView(View):

    def get(self,request,*args,**kwargs):

        return render(request,'pet_app/service.html')
    
class PetRegistrationView(View):
    
    def get(self,request,*args,**kwargs):

        form =  PetRegistrationForm()

        data = {'form' : form}
        
        return render(request,'pet_app/service_registration_form.html',context=data)
        
    def post(self,request,*args,**kwargs):

        form = PetRegistrationForm(request.POST, request.FILES)

        # customer_form = CustomerRegisterForm(request.POST,request.FILES)

        customer = Customer.objects.get(profile=request.user)

        if form.is_valid():

            with transaction.atomic():

                pet = form.save(commit=False)

                pet.customer = customer

                pet.save()

                Payment.objects.create(pet=pet,amount=120,customer=pet.customer)
                
                service  =  pet.service_type

                # customer = customer_form.save()

                subject = 'Service Credentials'

                recepients = [customer.email]

                template = 'email/service-credentials.html'

                context = {'pet':pet}

                print(service)

                print(recepients)

                thread = threading.Thread(target=sent_email,args=(subject,recepients,template,context))

                thread.start()

                return redirect('thank-you',uuid=pet.uuid)          
            
        else:

            print(form.errors)

            data = {'form': form}    

            return render(request,'pet_app/service_registration_form.html',context=data)

class PetListView(View):

    def get(self,request,*args,**kwargs):

        user = request.user

        print(user)

        if user.role == 'Admin':

            # Admin sees all pets
            pets = Pets.objects.filter(active_status=True).order_by('-created_at')

        elif user.role == 'Vet':

            # Vet sees only VETENARY or VACCINATION pets with active_status=True
            pets = Pets.objects.filter(active_status=True, service_type__in=['VETERINARY','VACCINATION']).order_by('-created_at')

        else:

            # Other users see only active pets
            pets = Pets.objects.none()

        return render(request, 'pet_app/pet_list.html',{'pets': pets})
            
class ThankYouView(View):

    def get(self, request, *args, **kwargs):

        uuid = kwargs.get('uuid')

        pet = get_object_or_404(Pets, uuid=uuid)

        return render(request, 'pet_app/thank_you.html',{'pet':pet})
    
# Update View
class PetUpdateView(View):

    def get(self,request,uuid,*args,**kwargs):

        pet = get_object_or_404(Pets, uuid=uuid)

        form = PetRegistrationForm(instance=pet)
        
        return render(request, 'pet_app/service_registration_form.html', {'form': form})

    def post(self, request, uuid, *args, **kwargs):

        pet = get_object_or_404(Pets, uuid=uuid)

        form = PetRegistrationForm(request.POST, request.FILES, instance=pet)

        if form.is_valid():

            form.save()

            return redirect('pet-list')  
        
        return render(request, 'pet_app/service_registration_form.html', {'form': form})
    
# Delete View
class PetDeleteView(View):

    def get(self, request, uuid, *args, **kwargs):

        pet = get_object_or_404(Pets, uuid=uuid)

        return render(request,'pet_app/pet_confirm_delete.html', {'pet': pet})

    def post(self, request, uuid, *args, **kwargs):

        pet = get_object_or_404(Pets, uuid=uuid)

        pet.active_status = False

        pet.save()

        return redirect('pet-list')
    

    
@csrf_exempt
def update_pet_status(request, uuid):

    if request.method == "POST":

        pet = get_object_or_404(Pets, uuid=uuid)

        new_status = request.POST.get('appointment_status')

        if new_status:

            pet.appointment_status = new_status

            pet.save()

            if new_status == 'REJECTED':

                user_role = request.user.role   # Assuming user has related Profile model

                if user_role in ['Admin']:

                    subject = 'Appointment Rejected'

                    recipients = [pet.customer.email]

                    print(pet.customer.email)  # For debugging/logging

                    template = 'email/rejected.html'  # Your cancellation email template

                    context = {'name': pet.customer.name,'category': pet.category,'service_type':pet.service_type,'appointment_status': pet.appointment_status,}

                    thread = threading.Thread(target=sent_email, args=(subject, recipients, template, context))

                    thread.start()

            return redirect('pet-list')

        return HttpResponseBadRequest("Missing status value.")

    return HttpResponseBadRequest("Invalid request method.")