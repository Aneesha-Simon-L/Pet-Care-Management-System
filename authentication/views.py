from django.shortcuts import render,redirect

from django . views . generic  import View

from django . contrib . auth . models import User

from . forms import LoginForm

from django . contrib . auth import authenticate

from django.contrib. auth import login,logout

# Create your views here.

class LoginView(View):

    def get(self,request,*args,**kwags):

        form = LoginForm()

        data = {'form' : form}

        return render(request,'authentication/login.html',context=data)
    
    def post(self,request,*args,**kwargs):

        form = LoginForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data.get('username')

            password = form.cleaned_data.get('password')

            print(username,password)

            user = authenticate(username = username, password = password)

            if user:

                login(request,user)

                role = user.role

                if role in ['Admin']:

                    return redirect('home')
                
                elif role in ['Vet']:

                    return redirect('home')
        #             return redirect('home')
                
                elif role in ['Customer']:

                    return redirect('home')
                
                else:
                    error = "Role not recognized."
            else:
                error = "Invalid username or password."
        else:
            error = "Form data is not valid."

        return render(request, 'authentication/login.html',{'form': form,'error': error})

        # data = {'form' : form, 'error' : error}

        # return redirect('home')
        # return redirect('service-register')
            
class LogoutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect('home')