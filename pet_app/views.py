from django.shortcuts import render,redirect,get_object_or_404

# Create your views here.

from django . views . generic import View

from django . db import transaction

from .forms import PetRegistrationForm , Pets 

from customer . forms import CustomerRegisterForm

from customer . models import Customer

from .utility import sent_email

from authentication.models import Profile

import threading

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

                service  =  pet.service_type

                # customer = customer_form.save()

                # customer = 

                subject = 'Service Credentials'

                recepients = [customer.email]

                template = 'email/service-credentials.html'

                context = {'pet':pet}

                print(service)

                print(recepients)

                thread = threading.Thread(target=sent_email,args=(subject,recepients,template,context))

                thread.start()

                return redirect('thank-you',pet_id=pet.id)          #  redirect to thank-you page with pet_id

        else:

            data = {'form': form}    

            return render(request,'pet_app/service_registration_form.html',context=data)

class PetListView(View):

    def get(self, request, *args, **kwargs):
    
        # pets = Pets.objects.all()/

        pets = Pets.objects.filter(active_status = True)

        return render(request, 'pet_app/pet_list.html', {'pets': pets})

class ThankYouView(View):

    def get(self, request, *args, **kwargs):

        pet_id = kwargs.get('pet_id')            #  get pet_id from URL

        pet = Pets.objects.get(id=pet_id)

        return render(request, 'pet_app/thank_you.html', {'pet': pet})

# Update View
class PetUpdateView(View):

    def get(self, request, uuid, *args, **kwargs):

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
    

# class VetPetListView(View):

#     def post(self, request, *args, **kwargs):

#         pet = Pets.objects.all()

#         return render(request,'base.html',{'pet':pet})

# class VetPetListView(View):

#     def post(self, request, *args, **kwargs):
#         # Get all pets with service_type 'VETERINARY'
#         pets = Pets.objects.filter(service_type='VETERINARY')

#         # Render the page with the filtered pets
#         return render(request, 'base.html', {'pets': pets})