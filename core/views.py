from django.shortcuts import render

def homepage(request):
    return render(request, 'core/homepage.html')  # Ensure this path matches the template location

