from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class QuizgoSearchForm(forms.Form):
    search = forms.CharField(
        max_length=100,
        label="searching",
        widget=forms.TextInput(attrs={'class': 'form-control me-3', 'placeholder': 'Search'})
    )

class ClientRegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=30)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)