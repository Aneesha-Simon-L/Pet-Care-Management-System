from django.shortcuts import render,redirect

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
    
        pets = Pets.objects.all()

        return render(request, 'pet_app/pet_list.html', {'pets': pets})

class ThankYouView(View):

    def get(self, request, *args, **kwargs):

        pet_id = kwargs.get('pet_id')            #  get pet_id from URL

        pet = Pets.objects.get(id=pet_id)

        return render(request, 'pet_app/thank_you.html', {'pet': pet})



            #     pet.pet_id = get_admission_number()

            # # return redirect('pet')

            #     username = pet.email

            #     password = get_password()

            #     print(password)

            #     profile = Profile.objects.create_user(username=username, password=password, role = 'Pet')

            #     pet.profile = profile

            #     pet.save()

            # return redirect('pets-list')

        

            # Process the form data
        #     return redirect('pet-register')
        
        # return render(request, 'pet_app/registration_form.html', {'form': form})



# class PetRegistrationView(LoginRequiredMixin, View):
#     """View for handling pet registration"""
#     template_name = 'pet_app/pet_registration.html'
    
#     def get(self, request, *args, **kwargs):
#         form = PetRegistrationForm()
#         context = {
#             'form': form,
#             'title': 'Register New Pet'
#         }
#         return render(request, self.template_name, context)
    
#     def post(self, request, *args, **kwargs):
#         form = PetRegistrationForm(request.POST, request.FILES)
        
#         if form.is_valid():
#             # Associate the pet with the current user's profile
#             pet = form.save(commit=False)
#             pet.profile = request.user.profile  # Assuming you have a OneToOne relationship
#             pet.save()
            
#             messages.success(request, 'Pet registration successful!')
#             return redirect('pet-detail', pk=pet.id)  # Redirect to pet detail page
        
#         context = {
#             'form': form,
#             'title': 'Register New Pet'
#         }
#         return render(request, self.template_name, context)

# class PetDetailView(View):
#     """View for displaying pet details"""
#     def get(self, request, pk, *args, **kwargs):
#         try:
#             pet = Pets.objects.get(id=pk)
#             context = {
#                 'pet': pet,
#                 'title': f'{pet.name} Details'
#             }
#             return render(request, 'pet_app/pet_detail.html', context)
#         except Pets.DoesNotExist:
#             messages.error(request, 'Pet not found!')
#             return redirect('home')

# class PetListView(LoginRequiredMixin, View):
#     """View for listing all pets belonging to the current user"""
#     def get(self, request, *args, **kwargs):
#         pets = Pets.objects.filter(profile=request.user.profile)
#         context = {
#             'pets': pets,
#             'title': 'My Pets'
#         }
#         return render(request, 'pet_app/pet_list.html', context)    