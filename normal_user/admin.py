from django.contrib import admin
from .models import Booking, Payment, Notification

admin.site.register(Booking)
admin.site.register(Payment)
admin.site.register(Notification)
