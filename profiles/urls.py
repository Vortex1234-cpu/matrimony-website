from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_profile, name='create_profile'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('my-profile/', views.view_my_profile, name='view_my_profile'),
    path('partner-preference/', views.partner_preference, name='partner_preference'),
    path('view/<int:profile_id>/', views.public_profile_view, name='public_profile_view'),
    path('update-photo/', views.update_photo, name='update_photo'),

    # Shortlist
    path('shortlist/toggle/<int:profile_id>/', views.toggle_shortlist, name='toggle_shortlist'),
    path('shortlist/', views.my_shortlist, name='my_shortlist'),
]