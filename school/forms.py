from django import forms
from .models import *

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'user_full_name',
            'user_email',
            'user_password',
            'user_phone',
            'user_phonenumber',
            'phone_number',
        ]

        widgets = {
            'user_password': forms.PasswordInput(),  # Hide the password input
        }