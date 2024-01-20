from django.urls import path
from . import views

urlpatterns = [
    path('students/', views.getAll),
    path('students/<id>', views.getOne),
]