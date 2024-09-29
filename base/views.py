from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
import json

from base.forms import UserCreationForm
from .models import User  # Import the User model

@csrf_exempt


def user(request):
    return render(request,'user.html')

def index(request):
    return render(request, 'index.html')


def category(request):
    return render(request,'category.html')

def login_view(request):
    return render(request, 'login.html') 
import json

def admin_login(request):
    print('work1')
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            print(f'Username: {username}, Password: {password}')  # Debugging line
            
            # Authenticate using custom User model
            user = User.objects.filter(username=username).first()  # Find the user by username
            
            if user is not None and user.password == password:  # Use custom password checking
                if user.role.id == 3:  # Check if user is an Admin
                    print('work3')
                    return JsonResponse({'success': True, 'redirect_url': '/category/'})
                else:
                    print('User is not an admin')  # Debugging line
                    return JsonResponse({'success': False, 'message': 'User is not an admin'})
            else:
                print('Invalid credentials')  # Debugging line
                # Print all users for debugging
                all_users = User.objects.all()
                print("All users in the database:")
                for user in all_users:
                    print(f'Username: {user.username}, Role: {user.role.name}')
                
                return JsonResponse({'success': False, 'message': 'Invalid credentials'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON data'})
    return JsonResponse({'success': False, 'message': 'Invalid request'})

def create_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user')  # Redirect to the user list or wherever you want
    else:
        form = UserCreationForm()
    return render(request, 'create_user.html', {'form': form})