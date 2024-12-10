from django.urls import path
from . import views  # Import your views

# Define URL patterns
urlpatterns = [
    path('book-room/<int:room_id>/', views.book_room, name='book_room'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('login/', views.user_login, name='user_login'),
    path('user_register/', views.user_register, name='user_register'),
    path('user-homepage/', views.user_homepage, name='user_homepage'),
    path('view-rooms/', views.view_rooms, name='view_rooms'),
    path('make-booking/', views.my_bookings, name='make_booking'),
    path('book-room/<int:room_id>/', views.book_room, name='book_room'),
]
