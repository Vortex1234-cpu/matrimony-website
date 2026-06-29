from django import forms

SELECT_CLASS = 'w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-red-400 text-sm'
INPUT_CLASS = 'w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-red-400 text-sm'

class SearchForm(forms.Form):

    RELIGION_CHOICES = [
        ('', 'Any Religion'),
        ('hindu', 'Hindu'),
        ('christian', 'Christian'),
        ('muslim', 'Muslim'),
        ('others', 'Others'),
    ]

    MARITAL_CHOICES = [
        ('', 'Any Status'),
        ('never_married', 'Never Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
    ]

    EDUCATION_CHOICES = [
        ('', 'Any Education'),
        ('school', 'School'),
        ('diploma', 'Diploma'),
        ('ug', 'Under Graduate'),
        ('pg', 'Post Graduate'),
        ('phd', 'PhD'),
    ]

    EMPLOYMENT_CHOICES = [
        ('', 'Any Employment'),
        ('government', 'Government'),
        ('private', 'Private'),
        ('business', 'Business'),
        ('not_working', 'Not Working'),
    ]

    DOSHAM_CHOICES = [
        ('', 'Any'),
        ('no', 'No Dosham'),
        ('yes', 'Has Dosham'),
    ]

    # Age
    min_age = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': INPUT_CLASS,
            'placeholder': 'Min Age',
            'min': 18,
            'max': 60
        })
    )
    max_age = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': INPUT_CLASS,
            'placeholder': 'Max Age',
            'min': 18,
            'max': 60
        })
    )

    # Religion & Caste
    religion = forms.ChoiceField(
        choices=RELIGION_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': SELECT_CLASS})
    )
    caste = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': INPUT_CLASS,
            'placeholder': 'Enter caste'
        })
    )

    # Education & Employment
    education = forms.ChoiceField(
        choices=EDUCATION_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': SELECT_CLASS})
    )
    employment_type = forms.ChoiceField(
        choices=EMPLOYMENT_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': SELECT_CLASS})
    )

    # Location
    city = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': INPUT_CLASS,
            'placeholder': 'City'
        })
    )
    district = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': INPUT_CLASS,
            'placeholder': 'District'
        })
    )
    state = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': INPUT_CLASS,
            'placeholder': 'State'
        })
    )

    # Marital Status
    marital_status = forms.ChoiceField(
        choices=MARITAL_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': SELECT_CLASS})
    )

    # Height
    min_height = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': INPUT_CLASS,
            'placeholder': 'Min Height (cm)'
        })
    )
    max_height = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': INPUT_CLASS,
            'placeholder': 'Max Height (cm)'
        })
    )

    # Horoscope
    chevvai_dosham = forms.ChoiceField(
        choices=DOSHAM_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': SELECT_CLASS})
    )
    star = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': INPUT_CLASS,
            'placeholder': 'Star (Natchathiram)'
        })
    )
    rasi = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': INPUT_CLASS,
            'placeholder': 'Rasi'
        })
    )

    # Keyword search
    keyword = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': INPUT_CLASS,
            'placeholder': '🔍 Search by name, city, job...'
        })
    )