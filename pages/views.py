from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings


def privacy_policy(request):
    return render(request, 'pages/privacy_policy.html')


def terms_conditions(request):
    return render(request, 'pages/terms_conditions.html')


def refund_policy(request):
    return render(request, 'pages/refund_policy.html')


def child_safety_standards(request):
    return render(request, 'pages/child_safety_standards.html')


def about_us(request):
    return render(request, 'pages/about_us.html')


def contact_us(request):
    if request.method == 'POST':
        name    = request.POST.get('name', '').strip()
        phone   = request.POST.get('phone', '').strip()
        email   = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        if not name or not phone or not message:
            messages.error(
                request,
                '❌ Please fill all required fields.'
            )
            return render(
                request, 'pages/contact_us.html'
            )

        # Send email to admin
        try:
            email_body = (
                f"New Contact Form Submission\n\n"
                f"Name    : {name}\n"
                f"Phone   : {phone}\n"
                f"Email   : {email}\n"
                f"Subject : {subject}\n\n"
                f"Message :\n{message}"
            )
            send_mail(
                subject=f'[MoonMatrimony] Contact: {subject}',
                message=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=True,
            )
        except Exception as e:
            print(f'Contact email error: {e}')

        messages.success(
            request,
            '✅ Your message has been sent! '
            'We will reply within 24 hours.'
        )
        return redirect('contact_us')

    return render(request, 'pages/contact_us.html')