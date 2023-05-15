from django.contrib.auth.models import User
from django.db import models
# Create your models here.
class Quizgo(models.Model):
    quiz_name = models.CharField(max_length=50,help_text="The name of quiz")
    quiz_code = models.IntegerField(help_text="The code to join")
    quiz_description = models.TextField()
    quiz_photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)

    def __str__(self):
        return self.quiz_name

class Question(models.Model):
    quiz = models.ForeignKey(Quizgo, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=200, verbose_name=('Question'))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.question.text

class Player(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=255)
    quiz = models.ForeignKey(Quizgo, on_delete=models.CASCADE, related_name='players')
    results = models.IntegerField(default=0)

    def __str__(self):
        return self.name.username


