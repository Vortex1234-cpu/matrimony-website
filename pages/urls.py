from django.urls import path
from . import views

urlpatterns = [
    path('about/',          views.about_us,         name='about_us'),
    path('contact/',        views.contact_us,        name='contact_us'),
    path('privacy-policy/', views.privacy_policy,    name='privacy_policy'),
    path('terms/',          views.terms_conditions,  name='terms_conditions'),
    path('refund-policy/',  views.refund_policy,     name='refund_policy'),
    path('child-safety-standards/', views.child_safety_standards, name='child_safety_standards'),
]