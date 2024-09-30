from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
import json

from base.forms import UserCreationForm
from .models import Game, User  # Import the User model

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


def game_view(request):
    if request.method == 'POST':
        # Access the form data from the POST request
        student_name = request.POST.get('studentName', None)
        
        if student_name:
            print(f"Received student name: {student_name}")
            # Process the data and render the template
            return render(request, 'game_view.html', {'student_name': student_name})
        else:
            return HttpResponse("No student name provided", status=400)
    
    return render(request, 'game_view.html')


def game_panel(request, game_type):
    # Fetch the game based on the selected game_type
    game = get_object_or_404(Game, game_type=game_type.capitalize())

    if request.method == 'POST':
        # Retrieve user answers from form submission
        user_answers = request.POST.getlist('answers')
        print(user_answers)
        correct_answers = game.answers
        feedback = []

        # Verify answers
        for i, (user_answer, correct_answer) in enumerate(zip(user_answers, correct_answers)):
            if user_answer.strip().lower() == correct_answer.lower():
                feedback.append(f"Question {i+1}: Correct!")
            else:
                feedback.append(f"Question {i+1}: Incorrect. The correct answer is {correct_answer}.")

        return render(request, 'game_panel.html', {
            'game': game,
            'feedback': feedback,
            'user_answers': user_answers,
        })

    return render(request, 'game_panel.html', {'game': game})