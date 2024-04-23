from django.contrib import admin
from django.urls import path,include
from .import views
from .views import register,login, index, admin_index  
from .admin import custom_admin_site 
from django.contrib.auth import views as auth_views
from .views import update
from .views import grade_quiz





urlpatterns = [
  
     path('', views.index, name='index'),
    # path('about/', views.about, name='about'),
    
    path('courses/', views.courses, name='courses'),
    path('course_view/', views.course_view, name='course_view'),
    path('course_userside/', views.course_userside, name='course_userside'),
   
    path('login/', views.login, name='login'),
   
    path('register/', views.register, name='register'),
  
    path('admin_index/', admin_index, name='admin_index'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('logout/',views.logout, name='logout'),
    path('edit/<slug:slug>/', views.edit, name='edit'),
    path('update/<int:id>/', views.update, name='update'),
    path('viewmore/<slug:slug>/', views.viewmore, name='viewmore'),
    path('viewmore1/<slug:slug>/', views.viewmore1, name='viewmore1'),
    path('viewmore2/<slug:slug>/', views.viewmore2, name='viewmore2'),
    path('admin_quiz/', views.admin_quiz, name='admin_quiz'),
    path('create_quizq/', views.create_quizq, name='create_quizq'),
    path('create_quiz_choice/', views.create_quiz_choice, name='create_quiz_choice'),
    path('quiz/', views.quiz, name='quiz'),
    path('quiz1/', views.quiz1, name='quiz1'),
    path('quiz2/', views.quiz2, name='quiz2'),
   
    path('grade/', grade_quiz, name='grade_quiz'),
    
   
   
   
   
 
    


   
]