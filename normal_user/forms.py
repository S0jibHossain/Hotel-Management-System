from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


# Custom validator for profile picture size (max 1 MB)
def validate_image_size(image):
    max_size = 1 * 1024 * 1024  # 1 MB in bytes
    if image.size > max_size:
        raise ValidationError("Image file size should not exceed 1 MB.")


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        label="Username",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'})
    )
    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered. Please use a different email.")
        return cleaned_data
