from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import User

class SignupForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

