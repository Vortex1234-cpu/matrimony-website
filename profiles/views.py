from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from .models import Profile, PartnerPreference, Shortlist
from .forms import ProfileForm, PartnerPreferenceForm


@login_required
def create_profile(request):
    if hasattr(request.user, 'profile'):
        return redirect('edit_profile')

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            request.user.is_profile_complete = True
            request.user.save()
            messages.success(
                request,
                '✅ Profile created! It will be visible after admin approval.'
            )
            return redirect('partner_preference')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = ProfileForm()

    return render(request, 'profiles/create_profile.html', {
        'form': form,
        'title': 'Create Profile'
    })


@login_required
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Profile updated successfully!')
            return redirect('view_my_profile')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profiles/create_profile.html', {
        'form': form,
        'title': 'Edit Profile'
    })


@login_required
def view_my_profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        messages.warning(request, '⚠️ Please create your profile first.')
        return redirect('create_profile')
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return redirect('dashboard')

    return render(request, 'profiles/view_profile.html', {'profile': profile})


@login_required
def partner_preference(request):
    preference = PartnerPreference.objects.filter(user=request.user).first()

    if request.method == 'POST':
        if preference:
            form = PartnerPreferenceForm(request.POST, instance=preference)
        else:
            form = PartnerPreferenceForm(request.POST)

        if form.is_valid():
            pref = form.save(commit=False)
            pref.user = request.user
            pref.save()
            messages.success(request, '✅ Partner preferences saved!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = PartnerPreferenceForm(instance=preference) if preference else PartnerPreferenceForm()

    return render(request, 'profiles/partner_preference.html', {'form': form})


@login_required
def public_profile_view(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)

    can_view_photo = True
    if profile.hide_photo:
        from matches.models import Interest
        mutual = Interest.objects.filter(
            (
                Q(sender=request.user, receiver=profile.user) |
                Q(sender=profile.user, receiver=request.user)
            ),
            status='accepted'
        ).exists()
        can_view_photo = mutual

    # Get interest status
    from matches.models import Interest
    interest_sent = Interest.objects.filter(
        sender=request.user,
        receiver=profile.user
    ).first()

    is_shortlisted = Shortlist.objects.filter(
        user=request.user,
        profile=profile
    ).exists()

    # Increment profile views
    if profile.user != request.user:
        profile.profile_views += 1
        profile.save(update_fields=['profile_views'])

    return render(request, 'profiles/public_profile.html', {
        'profile': profile,
        'can_view_photo': can_view_photo,
        'interest_sent': interest_sent,
        'is_shortlisted': is_shortlisted,
    })


@login_required
def update_photo(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        photo = request.FILES.get('profile_photo')
        if photo:
            profile.profile_photo = photo
            profile.save()
            messages.success(request, '✅ Photo updated!')
            return redirect('view_my_profile')
        else:
            messages.error(request, '❌ Please select a photo')
    return render(request, 'profiles/update_photo.html', {'profile': profile})


# =============================================
# SHORTLIST / FAVOURITE
# =============================================

@login_required
def toggle_shortlist(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)

    # Can't shortlist your own profile
    if profile.user == request.user:
        return JsonResponse({'error': 'Cannot shortlist yourself.'}, status=400)

    shortlist, created = Shortlist.objects.get_or_create(
        user=request.user,
        profile=profile
    )

    if not created:
        shortlist.delete()
        return JsonResponse({'status': 'removed', 'message': 'Removed from shortlist'})

    return JsonResponse({'status': 'added', 'message': 'Added to shortlist ❤️'})


@login_required
def my_shortlist(request):
    shortlisted = Shortlist.objects.filter(
        user=request.user
    ).select_related('profile')

    return render(request, 'profiles/my_shortlist.html', {
        'shortlisted': shortlisted,
    })