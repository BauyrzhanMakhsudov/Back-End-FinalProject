import random

from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Quizgo, Question, Choice, Player, User
from .forms import QuizgoSearchForm, ClientRegistrationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.conf import settings


def main(request):
    quizs = Quizgo.objects.all()
    arr = []
    for quiz in quizs:
        arr.append({"id": quiz.id, "url": quiz.quiz_photo.url})
    form = QuizgoSearchForm()
    context = {
        "quizs": quizs,
        "q": arr,
        "form": form
    }

    return render(request, "main.html",context)

def details(request, id):
    quiz = Quizgo.objects.get(id=id)
    form = QuizgoSearchForm()
    context = {
        "quiz_id": id,
        "quiz": quiz,
        "form": form
    }
    return render(request, "quiz.html", context)

def change(request):
    quiz_id = request.POST['quiz_id']
    form = QuizgoSearchForm()
    if(request.method == 'POST'):
        if 'save' in request.POST:
            quiz_id = request.POST['quiz_id']
            quiz_name = request.POST['quiz_name']
            quiz_code = request.POST['quiz_code']
            quiz_description = request.POST['quiz_description']
            quiz_photo = None

            quiz = Quizgo.objects.get(id=quiz_id)
            quiz.quiz_name = quiz_name
            quiz.quiz_code = quiz_code
            quiz.quiz_description = quiz_description
            if 'quiz_photo' in request.FILES and request.FILES['quiz_photo']:
                quiz_photo = request.FILES['quiz_photo']
                quiz.quiz_photo = quiz_photo

            quiz.save()
        elif 'delete' in request.POST:
            quiz = get_object_or_404(Quizgo, pk=quiz_id)
            quiz.delete()

        quizs = Quizgo.objects.all()
        arr = []
        for q in quizs:
            arr.append({"id": q.id, "url": q.quiz_photo.url})

        context = {
            "quizs": quizs,
            "q": arr,
            "form": form
        }

        return render(request, 'main.html', context)

    return render(request, "main.html")

from django.db.models import Q

def search(request):
    if request.method == 'GET':
        search_query = request.GET.get('search', '')
        print(str(search_query))
        if search_query and not search_query.isspace():
            results = Quizgo.objects.filter(
                Q(quiz_name__icontains=search_query) |
                Q(quiz_code__icontains=search_query)
            )
        else:
            results = Quizgo.objects.none()

        form = QuizgoSearchForm()
        context = {
            "quizs": results,
            "form": form,
            "c": 1
        }

        return render(request, "main.html", context)




def addQuiz(request):
    form = QuizgoSearchForm()
    if(request.method == 'POST'):
        quiz_name = request.POST['quiz_name']
        quiz_code = request.POST['quiz_code']
        quiz_description = request.POST['quiz_description']
        quiz_photo = None

        quiz = Quizgo(quiz_name=quiz_name, quiz_code=quiz_code, quiz_description=quiz_description)
        if 'quiz_photo' in request.FILES and request.FILES['quiz_photo']:
            quiz.quiz_photo = request.FILES['quiz_photo']

        quiz.save()

        return redirect('/')

def play(request, id):
    quiz = get_object_or_404(Quizgo, id=id)
    questions = Question.objects.filter(quiz=quiz)
    question = questions[0]
    choices = question.choice_set.all()
    answer_options = [choice.text for choice in choices]
    random.shuffle(answer_options)
    question_answers = [(question.text, answer_options)]
    length = len(question_answers)
    context = {
        "question_answers": question_answers,
        "q": 0,
        "q_id": id,
        "length": length
    }
    return render(request, 'kahoot.html', context)

def kahoot(request):
    return render(request, 'kahoot.html')

def question(request, id, p_id, question_number):
    quiz = get_object_or_404(Quizgo, id=id)
    questions = Question.objects.filter(quiz=quiz)
    
    if question_number >= len(questions):
            return HttpResponse("Quiz completed")

    question = questions[question_number]
    choices = question.choice_set.all()
    answer_options = [choice.text for choice in choices]
    random.shuffle(answer_options)
    question_answers = [(question.text, answer_options)]
    correct_answer = next((choice.text for choice in choices if choice.is_correct), None)
    player = Player.objects.filter(id=p_id).first()
    
    context = {
        "question_answers": question_answers,
        "length": len(questions),
        "q": question_number + 1,
        "q_id": id,
        "correct_answer": correct_answer,
        "player_id": p_id,
        "question_id": question.id,
        "name": player.name.username
    }
    
    return render(request, 'kahoot.html', context)


def gameover(request, id, p_id, question_number):
    player = Player.objects.get(id=p_id)
    quiz = Quizgo.objects.get(id=id)
    answers = Question.objects.filter(quiz=quiz)
    question_answers = []
    for answer in answers:
        choices = answer.choice_set.all()
        answer_options = [choice.text for choice in choices]
        correct_answer = next((choice.text for choice in choices if choice.is_correct), None)
        question_answer = (answer.text, answer_options, correct_answer)
        question_answers.append(question_answer)
    context = {
        "quiz_id": id,
        "player_id": p_id,
        "player": player,
        "quiz": quiz,
        "answers": question_answers,
    }
    return render(request, 'bitti.html', context)

def profile(request):
    return render(request, 'profile.html')

def info(request):
    return render(request, "info.html")

@login_required
def join(request, id):
    context = {
        "id": id
    }
    return render(request, "join.html", context)
def quick(request):
    if(request.method == 'GET'):
        name = request.GET.get("username")
        nickname = request.GET.get("nickname")
        quiz_id = request.GET.get("quiz_id")
        user = User.objects.get(username=name)
        quiz = Quizgo.objects.get(id=quiz_id)
        context = {
            "quiz_id": id,
            "name":name,
            "nickname":nickname,
            "quiz_id": quiz_id
        }
        try:
            player = Player.objects.get(name=user, quiz=quiz)
            player.nickname = nickname
            player.save()
        except Player.DoesNotExist:
            player = Player.objects.create(
                name = user,
                nickname=nickname,
                quiz= quiz,
                results=0
            )
        context.update({"player_id": player.id})
    return render(request, "quick.html", context)
def register(request):
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = False
            user.save()
            login(request, user)
            return redirect('/')
    else:
        form = ClientRegistrationForm()
    return render(request, 'registration/client_registration.html', {'form': form})

def reset_password(request):
    return render(request, "main.html")

def upR(request):
    if request.method == 'GET':
        correct = int(request.GET.get("correct", 0))
        incorrect = int(request.GET.get("incorrect", 0))
        player_id = request.GET.get("player_id")
        quiz_id = request.GET.get("quiz_id")
        quiz = Quizgo.objects.get(id=quiz_id)


        length = correct + incorrect
        percent = correct * 100 / length

        player = Player.objects.get(id=player_id)

        player.results = percent
        player.save()

        quizs = Quizgo.objects.all()
        arr = []
        for quiz in quizs:
            arr.append({"id": quiz.id, "url": quiz.quiz_photo.url})
        form = QuizgoSearchForm()
        context = {
            "quizs": quizs,
            "q": arr,
            "form": form
        }

        subject = "Your quiz result"
        message = "Your quiz result about " + quiz.quiz_name + ", nickname: " + player.nickname + "\n" + "Correct answers: " + str(correct) + ", " \
                                                                                                                                         "Incorrect answers: " + str(incorrect) + "\n" + "Total: " + str(percent)
        email_from = settings.EMAIL_HOST_USER
        user = User.objects.get(username=player.name)
        recipient_list = [user.email]
        send_mail( subject, message, email_from, recipient_list)

        return render(request, "main.html", context)

def addQuestion(request, id):
    quiz = Quizgo.objects.get(id=id)
    questions = Question.objects.filter(quiz=quiz)
    question_answers = []
    form = QuizgoSearchForm()
    for question in questions:
        choices = question.choice_set.all()
        answer_options = [choice.text for choice in choices]
        question_answer = (question.text, answer_options)
        question_answers.append(question_answer)

    context = {
        "quiz_id": id,
        "question_answers": question_answers,
        "form":form
    }
    return render(request, "addQuestion.html", context)

def addQuestionAdd(request, id):
    if request.method == 'POST':
        # Retrieve GET parameters
        question_text = request.POST["question"]
        option_1 = request.POST["option1"]
        option_2 = request.POST["option2"]
        option_3 = request.POST["option3"]
        option_4 = request.POST["option4"]

        # Check if question text is empty
        if not question_text:
            return HttpResponse("Question text cannot be empty")

        # Create objects and save to database
        quiz = Quizgo.objects.get(id=id)
        question = Question.objects.create(quiz=quiz, text=question_text)
        choice1 = Choice.objects.create(question=question, text=option_1, is_correct=True)
        choice2 = Choice.objects.create(question=question, text=option_2, is_correct=False)
        choice3 = Choice.objects.create(question=question, text=option_3, is_correct=False)
        choice4 = Choice.objects.create(question=question, text=option_4, is_correct=False)
        question.save()
        choice1.save()
        choice2.save()
        choice3.save()
        choice4.save()

        return redirect("/")

@login_required
def results(request):
    try:
        if request.user.is_staff:
            players = Player.objects.all()
        else:
            players = Player.objects.filter(name=request.user)

        players_list = [{"player": player} for player in players]

        if request.user.is_staff:
            context = {"players_list": players_list}
        else:
            context = {"players_list": players_list}

    except Player.DoesNotExist:
        context = {"error": "You have no quiz results yet."}

    return render(request, 'results.html', context)

