from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('add-student/',views.add_student,name='add-student'),
    path('add-to-student/',views.add_to_student,name='add-to-student'),
    path('view-student/',views.view_student,name='view-student'),
    path('delete/<int:pk>/', views.delete, name='delete'),
    path('edit/<int:pk>/', views.edit, name='edit'),
    path('edit-student/<int:pk>/', views.edit_student, name='edit-student'),

]

