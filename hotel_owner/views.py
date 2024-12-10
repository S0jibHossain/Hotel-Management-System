from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import RoomForm, HotelRegistrationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import HotelOwner, Hotel, Room, Booking


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            try:
                hotel_owner = HotelOwner.objects.get(user=user)  # Ensure the user is a hotel owner
                login(request, user)
                return redirect('hotel_owner_dashboard')  # Redirect to the dashboard
            except HotelOwner.DoesNotExist:
                messages.error(request, "You are not registered as a hotel owner.")
                return redirect('hotel_owner_register')  # Redirect to registration
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('hotel_owner/login')  # Redirect back to login page

    return render(request, 'hotel_owner/login.html')


def hotel_owner_register(request):
    if request.method == 'POST':
        form = HotelRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            username = form.cleaned_data['username']
            contact_number = form.cleaned_data['contact_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            image = form.cleaned_data['image']

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=name.split(' ')[0],
                last_name=' '.join(name.split(' ')[1:]) if len(name.split(' ')) > 1 else ''
            )
            user.save()

            hotel_owner = HotelOwner.objects.create(
                user=user,
                username=username,
                hotel_name=name,
                address=address,
                email=email,
                contact_number=contact_number,
                profile_picture = image
            )
            hotel_owner.save()
            messages.success(request, "Registration successful.")
            return redirect('hotel_owner/login')
        else:
            form = HotelRegistrationForm()
            return render(request, 'hotel_owner/register.html', {'form': form})
    else:
        form = HotelRegistrationForm()
    return render(request, 'hotel_owner/register.html', {'form': form})


@login_required
def hotel_owner_dashboard(request, hotel=None):
    # Ensure the logged-in user is a hotel owner
    if not hasattr(request.user, 'hotel_owner'):
        messages.error(request, "You are not registered as a hotel owner. Please complete registration.")
        return redirect('hotel_owner_register')

    hotel_owner = request.user.hotel_owner

    # try:
    #     # Ensure the hotel owner has an associated hotel
    #     hotel = Hotel.objects.get(owner=request.user)
    # except Hotel.DoesNotExist:
    #     # Redirect if no hotel is associated with the hotel owner
    #     messages.error(request, "No hotel is associated with your account. Please complete your hotel setup.")
    #     return redirect('hotel_owner/login')  # Redirect to a hotel setup view

    # Fetch data for the dashboard
    rooms = Room.objects.filter(hotel=hotel)
    bookings = Booking.objects.filter(room__hotel=hotel)

    context = {
        'hotel_owner': hotel_owner,
        'hotel': hotel,
        'rooms': rooms,
        'bookings': bookings,
    }

    return render(request, 'hotel_owner/dashboard.html', context)


@login_required
def manage_rooms(request):
    try:
        hotel_owner = request.user.hotel_owner
    except HotelOwner.DoesNotExist:
        messages.error(request, "You are not authorized to manage rooms.")
        return redirect('home')

    rooms = Room.objects.filter(hotel__owner=hotel_owner.user)
    return render(request, 'hotel_owner/manage_rooms.html', {'rooms': rooms})


@login_required
def add_room(request):

    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            # Associate the room with the user's hotel
            room = form.save(commit=False)
            # room.hotel = hotel
            room.save()
            return redirect('manage_rooms')  # Redirect to the manage rooms page after saving
    else:
        form = RoomForm()

    # Render the form when the user has a hotel
    return render(request, 'hotel_owner/add_room.html', {'form': form})


@login_required
def update_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, "Room updated successfully!")
            return redirect('manage_rooms')
    else:
        form = RoomForm(instance=room)

    return render(request, 'hotel_owner/update_room.html', {'form': form, 'room': room})


@login_required
def delete_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if request.method == 'POST':
        room.delete()
        messages.success(request, "Room deleted successfully!")
        return redirect('manage_rooms')

    return render(request, 'hotel_owner/delete_room.html', {'room': room})

@login_required
def view_bookings(request):
    try:
        # Fetch bookings related to the logged-in hotel owner's hotel
        hotel = Hotel.objects.get(owner=request.user)
        bookings = Booking.objects.filter(room__hotel=hotel)
    except AttributeError:
        bookings = []

    context = {'bookings': bookings}
    return render(request, 'hotel_owner/view_bookings.html', context)

@login_required
def hotel_owner_profile(request):
    hotel_owner = request.user.hotel_owner  # Get the current hotel owner's profile
    return render(request, 'hotel_owner/profile.html', {'hotel_owner': hotel_owner})

def hotel_owner_login(request):
    if request.user.is_authenticated:
        return redirect('hotel_owner_dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None and hasattr(user, 'hotel_owner'):  # Ensure it's a hotel owner
            login(request, user)
            return redirect('hotel_owner_dashboard')
        else:
            messages.error(request, "Invalid credentials or you are not a hotel owner.")
            return redirect('hotel_owner_login')
    return render(request, 'hotel_owner/login.html')

def edit_profile(request):
    # Your logic for editing the profile
    return render(request, 'hotel_owner/edit_profile.html')

def logout_view(request):
    logout(request)
    return redirect('hotel_owner_login')
