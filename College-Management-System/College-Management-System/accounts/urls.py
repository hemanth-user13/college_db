from django.urls import path
from . import views
from .views import show_teachers_rating, individual_rating


urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('student_login/', views.Student_login, name='Student_login'),
    path('student_signup/', views.student_signup, name='student_signup'),
    path('submit/', views.Stu_data, name='Stu_data'),
    path('loginv/', views.login_val, name='login_val'),
    path('teacherrating/<int:pk>/', views.teach_rating, name='teach_rating'),
    path('managerlogin/',views.manager_login,name='manager_login'),
    path('managerview/',views.manager_view,name='manager_view'),
    path('studentrating/', views.stu_rating, name='stu_rating'),
    path('forgetpassword/', views.forget_password, name='forget_password'),
    #path('student_rating/', views.student_rating, name='student_rating'),
    path('managerhome/', views.managerhome, name='managerhome'),
    path('show_rating/', views.show_teachers_rating, name='show_teachers_rating'),
    path('individualrating/<str:teacher>/', views.individual_rating, name='individual_rating'),
    path('piechart/', views.piechart, name='piechart'),
    path('upload/', views.upload_file, name='upload_file'),


]

