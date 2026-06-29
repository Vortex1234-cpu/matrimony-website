from django.urls import path
from . import views

urlpatterns = [
    path('plans/',
         views.plans_page,
         name='plans_page'),

    path('create-order/<int:plan_id>/',
         views.create_order,
         name='create_order'),

    path('payment-success/',
         views.payment_success,
         name='payment_success'),

    path('payment-failed/',
         views.payment_failed,
         name='payment_failed'),

    path('my-plan/',
         views.my_plan,
         name='my_plan'),
]