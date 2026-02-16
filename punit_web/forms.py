from django import forms
from .models import Customer

class CustomerRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
