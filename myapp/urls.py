from django.urls import path

from . import views

urlpatterns = [
    path('/', views.index, name='index'),
    path('/profile', views.profile, name='profile'),
    path('/home', views.home, name='home'),
    path('/quiz', views.quiz, name='quiz'),
    path('/quiz/<str:lang>', views.questions, name='questions'),# remove - if there is an error occurs while database connecticity
    path('/contest', views.contest, name='contest'),
    path('/contest/<int:problem_id>', views.problem, name='problem'),
    path('/code/<int:problem_id>', views.code, name='code'),
    path('/login', views.login_view, name='login'),
    path('/signup', views.signup, name='signup'),
    path('/logout', views.logout_view, name='logout'),
   
]