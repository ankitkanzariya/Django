from django.urls import path
from . import views

urlpatterns = [
     path('',views.index,name='index'),
     path('signup/',views.signup,name='signup'),
     path('login/',views.login,name='login'),
     path('logout/',views.logout,name='logout'),
     path('add-medicine/',views.add_medicine,name='add-medicine'),
     path('medicines/',views.medicines,name='medicines'),
     path('view-medicines/',views.view_medicines,name='view-medicines'),
     path('delete/<int:pk>/', views.delete, name='delete'),
     path('edit/<int:pk>/', views.edit, name='edit'),
     # path('delete/',views.delete,name='delete'),
]
