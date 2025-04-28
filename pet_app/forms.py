from django import forms

from .models import Pets, PetCategoryChoices, PetGenderChoices, PetStatusChoices,PetServiceChoices

class PetRegistrationForm(forms.ModelForm):

    class Meta:

        model = Pets

        exclude = ['uuid','adm_number','active_status', 'created_at', 'updated_at', 'registration_date','customer','appointment_status']

        widgets = {'name': forms.TextInput(attrs={'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-select',
                                                  'placeholder': 'Enter pet name',
                                                  'required': 'required'}),

                   'breed': forms.TextInput(attrs={'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-select',
                                                   'placeholder': 'Enter breed'}),

                    'age': forms.NumberInput(attrs={'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-select',
                                                    'placeholder': 'Enter age in years',
                                                    'required': 'required'}),

                    'photo': forms.FileInput(attrs={'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-select'}),

                    'dob': forms.DateInput(attrs={'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-select',
                                                  'type': 'date'}),

                    'last_vet_visit': forms.DateInput(attrs={'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-select',
                                                             'type': 'date'}),

                    'is_vaccinated': forms.CheckboxInput(attrs={'class': 'w-5 h-5 text-purple-600 bg-gray-100 border-gray-300 rounded focus:ring-purple-500 dark:focus:ring-purple-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600'}),

                    
                    'appointment_date' :forms.TextInput(attrs={'type':'date',
                                                            'class':'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-select',
                                                            'required':'required'})}

    category = forms.ChoiceField(choices=[('', '------------')] + PetCategoryChoices.choices,widget=forms.Select(attrs={
                                                                                            'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 form-select focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray',
                                                                                            'required': 'required'}))

    gender = forms.ChoiceField(choices=[('', '------------')] + PetGenderChoices.choices,widget=forms.Select(attrs={
                                                                                            'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 form-select focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray',
                                                                                            'required': 'required'}))

    status = forms.ChoiceField(choices=[('', '------------')] + PetStatusChoices.choices,widget=forms.Select(attrs={
                                                                                            'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 form-select focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray',
                                                                                            'required': 'required'}))
    
    service_type = forms.ChoiceField(choices=[('', '------------')] + PetServiceChoices.choices,widget=forms.Select(attrs={
                                                                                            'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 form-select focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray',
                                                                                            'required': 'required'}))

    def clean(self):

        cleaned_data = super().clean()

        age = cleaned_data.get('age')

        if age and age < 0:

            self.add_error('age', 'Age cannot be negative')
        
        return cleaned_data

    def __init__(self,*args,**kwargs):
        
        super(PetRegistrationForm, self).__init__(*args,**kwargs)
        
        # Make photo required only for new pets
        if not self.instance:

            self.fields.get('photo').widget.attrs['required'] = 'required'

