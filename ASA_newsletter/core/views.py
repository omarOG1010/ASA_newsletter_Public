

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
def random_digits():
    return "%0.12d" % random.randint(0, 999999999999)

@csrf_exempt
def new(request):
    if request.method == 'POST':
        emails = request.POST['email']
        sub = Subscriber(email=emails)

        if Subscriber.objects.filter(email=emails).exists():
            return render(request, 'index.html', {'email': sub.email, 'action': 'Email has Already been Added ', 'form': SubscriberForm()})
        else:

            sub.save()
            message = Mail(
                from_email=settings.FROM_EMAIL,
                to_emails=sub.email,
                subject='Newsletter Confirmation',
                html_content='<!DOCTYPE html> <html lang="en"> <head> <meta charset="UTF-8"> <meta name="viewport" content="width=device-width, initial-scale=1.0">     <title>Thank You for Subscribing!</title> </head> <body style="font-family: Arial, sans-serif; text-align: center; background-color: #f4f4f4; padding: 20px;"> <div style="background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);"> <h2 style="color: #333333;">Thank You for Subscribing to Our Newsletter!</h2> <p style="color: #666666;">We are excited to have you as part of our community.</p> <p style="color: #666666;">Stay tuned for the latest news and updates.</p> <img src="https://lh3.googleusercontent.com/drive-viewer/AITFw-yW0azqgXTxGi1nLHgsXrPOuz1-4nn1mzY7HYhVVJMc2zFUOQTHVDm_AOIUQrrD0foGSg0XdUxELO5G8CLdlyxSeCcceQ=s1600"="Newsletter Thank You" style="max-width: 250px; height: 250px; margin-top: 20px;">  </div> <p style="color: #999999; margin-top: 20px;">You are receiving this email because you subscribed to our Newsletter.</p> <p style="color: #999999;">© 2023 Arab Student Association. All rights reserved.</p> </body> </html>'
                    )
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY) 
            response = sg.send(message)
            return render(request, 'index.html', {'email': sub.email, 'action': 'Added to the Newsletter', 'form': SubscriberForm()})
    else:
        return render(request, 'index.html', {'form': SubscriberForm()})
    



def delete(request):
    sub = Subscriber.objects.get(email=request.GET['email'])
    sub.delete()
    return render(request, 'index.html', {'email': sub.email, 'action': 'unsubscribed'})
    


# def confirm(request):
#     sub = Subscriber.objects.get(email=request.GET['email'])
#     if sub.conf_num == request.GET['conf_num']:
#         sub.confirmed = True
#         sub.save()
#         return render(request, 'index.html', {'email': sub.email, 'action': 'confirmed'})
#     else:
#         return render(request, 'index.html', {'email': sub.email, 'action': 'denied'})
