from django import forms

# Define a form for capturing subscriber email addresses
class SubscriberForm(forms.Form):
    email = forms.EmailField(  # Define an EmailField for the email address
        label='Your email',  # Label displayed in the form
        max_length=100,  # Maximum length of the email address
        widget=forms.EmailInput(attrs={'class': 'form-control'})  # Widget to render the form field with CSS class
    )
