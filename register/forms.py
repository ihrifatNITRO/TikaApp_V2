# register/forms.py

from django import forms

class RegistrationForm(forms.Form):
    # These are the choices for the 'Gender' radio buttons
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Prefer not to say'),
    ]

    # Here we define each field.
    # By default, all fields in Django are required. You don't need to add anything extra.

    full_name = forms.CharField(
        label='Full Name',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'})
    )
    
    # We use IntegerField to make sure only numbers can be typed.
    id_card = forms.IntegerField(
        label='ID Card',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter national ID'})
    )

    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )

    # We use IntegerField here as well for numbers only.
    phone_number = forms.IntegerField(
        label='Phone Number',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your number'})
    )

    # The 'PasswordInput' widget makes the text appear as dots (••••••).
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'})
    )

    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm your password'})
    )

    # 'ChoiceField' with a 'RadioSelect' widget creates the radio buttons.
    gender = forms.ChoiceField(
        label='Gender',
        choices=GENDER_CHOICES,
        widget=forms.RadioSelect
    )