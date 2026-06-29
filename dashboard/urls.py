from django.urls import path
from . import views, admin_views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),

    # Admin Panel
    path('admin-panel/', admin_views.admin_dashboard,
         name='admin_dashboard'),
    path('admin-panel/profiles/', admin_views.admin_profiles,
         name='admin_profiles'),
    path('admin-panel/profiles/approve/<int:profile_id>/',
         admin_views.approve_profile, name='approve_profile'),
    path('admin-panel/profiles/reject/<int:profile_id>/',
         admin_views.reject_profile, name='reject_profile'),
    path('admin-panel/users/', admin_views.admin_users,
         name='admin_users'),
]