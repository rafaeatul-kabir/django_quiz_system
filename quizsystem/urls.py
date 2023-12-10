from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name="home"),
    path('register', views.register, name="register"),
    path('login', views.login, name="login"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('logout', views.logout, name="logout"),
    path('quiz', views.get_questions, name="quiz"),
    path('submit_quiz', views.submit_quiz, name="submit_quiz"),
    path('result', views.result, name="result"),

]
