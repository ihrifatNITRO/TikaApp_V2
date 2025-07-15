# login/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.forms import AuthenticationForm  <-- 1. REMOVE THIS LINE
from django.contrib import messages
from .forms import LoginForm  # <-- 2. ADD THIS LINE TO IMPORT YOUR NEW FORM

def login_view(request):
    if request.method == 'POST':
        # 3. Use your custom LoginForm here
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                # messages.success(request, f"Welcome back, {user.first_name}!")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid email or password.")
        else:
            messages.error(request, "Invalid email or password.")
    else:
        # 4. And also use it here for the empty form
        form = LoginForm()
        
    return render(request, 'login/login.html', {'form': form})

def logout_view(request):
    # This view does not need any changes
    logout(request)
    messages.info(request, "You have been successfully logged out.")
    return redirect('homepage')