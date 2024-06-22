from django.contrib import admin
from django.urls import path
from myapp.views import StudentList,StudentDetail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/students',StudentList.as_view()),
    path('api/students/<int:pk>',StudentDetail.as_view()),
    
]
