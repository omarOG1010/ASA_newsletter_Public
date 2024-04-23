from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import Subscriber
from .forms import SubscriberForm
import random
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Helper Functions

# Function to generate random digits
def random_digits():
    return "%0.12d" % random.randint(0, 999999999999)

# View for handling new subscriptions
@csrf_exempt
def new(request):
    if request.method == 'POST':
        # Extract email from the form
        email = request.POST['email']
        
        # Create a new Subscriber instance with the provided email
        sub = Subscriber(email=email)

        # Check if the email already exists in the database
        if Subscriber.objects.filter(email=email).exists():
            # If email exists, render the index.html template with a message indicating that the email is already subscribed
            return render(request, 'index.html', {'email': sub.email, 'action': 'Email has Already been Added ', 'form': SubscriberForm()})
        else:
            # If email doesn't exist, save the Subscriber instance to the database
            sub.save()
            
            # Compose the confirmation email message
            message = Mail(
                from_email=settings.FROM_EMAIL,
                to_emails=sub.email,
                subject='Newsletter Confirmation',
                html_content='<!DOCTYPE html> <html lang="en"> ... </html>'
            )
            
            # Send the confirmation email using SendGrid API
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            response = sg.send(message)
            
            # Render the index.html template with a message indicating successful subscription
            return render(request, 'index.html', {'email': sub.email, 'action': 'Added to the Newsletter', 'form': SubscriberForm()})
    else:
        # If request method is not POST, render the index.html template with the SubscriberForm
        return render(request, 'index.html', {'form': SubscriberForm()})
    

# View for handling unsubscribe requests
def delete(request):
    # Retrieve the Subscriber object using the email provided in the request
    sub = Subscriber.objects.get(email=request.GET['email'])
    
    # Delete the Subscriber object from the database
    sub.delete()
    
    # Render the index.html template with a message indicating successful unsubscription
    return render(request, 'index.html', {'email': sub.email, 'action': 'unsubscribed'})

# def confirm(request):
#     sub = Subscriber.objects.get(email=request.GET['email'])
#     if sub.conf_num == request.GET['conf_num']:
#         sub.confirmed = True
#         sub.save()
#         return render(request, 'index.html', {'email': sub.email, 'action': 'confirmed'})
#     else:
#         return render(request, 'index.html', {'email': sub.email, 'action': 'denied'})
