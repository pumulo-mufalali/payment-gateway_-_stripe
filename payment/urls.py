from django.urls import path
from .views import home, pay, successMsg

urlpatterns = [
  path('', home, name='home'),
  path('pay/', pay, name=pay),
  path('success/<str:args>/', successMsg, name='success'),
]