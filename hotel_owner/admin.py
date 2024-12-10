from django.contrib import admin
from .models import Hotel, Room, Review, HotelOwner #eikhane HotelOwner add korci

admin.site.register(Hotel)
admin.site.register(Room)
admin.site.register(Review)

#eida notun kore add korci
admin.site.register(HotelOwner)
