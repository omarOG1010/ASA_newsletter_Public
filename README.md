# Django Newsletter 

I created this Newsletter for the Arab Student Asssociation on the University of Minnesota Campus. This can be used as a template to make your own but you'll need the specifications listed below.


## Features

- User Registration and Authentication: Sign up page checks if its a real addressable email and checks for duplicates in the Django server. Send a confirmation email to the signee

- Newsletter Subscription: Users can sign up for a account at https://asanews.up.railway.app/new/  (you can buy a new domain but I'm cheap this one is free from railway).

- Admin Dashboard: Admins can manage newsletter subscriptions and send updates to all subscribers.

- Email Notifications: SendGrid is integrated to send email notifications to subscribers when new updates are available.

## Prerequisites

- Python: Make sure you have Python installed. You can download it from the official website.

- Django: This project uses Django as the web framework. Install it using pip

- SendGrid Account: Sign up for a SendGrid account to send email notifications to subscribers.

- Railway Account: Railway is used for deployment. Sign up for a Railway account and install the Railway CLI for deployment.
## Important Missing settings.py file 
- I intentionally left how how I set up my settings.py file (which comes with the Django template) for security reasons. Though you can lookup many youtube videos to help you with that. 
