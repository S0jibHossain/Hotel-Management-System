from django.urls import path
from . import views  # Import your views


# Define URL patterns
urlpatterns = [
    path('hotel-owner/dashboard/', views.hotel_owner_dashboard, name='hotel_owner_dashboard'), # Replace with your actual view
    path('view-bookings/', views.view_bookings, name='view_bookings'),  # Add this URL
    path('manage-rooms/', views.manage_rooms, name='manage_rooms'),     # Replace with your actual view
    path('manage-rooms/add_room/', views.add_room, name='add_room'),
    path('manage-rooms/update/<int:room_id>/', views.update_room, name='update_room'),
    path('manage-rooms/delete/<int:room_id>/', views.delete_room, name='delete_room'),
    path('hotel-owner/register/', views.hotel_owner_register, name='hotel_owner_register'),
    path('login/', views.login_view, name='hotel_owner/login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.hotel_owner_profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),  # Define the URL for edit_profile

]














