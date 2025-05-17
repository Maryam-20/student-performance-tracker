from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import AllUser

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=254)

    class Meta:
        model = AllUser
        fields = [
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]
        widgets = {
            'email': forms.EmailInput(attrs={'autofocus': True}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email  # Set the username as the email
        if commit:
            user.save()
        return user


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = AllUser
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'email': forms.EmailInput(attrs={'autofocus': True}),
        }