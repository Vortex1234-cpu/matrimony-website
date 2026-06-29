from django.db import models
from django.conf import settings


class Profile(models.Model):

    # Religion choices
    RELIGION_CHOICES = [
        ('hindu', 'Hindu'),
        ('christian', 'Christian'),
        ('muslim', 'Muslim'),
        ('others', 'Others'),
    ]

    # Marital status choices
    MARITAL_CHOICES = [
        ('never_married', 'Never Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
    ]

    # Education choices
    EDUCATION_CHOICES = [
        ('school', 'School'),
        ('diploma', 'Diploma'),
        ('ug', 'Under Graduate'),
        ('pg', 'Post Graduate'),
        ('phd', 'PhD'),
    ]

    # Employment choices
    EMPLOYMENT_CHOICES = [
        ('government', 'Government'),
        ('private', 'Private'),
        ('business', 'Business'),
        ('not_working', 'Not Working'),
    ]

    # Dosham choices
    DOSHAM_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
        ('dont_know', "Don't Know"),
    ]

    # Gender choices  ← ADDED
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    # Basic Info
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(           # ← ADDED
        max_length=10,
        choices=GENDER_CHOICES,
        blank=True
    )
    religion = models.CharField(
        max_length=20,
        choices=RELIGION_CHOICES
    )
    caste = models.CharField(max_length=100, blank=True)
    subcaste = models.CharField(max_length=100, blank=True)
    mother_tongue = models.CharField(max_length=50, blank=True)
    marital_status = models.CharField(
        max_length=20,
        choices=MARITAL_CHOICES,
        default='never_married'
    )

    # Physical Info
    height_cm = models.IntegerField(null=True, blank=True)
    weight_kg = models.IntegerField(null=True, blank=True)
    skin_tone = models.CharField(max_length=50, blank=True)
    body_type = models.CharField(max_length=50, blank=True)

    # Education & Career
    education = models.CharField(
        max_length=20,
        choices=EDUCATION_CHOICES,
        blank=True
    )
    education_detail = models.CharField(max_length=200, blank=True)
    employment_type = models.CharField(
        max_length=20,
        choices=EMPLOYMENT_CHOICES,
        blank=True
    )
    job_title = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100, blank=True)
    annual_income = models.IntegerField(null=True, blank=True)

    # Location
    city = models.CharField(max_length=100, blank=True)
    district = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, default='India')

    # Family Info
    father_name = models.CharField(max_length=100, blank=True)
    father_occupation = models.CharField(max_length=100, blank=True)
    mother_name = models.CharField(max_length=100, blank=True)
    mother_occupation = models.CharField(max_length=100, blank=True)
    brothers = models.IntegerField(default=0)
    sisters = models.IntegerField(default=0)
    family_type = models.CharField(
        max_length=20,
        choices=[('nuclear', 'Nuclear'), ('joint', 'Joint')],
        blank=True
    )
    family_status = models.CharField(
        max_length=20,
        choices=[
            ('middle', 'Middle Class'),
            ('upper_middle', 'Upper Middle Class'),
            ('rich', 'Rich'),
        ],
        blank=True
    )

    # Horoscope
    star = models.CharField(max_length=50, blank=True)
    rasi = models.CharField(max_length=50, blank=True)
    lagnam = models.CharField(max_length=50, blank=True)
    chevvai_dosham = models.CharField(
        max_length=20,
        choices=DOSHAM_CHOICES,
        default='dont_know'
    )
    sarpa_dosham = models.CharField(
        max_length=20,
        choices=DOSHAM_CHOICES,
        default='dont_know'
    )

    # About
    about = models.TextField(blank=True)

    # Profile Photo
    profile_photo = models.ImageField(
        upload_to='profile_photos/',
        null=True,
        blank=True,
        default=None
    )
    hide_photo = models.BooleanField(
    default=False,
    help_text="If checked, photo is hidden from public search results"
)

    # Status
    is_approved = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    profile_views = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} - {self.user.phone}"

    def age(self):
        # FIXED: original didn't account for whether birthday has passed this year
        from datetime import date
        today = date.today()
        dob = self.date_of_birth
        return today.year - dob.year - (
            (today.month, today.day) < (dob.month, dob.day)
        )


class PartnerPreference(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='preference'
    )
    min_age = models.IntegerField(default=18)
    max_age = models.IntegerField(default=35)
    min_height = models.IntegerField(default=140)
    max_height = models.IntegerField(default=200)
    religion = models.CharField(max_length=50, blank=True)
    caste = models.CharField(max_length=100, blank=True)
    education = models.CharField(max_length=50, blank=True)
    employment = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=100, blank=True)
    marital_status = models.CharField(max_length=50, blank=True)
    dosham_ok = models.BooleanField(default=True)

    def __str__(self):
        # FIXED: use phone instead of username to match your custom user model
        return f"Preference of {self.user.phone}"
class Shortlist(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='shortlisted_by'
    )
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='shortlisted_in'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'profile')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.phone} → {self.profile.full_name}"

class ProfilePhoto(models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='photos'
    )
    image = models.ImageField(upload_to='profile_photos/')
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo of {self.profile.full_name}"