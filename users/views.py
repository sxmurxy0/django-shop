from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomUserChangeForm


def register(request):
    if request.user.is_authenticated:
        return redirect('shop:catalog')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно! Добро пожаловать!')
            return redirect('shop:catalog')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'register.html', {'form': form})

def _login(request):
    if request.user.is_authenticated:
        return redirect('shop:catalog')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('shop:catalog')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
    
    return render(request, 'login.html')

@login_required
def _logout(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы.')
    return redirect('shop:catalog')

@login_required
def profile(request):  
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Данные успешно обновлены!')
            return redirect('users:profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    
    return render(request, 'profile.html', {'form': form})