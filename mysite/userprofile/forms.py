from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class RegistrationForm(forms.ModelForm):
    username = forms.RegexField(label="Username", max_length=30,
        regex=r'^[\w.-]+$', error_messages={'invalid': 
            'This value may contain only letters, numbers and ./-/_ characters.'})

    email = forms.EmailField(label='E-mail')
    email_repeat = forms.EmailField(label='E-mail (repeat)', required=True)

    password = forms.CharField(label='Password',
        widget=forms.PasswordInput(render_value=False))
    password_repeat = forms.CharField(label='Password (repeat)',
        widget=forms.PasswordInput(render_value=False))

    first_name = forms.CharField(label='First name', required=False)
    last_name = forms.CharField(label='Last name', required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'email_repeat', 'password', 'password_repeat', 'first_name', 'last_name')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user']
        #fields = '__all__'

class EditProfileForm(forms.ModelForm):

    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name') 
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name']