from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout , get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Itinerary

# Authentication Views

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user to the database
            print(f"User created: {user.username}")  # Debug print
            messages.success(request, f'Account created for {user.username}!')
            return redirect('login')
        else:
            print("Form errors:", form.errors)  # Debug print
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    """
    Handles user login.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    """
    Handles user logout.
    """
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')

@login_required
# Itinerary Management Views
def home(request):
    """
    Homepage view: Displays a list of all itineraries.
    """
    itineraries = Itinerary.objects.filter(user=request.user)
    return render(request, 'homepage.html', {'itineraries': itineraries})

def itinerary_detail(request, pk):
    """
    Detail view: Displays details of a specific itinerary.
    """
    itinerary = get_object_or_404(Itinerary, pk=pk, user=request.user)
    return render(request, 'itinerary_detail.html', {'itinerary': itinerary})

@login_required
def create_itinerary(request):
    """
    Create view: Handles creating a new itinerary.
    """
    if request.method == 'POST':
        title = request.POST.get('title')
        destination = request.POST.get('destination')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        activities = request.POST.get('activities')
        expenses = request.POST.get('expenses')

        Itinerary.objects.create(
            user=request.user,  # Associate itinerary with the current user
            title=title,
            destination=destination,
            start_date=start_date,
            end_date=end_date,
            activities=activities,
            expenses=expenses,
        )
        return redirect('home')
    return render(request, 'create_itinerary.html')

def edit_itinerary(request, pk):
    """
    Edit view: Handles updating an existing itinerary.
    """
    itinerary = get_object_or_404(Itinerary, pk=pk, user=request.user)
    
    if request.method == 'POST':
        itinerary.title = request.POST.get('title')
        itinerary.destination = request.POST.get('destination')
        itinerary.start_date = request.POST.get('start_date')
        itinerary.end_date = request.POST.get('end_date')
        itinerary.activities = request.POST.get('activities')
        itinerary.expenses = request.POST.get('expenses')
        itinerary.save()
        return redirect('home')
    
    context = {'itinerary': itinerary}
    return render(request, 'edit_itinerary.html', context)

def delete_itinerary(request, pk):
    """
    Delete view: Handles deleting an itinerary.
    """
    itinerary = get_object_or_404(Itinerary, pk=pk, user=request.user)
    if request.method == 'POST':
        itinerary.delete()
        return redirect('home')
    return render(request, 'delete_itinerary.html', {'itinerary': itinerary})

def share_itinerary(request, pk):
    """
    Share view: Generates a shareable link for an itinerary.
    """
    itinerary = get_object_or_404(Itinerary, pk=pk, user=request.user)
    shareable_link = f"{request.build_absolute_uri('/')}itinerary/{itinerary.id}/"
    return render(request, 'share_itinerary.html', {'itinerary': itinerary, 'shareable_link': shareable_link})
