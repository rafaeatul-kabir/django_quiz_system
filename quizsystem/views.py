import random
from django.shortcuts import render, redirect, reverse
from . forms import CreateUserForm, UserLoginForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from . customdecorator import not_logged_in_redirect 
from . import models

def homepage(request):
    return render(request, 'home.html')

@not_logged_in_redirect('dashboard')
def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    context = { 'registrationForm' : form}
    return render(request, 'register.html', context=context)

@not_logged_in_redirect('dashboard')
def login(request):
    form = UserLoginForm
    if request.method=="POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect("dashboard")

    context = {'loginForm': form}
    return render(request, 'login.html', context=context)

@login_required(login_url="login")
def dashboard(request):
    #getting the topics
    topics = models.Topic.objects.all()
    # getting user's quiz records'
    user_record = models.UserRecord.objects.filter(user=request.user)
    context = {
        'user': request.user,
        'quizes': user_record,
        'topics': topics
    }
    return render(request, 'dashboard.html', context=context)

@login_required(login_url="login")
def logout(request):
    auth.logout(request)
    return redirect("home")

@login_required(login_url="login")
def get_questions(request):
    if request.method == 'POST':
        selected_topic_ids = request.POST.getlist('selected_topics')
        selected_topics = models.Topic.objects.filter(id__in=selected_topic_ids)

        # Query questions related to selected topics
        related_questions = models.Question.objects.filter(topic__in=selected_topics)
        random_questions = random.sample(list(related_questions), min(5, len(related_questions)))
        context = {'questions': random_questions}
        return render(request, "quiz.html", context=context)

@login_required(login_url="login")
def submit_quiz(request):
    if request.method == 'POST':
        selected_options = {key: value for key, value in request.POST.items() if key.startswith('option_q')}
        print(selected_options)
        attempts_list = []
        user = request.user
        score =0
        for key,value in selected_options.items():
            question_id = key.replace("option_q", "")
            if "option_q" in value:
                chosen_option=""
            else:
                chosen_option = value
            question = models.Question.objects.get(pk=question_id)
            attempt = models.UserQuestionAttempt(user=user, question=question, chosen_option=chosen_option)
            attempt.save()
            score+=int(attempt.is_correct)
            attempts_list.append(attempt)
        user_record = models.UserRecord.objects.create(user=user)
        user_record.save()
        user_record.attempts.set(attempts_list)
        user_record.score = score
        user_record.save()
        return redirect(reverse('result', kwargs={'quiz_id': user_record.id}))

@login_required(login_url="login")
def result(request, quiz_id):
    user = request.user
    last_user_record = models.UserRecord.objects.get(pk=quiz_id)
    context = {'last_user_record': last_user_record}
    return render(request, 'result.html', context=context)

