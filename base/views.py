from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render, get_object_or_404
import random
from base.forms import UserCreationForm
from .models import Feedback, Game, User  

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
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            print(f'Username: {username}, Password: {password}')  # Debugging line
            
            # Authenticate using custom User model
            user = User.objects.filter(username=username).first()  # Find the user by username
            
            if user is not None and user.password == password:   # Use Django's password checking
                if user.role.id == 3:  # Check if user is an Admin
                    print('Admin login successful')  # Debugging line
                    return JsonResponse({'success': True, 'redirect_url': '/create-user/'})  # Redirect to create_user.html
                elif user.role.id == 2:  # Check if user is a different role (e.g., staff)
                    print('Staff login successful')  # Debugging line
                    return JsonResponse({'success': True, 'redirect_url': '/teachers_panel'})  # Example redirect
                else:
                    print('User is not an admin or staff')  # Debugging line
                    return JsonResponse({'success': False, 'message': 'User is not authorized'})
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
            return redirect('success_url')  
    else:
        form = UserCreationForm()  

    return render(request, 'create_user.html', {'form': form})


def game_view(request):
    if request.method == 'POST':
        student_name = request.POST.get('studentName', None)
        
        if student_name:
            print(f"Received student name: {student_name}")
            return render(request, 'game_view.html', {'student_name': student_name})
        else:
            return HttpResponse("No student name provided", status=400)
    
    return render(request, 'game_view.html')


def game_panel(request, game_type):
    game = get_object_or_404(Game, game_type=game_type.capitalize())

    # Define mock answers for each question
    mock_answers = {
        1: ["6", "37", "9"],  # Mock answers for question 1
        2: ["15", "26", "20"],  # Mock answers for question 2
        3: ["14", "12", "30"],  # Mock answers for question 3
    }

    questions = game.questions
    for question in questions:
        question_id = question['id']
        correct_answer = game.answers[question_id - 1]  # Assuming answers are in the same order as questions
        options = list(set([correct_answer] + mock_answers[question_id]))  # Ensure unique options
        random.shuffle(options)
        question['options'] = options

    if request.method == 'POST':
        user_answers = []
        feedback = []

        # Collect user answers based on unique question identifiers
        for question in questions:
            question_id = question['id']
            user_answer = request.POST.get(f'answers_{game.id}_{question_id}', None)  # Default to None if not found
            user_answers.append(user_answer)

            # Compare user answer with the correct answer
            correct_answer = game.answers[question_id - 1]
            if user_answer is None:
                feedback.append(f"Question {question_id}: Not answered.")
            elif user_answer == correct_answer:
                feedback.append(f"Question {question_id}: Correct!")
            else:
                feedback.append(f"Question {question_id}: Incorrect. The correct answer is {correct_answer}.")

        print("User's answers:", user_answers)

        return render(request, 'game_panel.html', {
            'game': game,
            'feedback': feedback,
            'user_answers': user_answers,
            'questions': questions,
        })

    return render(request, 'game_panel.html', {'game': game, 'questions': questions})

def teachers_panel(request):
    feedback_list = Feedback.objects.all()  
    return render(request, 'teachers_panel.html', {'feedback_list': feedback_list})