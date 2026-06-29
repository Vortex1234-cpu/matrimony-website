from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Home page — no separate app needed
    path('', TemplateView.as_view(
        template_name='home/index.html'
    ), name='home'),

    # Apps
    path('accounts/', include('accounts.urls')),
    path('profiles/', include('profiles.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('search/', include('search.urls')),
    path('matches/', include('matches.urls')),
    path('payments/', include('payments.urls')),
    path('notifications/', include('notifications.urls')),
    path('pages/', include('pages.urls')),

    # Password Reset
    path('accounts/password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='accounts/forgot_password.html',
             email_template_name='emails/password_reset_email.txt',
             html_email_template_name='emails/password_reset_email.html',
             subject_template_name='emails/password_reset_subject.txt',
             success_url='/accounts/password-reset/done/'
         ),
         name='password_reset'),

    path('accounts/password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html'
         ),
         name='password_reset_done'),

    path('accounts/password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html',
             success_url='/accounts/password-reset-complete/'
         ),
         name='password_reset_confirm'),

    path('accounts/password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html'
         ),
         name='password_reset_complete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'matrimony_project.views.error_404'
handler500 = 'matrimony_project.views.error_500'