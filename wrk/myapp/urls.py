from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('signup/',views.signup,name='signup'),
    path('login/',views.login,name='login'),
    path('policy/',views.policy,name='policy'),
    path('change-password/',views.change_password,name='change-password'),
    path('logout/',views.logout,name='logout'),
]


