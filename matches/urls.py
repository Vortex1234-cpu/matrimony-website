from django.urls import path
from . import views

urlpatterns = [
    path('send-interest/<int:profile_id>/',
         views.send_interest,
         name='send_interest'),

    path('accept/<int:interest_id>/',
         views.accept_interest,
         name='accept_interest'),

    path('reject/<int:interest_id>/',
         views.reject_interest,
         name='reject_interest'),

    path('received/',
         views.interests_received,
         name='interests_received'),

    path('sent/',
         views.interests_sent,
         name='interests_sent'),

    path('mutual/',
         views.mutual_matches,
         name='mutual_matches'),
]