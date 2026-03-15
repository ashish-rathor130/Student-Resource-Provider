from django.urls import path
from . import views

urlpatterns = [
   path('', views.home, name='home'),
   path('register/', views.register, name='register'),
   path('verify_otp/<int:user_id>/', views.verify_user_otp, name='verify_otp'),
   path('resend_otp/<int:user_id>/', views.resend_otp, name='resend_otp'),
   path('login/', views.user_login, name='login'),
   path('logout/', views.user_logout, name='logout'),
   path("reset_password/",views.reset_password_view,name="reset_password"),
   path("change_password/",views.change_password_view,name="change_password"),
   path("profile/<int:user_id>/",views.profile,name="profile"),
   path("about-us/",views.about_us, name ="about"),
   path("notes/<str:sem_id>/",views.notes, name ="notes"),
   path("units/<str:sub_id>/",views.all_units, name ="units"),
   path("papers/",views.papers, name ="papers"),
   
   path('course/upload/', views.upload_course, name='upload_course'),
   path('semester/upload/', views.upload_semester, name='upload_semester'),
   path('subject/upload/<str:sem_id>/', views.upload_subject, name='upload_subject'),
   path('unit/upload/<str:sub_id>/', views.upload_unit, name='upload_unit'),
   path('note/upload/', views.upload_note, name='upload_note'),
]