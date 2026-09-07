from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'gender', 'height',
                  'designation', 'job_location', 'district', 'religion', 'caste', 'marriage_level',
                  'father_name', 'mother_name', 'sibling_details', 'profile_pictures']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already registered!')
        return email