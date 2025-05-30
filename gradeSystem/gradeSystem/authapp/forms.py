from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class SignUpForm(UserCreationForm):
    """
    Responsible for the Registration Form
    """
    
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


class StudentForm(forms.ModelForm):
    """
    Form for updating Student Profile
    """
    
    class Meta:
        model = Student
        fields = ['full_name', 'gender', 'grade_level', 'class_name', 'phone_number', 'address', 'date_of_birth']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter full name',
            }),
            'gender': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Select gender',
            }),
            'grade_level': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Select grade level',
            }),
            'class_name': forms.Select(attrs={  
                'class': 'form-control',
                'placeholder': 'Select class',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number',
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter address',
                'rows': 3,
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
        }

class StaffForm(forms.ModelForm):
    """
    Form for updating Staff Profile
    """
    class Meta:
        model = Staff
        fields = ['full_name', 'gender', 'position', 'phone_number', 'address', 'date_of_birth']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter full name',
            }),
            'gender': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Select gender',
            }),
            'position': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Select staff role',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number',
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter address',
                'rows': 3,
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
        }

class TeacherForm(forms.ModelForm):
    """
    Form for Ipdating Teacher's Profile
    """
    class Meta:
        model = Teacher
        fields = ['full_name', 'gender', 'phone_number', 'subject_taught', 'class_teacher', 'class_names']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter full name',
            }),
            'gender': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Select gender',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number',
            }),
            'subject_taught': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Select subject taught',
            }),
            'class_names': forms.SelectMultiple(attrs={
                'class': 'form-control',
            }),
        }