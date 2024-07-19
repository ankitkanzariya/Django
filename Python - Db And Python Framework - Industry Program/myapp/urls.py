from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.login,name='login'),
    path('register/',views.register,name='register'),
    path('forget/',views.forget,name='forget'),
    path('index/',views.index,name='index'),
    path('logout/',views.logout,name='logout'),
    path('adminpanel/',views.adminpanel,name='adminpanel'),
    path('insurance_application/', views.insurance_application, name='insurance_application'),
    path('submit_question',views.submit_question,name='submit_question'),
]
