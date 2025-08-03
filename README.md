# Donation App with Stripe Integration

A beautiful and modern donation application built with Django, Bootstrap, and Stripe payment processing.

## Features

- 🎨 **Modern UI/UX**: Beautiful, responsive design with Bootstrap 5
- 💳 **Secure Payments**: Stripe integration for safe payment processing
- 📱 **Mobile Responsive**: Works perfectly on all devices
- 🔒 **Security**: CSRF protection and secure payment handling
- 📊 **Admin Panel**: Django admin interface for managing donations
- 📧 **Email Integration**: Ready for email confirmation setup
- 🌐 **Social Sharing**: Built-in social media sharing functionality

## Pages

1. **Home Page** (`home.html`): Landing page with donation form
2. **Success Page** (`success.html`): Confirmation page after successful donation
3. **Cancel Page** (`cancel.html`): Page shown when donation is cancelled
4. **Base Template** (`base.html`): Common layout and styling

## Technology Stack

- **Backend**: Django 5.2.4
- **Frontend**: HTML5, CSS3, Bootstrap 5.3.0
- **Payment**: Stripe API
- **Database**: SQLite (can be changed to PostgreSQL/MySQL)
- **Icons**: Font Awesome 6.4.0
- **Fonts**: Google Fonts (Inter)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd gateway_-_stripe
```

### 2. Create Virtual Environment
```bash
python -m venv venv
```

### 3. Activate Virtual Environment
**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Set Up Stripe

1. Create a Stripe account at [stripe.com](https://stripe.com)
2. Get your API keys from the Stripe Dashboard
3. Update the settings in `stripe/settings.py`:

```python
STRIPE_PUBLISHABLE_KEY = 'pk_test_your_actual_publishable_key'
STRIPE_SECRET_KEY = 'sk_test_your_actual_secret_key'
STRIPE_WEBHOOK_SECRET = 'whsec_your_webhook_secret'
```

### 6. Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 8. Run the Development Server
```bash
python manage.py runserver
```

### 9. Access the Application
- Home page: http://127.0.0.1:8000/
- Admin panel: http://127.0.0.1:8000/admin/

## Stripe Webhook Setup

For production, you'll need to set up Stripe webhooks:

1. Go to your Stripe Dashboard
2. Navigate to Developers > Webhooks
3. Add endpoint: `https://yourdomain.com/webhook/`
4. Select events: `payment_intent.succeeded`, `payment_intent.payment_failed`
5. Copy the webhook secret and update `STRIPE_WEBHOOK_SECRET` in settings

## Project Structure

```
gateway_-_stripe/
├── payment/                 # Main app
│   ├── templates/
│   │   └── payment/
│   │       ├── base.html    # Base template
│   │       ├── home.html    # Landing page
│   │       ├── success.html # Success page
│   │       └── cancel.html  # Cancel page
│   ├── models.py           # Donation model
│   ├── views.py            # View functions
│   ├── urls.py             # URL patterns
│   └── admin.py            # Admin configuration
├── stripe/                 # Project settings
│   ├── settings.py         # Django settings
│   └── urls.py             # Main URL configuration
├── static/                 # Static files
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Customization

### Styling
- Modify CSS variables in `base.html` to change colors
- Update Bootstrap classes for layout changes
- Customize animations and transitions

### Payment Options
- Add more payment methods in Stripe
- Modify donation amounts in `home.html`
- Add recurring donation options

### Features
- Add email notifications
- Implement donation tracking
- Add user accounts and donation history
- Create donation goals and progress bars

## Security Considerations

- Never commit API keys to version control
- Use environment variables for sensitive data
- Enable HTTPS in production
- Regularly update dependencies
- Monitor Stripe webhook events

## Testing

For testing payments, use Stripe's test card numbers:
- **Success**: 4242 4242 4242 4242
- **Decline**: 4000 0000 0000 0002
- **Expired**: 4000 0000 0000 0069

## Deployment

1. Set `DEBUG = False` in production
2. Configure a production database (PostgreSQL recommended)
3. Set up static file serving
4. Configure HTTPS
5. Set up proper environment variables
6. Use a production WSGI server (Gunicorn)

## Support

For issues and questions:
1. Check the Django and Stripe documentation
2. Review the code comments
3. Test with Stripe's test mode first

## License

This project is open source and available under the MIT License.

---

**Note**: This is a development setup. For production use, ensure proper security measures and follow Django deployment best practices. 