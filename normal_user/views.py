from datetime import timedelta, date, datetime

from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import Group
from hotel_owner.models import Booking
from .forms import UserRegistrationForm
from .models import Booking  # Import Booking from the correct app
from hotel_owner.models import Room  # Import Room from the hotel_owner app


# User Registration View
def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # Assign the user to the NormalUser group
            group, created = Group.objects.get_or_create(name='NormalUser')
            user.groups.add(group)

            # Automatically log the user in
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('user_login')
        else:
            messages.error(request, "There was an error with your registration. Please try again.")
    else:
        form = UserRegistrationForm()

    return render(request, 'normal_user/user_register.html', {'form': form})


# User Login View
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user and user.groups.filter(name='NormalUser').exists():
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('user_homepage')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'normal_user/user_login.html')


# User Homepage (After Login)
@login_required
def user_homepage(request):
    if not request.user.groups.filter(name='NormalUser').exists():
        messages.error(request, "You are not authorized to access this page.")
        return redirect('role_selection')
    return render(request, 'normal_user/user_homepage.html')

# Logout View
def logout_view(request):
    logout(request)
    return redirect('role_selection')


@login_required
def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if request.method == 'POST':
        check_in_date = request.POST.get('check_in_date')
        check_out_date = request.POST.get('check_out_date')

        if not check_in_date or not check_out_date:
            messages.error(request, "Check-in and check-out dates are required.")
            return redirect('book_room', room_id=room_id)

        check_in = date.fromisoformat(check_in_date)
        check_out = date.fromisoformat(check_out_date)

        if check_in >= check_out:
            messages.error(request, "Check-out date must be after check-in date.")
            return redirect('book_room', room_id=room_id)

        # Create booking
        booking = Booking(
            user=request.user,
            room=room,
            check_in_date=check_in,
            check_out_date=check_out,
            total_price=(check_out - check_in).days * room.price_per_night,
            is_confirmed=True
        )
        booking.save()

        # Mark the room as unavailable
        room.is_available = False
        room.save()

        messages.success(request, "Room booked successfully!")
        return redirect('view_rooms')  # Redirect to the room list or bookings page

    return render(request, 'normal_user/book_room.html', {'room': room})


def my_bookings(request):
    return render(request, 'normal_user/my_bookings.html')
    # Replace with actual template path


def view_rooms(request):
    # Get all available rooms
    available_rooms = Room.objects.filter(is_available=True)

    return render(request, 'normal_user/view_rooms.html', {'available_rooms': available_rooms})