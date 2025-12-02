from django import forms
from django.contrib.auth.models import User
class ContactForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)


class SignupForm(forms.ModelForm):

    class Meta:
        model = User 
        fields = ['first_name', 'last_name', 'email', 'username', 'password']

