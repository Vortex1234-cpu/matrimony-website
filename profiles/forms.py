from django import forms
from .models import Profile, PartnerPreference

INPUT_CLASS = 'w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-red-400'
SELECT_CLASS = 'w-full border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-red-400'

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        exclude = [
            'user',
            'is_approved',
            'is_premium',
            'profile_views',
            'created_at',
            'updated_at'
        ]
        widgets = {
            # Basic Info
            'full_name': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Enter your full name'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': INPUT_CLASS,
                'type': 'date'
            }),
            'religion': forms.Select(attrs={
                'class': SELECT_CLASS
            }),
            'caste': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Enter your caste'
            }),
            'subcaste': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Enter your subcaste'
            }),
            'mother_tongue': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'e.g. Tamil, Telugu'
            }),
            'marital_status': forms.Select(attrs={
                'class': SELECT_CLASS
            }),

            # Physical
            'height_cm': forms.NumberInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Height in cm (e.g. 165)'
            }),
            'weight_kg': forms.NumberInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Weight in kg (e.g. 60)'
            }),
            'skin_tone': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'e.g. Fair, Wheatish, Dark'
            }),
            'body_type': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'e.g. Slim, Athletic, Average'
            }),

            # Education
            'education': forms.Select(attrs={
                'class': SELECT_CLASS
            }),
            'education_detail': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'e.g. B.E Computer Science'
            }),
            'employment_type': forms.Select(attrs={
                'class': SELECT_CLASS
            }),
            'job_title': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'e.g. Software Engineer'
            }),
            'company': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'e.g. TCS, Infosys'
            }),
            'annual_income': forms.NumberInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Annual income in rupees'
            }),

            # Location
            'city': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Your city'
            }),
            'district': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Your district'
            }),
            'state': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Your state'
            }),
            'country': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Your country'
            }),

            # Family
            'father_name': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Father name'
            }),
            'father_occupation': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Father occupation'
            }),
            'mother_name': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Mother name'
            }),
            'mother_occupation': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Mother occupation'
            }),
            'brothers': forms.NumberInput(attrs={
                'class': INPUT_CLASS
            }),
            'sisters': forms.NumberInput(attrs={
                'class': INPUT_CLASS
            }),
            'family_type': forms.Select(attrs={
                'class': SELECT_CLASS
            }),
            'family_status': forms.Select(attrs={
                'class': SELECT_CLASS
            }),

            # Horoscope
            'star': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'e.g. Ashwini, Bharani'
            }),
            'rasi': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'e.g. Mesham, Rishabam'
            }),
            'lagnam': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'e.g. Mesham'
            }),
            'chevvai_dosham': forms.Select(attrs={
                'class': SELECT_CLASS
            }),
            'sarpa_dosham': forms.Select(attrs={
                'class': SELECT_CLASS
            }),

            # About
            'about': forms.Textarea(attrs={
                'class': INPUT_CLASS,
                'rows': 4,
                'placeholder': 'Write something about yourself...'
            }),

            # Photo
            'profile_photo': forms.FileInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg px-4 py-2',
                'accept': 'image/*'
            }),
        }
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            # ... your existing fields ...
            'hide_photo',
        ]
        widgets = {
            # ... your existing widgets ...
            'hide_photo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class PartnerPreferenceForm(forms.ModelForm):

    class Meta:
        model = PartnerPreference
        exclude = ['user']
        widgets = {
            'min_age': forms.NumberInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Minimum age'
            }),
            'max_age': forms.NumberInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Maximum age'
            }),
            'min_height': forms.NumberInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Minimum height in cm'
            }),
            'max_height': forms.NumberInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Maximum height in cm'
            }),
            'religion': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Preferred religion'
            }),
            'caste': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Preferred caste (leave blank for any)'
            }),
            'education': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Preferred education'
            }),
            'employment': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Preferred employment type'
            }),
            'location': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Preferred location'
            }),
            'marital_status': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'e.g. Never Married'
            }),
            'dosham_ok': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-red-700'
            }),
        }