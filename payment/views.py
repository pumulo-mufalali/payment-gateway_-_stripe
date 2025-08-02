from django.shortcuts import render, redirect
from django.urls import reverse

def home(request):
  return render(request, 'payment/home.html')

def pay(request):
  amount_contributed = 100
  if request.method == 'POST':
    print('Data:', request.PST)
  
  return redirect(reverse('success', args=[amount_contributed]))

def successMsg(request, args):
  amount_contributed = args
  return render(request, 'payment/success.html', {'amount_contributed': amount_contributed})