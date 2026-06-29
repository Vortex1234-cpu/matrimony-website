from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from notifications.models import DeviceToken
from .forms import RegisterForm, LoginForm
from .models import User, AccountDeletionRequest
from .email_utils import (
    generate_otp,
    send_otp_email
)


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.phone = form.cleaned_data['phone']
            user.gender = form.cleaned_data['gender']
            user.first_name = form.cleaned_data['full_name']
            user.is_active = True
            user.is_verified = False

            otp = generate_otp()
            user.otp_code = otp
            user.otp_created_at = timezone.now()
            user.save()

            request.session['otp_user_id'] = user.id
            request.session['otp_purpose'] = 'register'
            request.session.modified = True

            email_sent = False
            if user.email:
                try:
                    email_sent = send_otp_email(user, otp)
                except Exception as e:
                    print(f'Email error: {e}')
                    email_sent = False

            if email_sent:
                messages.success(
                    request,
                    f'✅ OTP sent to {user.email}. '
                    f'Check inbox and spam folder.'
                )
            else:
                messages.warning(
                    request,
                    f'📧 Email could not be sent. '
                    f'Your OTP is: <strong '
                    f'style="font-size:1.5rem;'
                    f'color:#8B0000;letter-spacing:4px;">'
                    f'{otp}</strong>'
                )

            return redirect('verify_otp')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def verify_otp_view(request):
    user_id = request.session.get('otp_user_id')
    purpose = request.session.get('otp_purpose', 'register')

    if not user_id:
        messages.error(request, 'Session expired. Please try again.')
        return redirect('login' if purpose == 'login' else 'register')

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect('register')

    if request.method == 'POST':
        otp_entered = request.POST.get('otp', '').strip()

        if user.is_otp_valid(otp_entered):
            user.otp_code = None
            user.otp_created_at = None

            if purpose == 'login':
                # Login OTP verified
                user.save()
                login(request, user)

                # Save FCM token with logged-in user
                token = request.POST.get("fcm_token")
                if token:
                    DeviceToken.objects.update_or_create(
                        token=token,
                        defaults={
                            "user": user
                        }
                    )

                del request.session['otp_user_id']
                del request.session['otp_purpose']
                messages.success(
                    request,
                    f'Welcome back, {user.first_name}! 👋'
                )
                next_url = request.session.pop('login_next', '')
                return redirect(next_url if next_url else 'dashboard')

            else:
                # Registration OTP verified
                user.is_verified = True
                user.save()
                login(request, user)
                del request.session['otp_user_id']
                del request.session['otp_purpose']
                messages.success(
                    request,
                    f'🎉 Welcome {user.first_name}! Account verified!'
                )
                return redirect('create_profile')
        else:
            messages.error(
                request,
                '❌ Invalid or expired OTP. Try again or resend.'
            )

    return render(
        request,
        'accounts/verify_otp.html',
        {'user': user, 'purpose': purpose}
    )


def resend_otp_view(request):
    user_id = request.session.get('otp_user_id')
    if not user_id:
        return redirect('register')

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect('register')

    otp = generate_otp()
    user.otp_code = otp
    user.otp_created_at = timezone.now()
    user.save()

    email_sent = send_otp_email(user, otp)

    if email_sent:
        messages.success(request, f'✅ New OTP sent to {user.email}!')
    else:
        messages.warning(request, f'⚠️ Could not send email. Use OTP: {otp}')

    return redirect('verify_otp')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username'].strip()
            password = form.cleaned_data['password']

            # Try username first
            user = authenticate(request, username=username, password=password)

            # Try phone number
            if user is None:
                try:
                    user_obj = User.objects.get(phone=username)
                    user = authenticate(
                        request,
                        username=user_obj.username,
                        password=password
                    )
                except Exception:
                    user = None

            # Try email
            if user is None:
                try:
                    user_obj = User.objects.get(email=username)
                    user = authenticate(
                        request,
                        username=user_obj.username,
                        password=password
                    )
                except Exception:
                    user = None

            if user is not None:
                if not user.is_active:
                    messages.error(request, "❌ Your account is disabled.")
                else:
                    login(request, user)

                    # Save FCM token with logged-in user
                    token = request.POST.get("fcm_token")
                    if token:
                        DeviceToken.objects.update_or_create(
                            token=token,
                            defaults={
                                "user": user
                            }
                        )

                    messages.success(
                        request,
                        f"Welcome back, {user.first_name}! 👋"
                    )

                    next_url = request.GET.get("next", "")
                    return redirect(next_url if next_url else "dashboard")
            else:
                messages.error(
                    request,
                    '❌ Invalid credentials. Try again.'
                )
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


def delete_account_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    error = None
    existing_request = AccountDeletionRequest.objects.filter(
        user=request.user, status='pending'
    ).first()

    if request.method == 'POST':
        password = request.POST.get('password', '')
        confirm = request.POST.get('confirm')
        reason = request.POST.get('reason', '').strip()

        if existing_request:
            error = 'You already have a pending deletion request.'
        elif not confirm:
            error = 'Please confirm you understand this action is permanent.'
        elif not request.user.check_password(password):
            error = 'Incorrect password.'
        else:
            AccountDeletionRequest.objects.create(
                user=request.user,
                reason=reason
            )
            messages.success(
                request,
                'Your deletion request has been submitted. '
                'An admin will review it shortly.'
            )
            return redirect('dashboard')

    return render(request, 'accounts/delete_account.html', {
        'error': error,
        'existing_request': existing_request
    })


def test_email_view(request):
    from django.core.mail import send_mail
    from django.conf import settings
    from django.http import HttpResponse

    try:
        send_mail(
            subject='TownMatrimony Test Email',
            message='This is a test email from TownMatrimony.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
        return HttpResponse('✅ Email sent successfully! Check inbox.')
    except Exception as e:
        return HttpResponse(f'❌ Email failed: {str(e)}')


def reset_admin_view(request):
    import os
    from django.http import HttpResponse
    from django.contrib.auth import get_user_model
    User = get_user_model()

    secret = request.GET.get('secret', '')
    expected = os.environ.get('DJANGO_ADMIN_PASSWORD', '')

    if not secret or secret != expected:
        return HttpResponse('❌ Unauthorized', status=401)

    try:
        username = os.environ.get('DJANGO_ADMIN_USERNAME', 'admin')
        email = os.environ.get('DJANGO_ADMIN_EMAIL', '')
        password = os.environ.get('DJANGO_ADMIN_PASSWORD', '')
        phone = os.environ.get('DJANGO_ADMIN_PHONE', '9000000000')

        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            user.set_password(password)
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.is_verified = True
            user.save()
            return HttpResponse(
                f'✅ Admin password reset!'
                f'<br>Username: {username}'
                f'<br>Try logging in now at /admin'
            )
        else:
            user = User(
                username=username,
                email=email,
                phone=phone,
                first_name='Admin',
                is_staff=True,
                is_superuser=True,
                is_active=True,
                is_verified=True,
            )
            user.set_password(password)
            user.save()
            return HttpResponse(
                f'✅ Admin created!'
                f'<br>Username: {username}'
                f'<br>Login at /admin'
            )
    except Exception as e:
        return HttpResponse(f'❌ Error: {str(e)}')