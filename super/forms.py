# super/forms.py

from django import forms
from .models import Child

# This form no longer inherits from AuthenticationForm
class SuperuserLoginForm(forms.Form):
    username = forms.EmailField(
        label='Admin Email',
        widget=forms.EmailInput(attrs={'autofocus': True, 'class': 'form-control'})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


class ChildForm(forms.ModelForm):
    class Meta:
        model = Child
        fields = [
            'child_name', 
            'date_of_birth',
            'blood_group',
            'next_vaccine_date', 
            'taken_vaccines_list'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'next_vaccine_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }