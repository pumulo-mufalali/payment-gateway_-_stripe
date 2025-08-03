import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import Donation

# Configure Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

def home(request):
    """Landing page with donation form"""
    context = {
        'stripe_public_key': settings.STRIPE_PUBLISHABLE_KEY,
    }
    return render(request, 'payment/home.html', context)

@require_http_methods(["POST"])
def create_payment_intent(request):
    """Create Stripe payment intent for donation"""
    try:
        data = json.loads(request.body)
        amount = data.get('amount')
        name = data.get('name')
        email = data.get('email')
        message = data.get('message', '')
        
        # Validate amount
        if not amount or float(amount) <= 0:
            return JsonResponse({'error': 'Invalid amount'}, status=400)
        
        # Create payment intent
        intent = stripe.PaymentIntent.create(
            amount=int(float(amount) * 100),  # Convert to cents
            currency='usd',
            metadata={
                'name': name,
                'email': email,
                'message': message
            }
        )
        
        # Create donation record
        donation = Donation.objects.create(
            name=name,
            email=email,
            amount=amount,
            message=message,
            stripe_payment_intent_id=intent.id
        )
        
        return JsonResponse({
            'client_secret': intent.client_secret,
            'donation_id': donation.id
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def stripe_webhook(request):
    """Handle Stripe webhooks for payment status updates"""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError as e:
        return JsonResponse({'error': 'Invalid signature'}, status=400)
    
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        donation = get_object_or_404(
            Donation, 
            stripe_payment_intent_id=payment_intent['id']
        )
        donation.payment_status = 'completed'
        donation.save()
        
    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        donation = get_object_or_404(
            Donation, 
            stripe_payment_intent_id=payment_intent['id']
        )
        donation.payment_status = 'failed'
        donation.save()
    
    return JsonResponse({'status': 'success'})

def success(request, donation_id):
    """Success page after successful donation"""
    donation = get_object_or_404(Donation, id=donation_id)
    context = {
        'donation': donation,
    }
    return render(request, 'payment/success.html', context)

def cancel(request):
    """Cancel page when payment is cancelled"""
    return render(request, 'payment/cancel.html')