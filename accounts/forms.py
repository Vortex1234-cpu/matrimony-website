from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

INPUT_CLASS = 'form-control'
SELECT_CLASS = 'form-select'

class RegisterForm(UserCreationForm):

    GENDER_CHOICES = [
        ('', 'Select Gender'),
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    full_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your full name',
            'class': INPUT_CLASS
        })
    )
    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter 10 digit mobile number',
            'class': INPUT_CLASS
        })
    )
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={
            'class': SELECT_CLASS
        })
    )
    email = forms.EmailField(
        required=True,  # Email is now mandatory
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your email',
            'class': INPUT_CLASS
        })
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Create a password',
            'class': INPUT_CLASS
        })
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm your password',
            'class': INPUT_CLASS
        })
    )

    class Meta:
        model = User
        fields = [
            'full_name', 'phone', 'gender',
            'email', 'username',
            'password1', 'password2'
        ]
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Choose a username',
                'class': INPUT_CLASS
            })
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit():
            raise forms.ValidationError(
                'Phone number must contain only digits'
            )
        if len(phone) != 10:
            raise forms.ValidationError(
                'Phone number must be exactly 10 digits'
            )
        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError(
                'This phone number is already registered'
            )
        return phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError(
                'Email address is required.'
            )
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'This email is already registered. '
                'Please use a different email or login.'
            )
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                'This username is already taken. '
                'Please choose another.'
            )
        return username


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter username or phone',
            'class': INPUT_CLASS
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter your password',
            'class': INPUT_CLASS
        })
    )