import stripe as stripe_api
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import Donation


stripe_api.api_key = settings.STRIPE_SECRET_KEY

def home(request):
    context = {
        'stripe_public_key': settings.STRIPE_PUBLISHABLE_KEY,
    }
    return render(request, 'payment/home.html', context)

@require_http_methods(["POST"])
def create_payment_intent(request):
    try:
        data = json.loads(request.body)
        name = data.get('name')
        email = data.get('email')
        message = data.get('message', '')

        try:
            amount = float(data.get('amount', 0))
            if amount <= 0:
                return JsonResponse({'error': 'Invalid amount'}, status=400)
            
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Invalid amount'}, status=400)
        
        intent = stripe_api.PaymentIntent.create(
            amount=int(float(amount) * 100),  # Convert to cents
            currency='usd',
            metadata={
                'name': name,
                'email': email,
                'message': message
            }
        )
        
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
        event = stripe_api.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe_api.error.SignatureVerificationError as e:
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
    donation = get_object_or_404(Donation, id=donation_id)
    context = {
        'donation': donation,
    }
    return render(request, 'payment/success.html', context)

def cancel(request):
    return render(request, 'payment/cancel.html')