from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Validator to restrict image size to 1 MB
def validate_image_size(image):
    max_size = 1 * 1024 * 1024  # 1 MB in bytes
    if image.size > max_size:
        raise ValidationError("Image file size should not exceed 1 MB.")


# HotelOwner Model

class HotelOwner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='hotel_owner')
    hotel_name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    contact_number = models.CharField(max_length=15)
    address = models.TextField()
    profile_picture = models.ImageField(upload_to='hotel_owners/', null=True, blank=True, validators=[validate_image_size])
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.username or self.user.username


# Hotel Model
class Hotel(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='hotel')
    name = models.CharField(max_length=100)
    address = models.TextField()
    contact = models.CharField(max_length=15)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    category = models.CharField(max_length=50)  # e.g., Single, Double, Suite
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    amenities = models.TextField()  # Describe available amenities
    image = models.ImageField(upload_to='room_images/', blank=True, null=True)  # Add this line
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - {self.hotel.name}"


# Booking Model
class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='hotel_owner_bookings')
    customer_name = models.CharField(max_length=255)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Booking for {self.customer_name} in {self.room.hotel.name}"

# Review Model
class Review(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField()  # e.g., 1 to 5 stars
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.hotel.name} by {self.customer.username}"

