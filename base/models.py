from django.db import models

class Role(models.Model):
    ROLE_CHOICES = [
        (1, 'Student'),
        (2, 'Teacher'),
        (3, 'Admin'),
    ]
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, choices=ROLE_CHOICES, unique=True)

    def __str__(self):
        return self.name


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    password = models.CharField(max_length=100, blank=True, null=True)  

    def __str__(self):
        return self.username


class Feedback(models.Model):
    student_name = models.CharField(max_length=100)
    time_taken = models.DurationField()  
    score = models.IntegerField()

    def __str__(self):
        return f"{self.student_name} - Score: {self.score}"


class Game(models.Model):
    game_type = models.CharField(max_length=100)
    questions = models.JSONField() 
    answers = models.JSONField()  

    def __str__(self):
        return self.game_type
