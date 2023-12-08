from django.shortcuts import render, redirect
from . forms import CreateUserForm, UserLoginForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from . customdecorator import not_logged_in_redirect 

def homepage(request):
    return render(request, 'home.html')

@not_logged_in_redirect('dashboard')
def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    context = { 'registrationForm' : form}
    return render(request, 'register.html', context=context)

@not_logged_in_redirect('dashboard')
def login(request):
    form = UserLoginForm
    if request.method=="POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect("dashboard")

    context = {'loginForm': form}
    return render(request, 'login.html', context=context)

@login_required(login_url="login")
def dashboard(request):
    context = {'user': request.user}
    return render(request, 'dashboard.html', context=context)

def logout(request):
    auth.logout(request)
    return redirect("home")