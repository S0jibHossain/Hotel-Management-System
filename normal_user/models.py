from django.db import models
from django.contrib.auth.models import User
from hotel_owner.models import Room
from django.contrib.auth.models import AbstractUser

# Booking Model
class Booking(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Booking by {self.user.username} for {self.room}"

# Payment Model
class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    is_successful = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment for booking {self.booking.id}"


# Notification Model (Optional)
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}"


