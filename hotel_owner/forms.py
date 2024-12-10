from django import forms
from django.contrib.auth.models import User
from .models import HotelOwner
from django.core.exceptions import ValidationError
from .models import Room

# Custom validator for profile picture size
def validate_image_size(image):
    max_size = 3 * 1024 * 1024  # 3 MB in bytes
    if image.size > max_size:
        raise ValidationError("Image file size should not exceed 3 MB.")

class RoomForm(forms.ModelForm):
    category = forms.CharField(
        max_length=100,
        required=True,
        label="Category",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter room category'})
    )
    price_per_night = forms.DecimalField(
        required=True,
        label="Price Per Night",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price per night'})
    )
    is_available = forms.BooleanField(
        required=False,
        label="Is Available",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    amenities = forms.CharField(
        required=True,
        label="Amenities",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter amenities (e.g., WiFi, TV, AC)',
            'rows': 3
        })
    )
    image = forms.ImageField(
        required=False,
        label="Room Image",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Room
        fields = ['category', 'price_per_night', 'is_available', 'amenities', 'image']


class HotelOwnerRegistrationForm(forms.ModelForm):
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
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}),
        required=True,
        label="Password"
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}),
        required=True,
        label="Confirm Password"
    )
    profile_picture = forms.ImageField(
        required=False,  # Set to False if this field is optional
        validators=[validate_image_size],  # Use custom validators if needed
        label="Profile Picture",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = HotelOwner
        fields = ['hotel_name', 'address', 'contact_number']
        widgets = {
            'hotel_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter hotel name'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter address', 'rows': 3}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter contact number'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already in use.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise ValidationError("The passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        email = self.cleaned_data['email']

        # Check if the email already exists in the HotelOwner model
        if HotelOwner.objects.filter(email=email).exists():
            raise ValidationError(
                "This email is already registered with another hotel owner. Please use a different email.")

        # If email doesn't exist, create the associated User first
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )

        # Create the HotelOwner instance
        hotel_owner = super().save(commit=False)
        hotel_owner.user = user
        hotel_owner.profile_picture = self.cleaned_data['profile_picture']

        if commit:
            hotel_owner.save()  # Now commit the save operation

        return hotel_owner











#eita notun form
class HotelRegistrationForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Full Name', 'class': 'form-control'}),
        label="Name"
    )
    address = forms.CharField(
        max_length=255,
        widget=forms.Textarea(attrs={'placeholder': 'Your Address', 'class': 'form-control', 'rows': 3}),
        label="Address"
    )
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}),
        label="Username"
    )
    contact_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'placeholder': 'Contact Number', 'class': 'form-control'}),
        label="Contact Number"
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email Address', 'class': 'form-control'}),
        label="Email"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}),
        label="Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control'}),
        label="Confirm Password"
    )
    image = forms.ImageField(
        label="Profile Picture",
        required=False
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match!")

        return cleaned_data

