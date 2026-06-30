from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Authentication
    path('register/', views.register_view, name='register'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('resend-otp/', views.resend_otp_view, name='resend_otp'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Account Management
    path('delete-account/', views.delete_account_view, name='delete_account'),
    path('reset-admin/', views.reset_admin_view, name='reset_admin'),
    path('test-email/', views.test_email_view, name='test_email'),

    # Password Reset
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='accounts/forgot_password.html',
            email_template_name='accounts/password_reset_email.html',
            success_url='/accounts/password-reset/done/'
        ),
        name='password_reset'
    ),

    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='accounts/password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='accounts/password_reset_confirm.html',
            success_url='/accounts/reset-complete/'
        ),
        name='password_reset_confirm'
    ),

    path(
        'reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='accounts/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
]
# urls.py
path('api/update-fcm-token/', views.update_fcm_token_view, name='update_fcm_token'),