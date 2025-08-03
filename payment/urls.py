from django.urls import path
from .views import home, create_payment_intent, stripe_webhook, success, cancel

urlpatterns = [
    path('', home, name='home'),
    path('create-payment-intent/', create_payment_intent, name='create_payment_intent'),
    path('webhook/', stripe_webhook, name='stripe_webhook'),
    path('success/<int:donation_id>/', success, name='success'),
    path('cancel/', cancel, name='cancel'),
]