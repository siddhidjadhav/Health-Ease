from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .utility import get_user_identity
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm

# Create your views here.

def home(request):
    return render(request, 'home.html', {})

def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = request.user
    return render(request, 'profile.html', {'user': user})

def register_user(request):
    form = CreateUserForm()
     
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()

    return render(request, 'register.html', {'form': form})

def login_user(request):
    if request.user.is_authenticated:
        return redirect('patient_dashboard')
    if request.method=="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            user_identity = get_user_identity(user)
            print(user_identity)
            return redirect(user_identity)
            ...
        else:
            # Return an 'invalid login' error message.
            messages.success(request, ("Invalid Details"))
            return redirect('login')
            ...
    return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    return redirect('home')