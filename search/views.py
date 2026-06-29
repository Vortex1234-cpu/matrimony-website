from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import date, timedelta
from profiles.models import Profile
from .forms import SearchForm


def get_opposite_gender(user):
    if hasattr(user, 'profile'):
        return None
    try:
        if user.gender == 'male':
            return 'female'
        elif user.gender == 'female':
            return 'male'
    except:
        pass
    return None


@login_required
def search_view(request):
    form = SearchForm(request.GET or None)
    profiles = Profile.objects.filter(
        is_approved=True
    ).exclude(
        user=request.user
    ).order_by('-created_at')

    # Filter by opposite gender
    if request.user.gender == 'male':
        profiles = profiles.filter(user__gender='female')
    elif request.user.gender == 'female':
        profiles = profiles.filter(user__gender='male')

    if form.is_valid():
        data = form.cleaned_data

        # Keyword search
        keyword = data.get('keyword')
        if keyword:
            profiles = profiles.filter(
                full_name__icontains=keyword
            ) | profiles.filter(
                city__icontains=keyword
            ) | profiles.filter(
                job_title__icontains=keyword
            ) | profiles.filter(
                caste__icontains=keyword
            )

        # Age filter
        min_age = data.get('min_age')
        max_age = data.get('max_age')
        today = date.today()

        if min_age:
            max_dob = today - timedelta(days=min_age * 365)
            profiles = profiles.filter(
                date_of_birth__lte=max_dob
            )
        if max_age:
            min_dob = today - timedelta(days=max_age * 365)
            profiles = profiles.filter(
                date_of_birth__gte=min_dob
            )

        # Religion
        if data.get('religion'):
            profiles = profiles.filter(
                religion=data['religion']
            )

        # Caste
        if data.get('caste'):
            profiles = profiles.filter(
                caste__icontains=data['caste']
            )

        # Education
        if data.get('education'):
            profiles = profiles.filter(
                education=data['education']
            )

        # Employment
        if data.get('employment_type'):
            profiles = profiles.filter(
                employment_type=data['employment_type']
            )

        # Location
        if data.get('city'):
            profiles = profiles.filter(
                city__icontains=data['city']
            )
        if data.get('district'):
            profiles = profiles.filter(
                district__icontains=data['district']
            )
        if data.get('state'):
            profiles = profiles.filter(
                state__icontains=data['state']
            )

        # Marital Status
        if data.get('marital_status'):
            profiles = profiles.filter(
                marital_status=data['marital_status']
            )

        # Height
        if data.get('min_height'):
            profiles = profiles.filter(
                height_cm__gte=data['min_height']
            )
        if data.get('max_height'):
            profiles = profiles.filter(
                height_cm__lte=data['max_height']
            )

        # Dosham
        if data.get('chevvai_dosham'):
            profiles = profiles.filter(
                chevvai_dosham=data['chevvai_dosham']
            )

        # Star & Rasi
        if data.get('star'):
            profiles = profiles.filter(
                star__icontains=data['star']
            )
        if data.get('rasi'):
            profiles = profiles.filter(
                rasi__icontains=data['rasi']
            )

    # Pagination
    paginator = Paginator(profiles, 12)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Check if HTMX request
    if request.headers.get('HX-Request'):
        return render(request, 'search/partials/results.html', {
            'profiles': page_obj,
            'total': profiles.count()
        })

    return render(request, 'search/search.html', {
        'form': form,
        'profiles': page_obj,
        'total': profiles.count()
    })