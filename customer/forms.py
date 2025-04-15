from django import forms

from .models import Customer

class CustomerRegisterForm(forms.ModelForm):

    class Meta:

        model = Customer

        exclude = ['uuid', 'active_status','profile']  # Assuming you have these in BaseClass

        widgets = {'name': forms.TextInput(attrs={'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-select',
                                                  'placeholder': 'Enter full name',
                                                  'required': 'required'}),

                    'contact': forms.TextInput(attrs={'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-select',
                                                      'placeholder': 'Enter phone number',
                                                      'required': 'required'}),

                    'email': forms.EmailInput(attrs={'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-select',
                                                     'placeholder': 'Enter email address',
                                                     'required': 'required'}),

                    'place': forms.TextInput(attrs={'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-select',
                                                    'placeholder': 'Enter place'}),}


    # def __init__(self, *args, **kwargs):

    #     super(CustomerRegistrationForm, self).__init__(*args, **kwargs)

    #     for field in self.fields:

    #         self.fields[field].widget.attrs['autocomplete'] = 'off'
