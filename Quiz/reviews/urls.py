from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from .views import *

urlpatterns = [
                  path('kahoot', kahoot),
                  path('', main, name="main"),
                  path('details/<int:id>/', details, name="details_quiz"),
                  path('details/<int:id>/change/', change, name="change"),
                  path('change', change, name='change'),
                  path('addQuiz', addQuiz, name='addQuiz'),
                  path('search', search, name='search'),
                  path('search', search, name='searchko'),
                  path('play/<int:id>/', play, name='play'),
                  path('question/<int:id>/<int:p_id>/<int:question_number>/', question, name='question'),
                  path('gameover/<int:id>/<int:p_id>/<int:question_number>/', gameover, name='gameover'),
                  path('register/', register, name='register'),
                  path('join/<int:id>', join, name='join'),
                  path('info/', info, name='info'),
                  path('quick', quick, name='quick'),
                  path('upR', upR, name='upR'),
                  path('addQuestion/<int:id>', addQuestion, name='addQuestion'),
                  path('addQuestion/<int:id>/add', addQuestionAdd, name='addQuestionAdd'),
                  path('results/', results, name='results'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)