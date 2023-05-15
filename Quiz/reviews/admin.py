from django.contrib import admin

from .models import Quizgo, Question, Choice, Player

# Register your models here.

admin.site.register(Quizgo)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Player)

