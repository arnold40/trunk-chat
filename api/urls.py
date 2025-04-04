from django.urls import path
from . import views

urlpatterns = [
    path('vegetarian/', views.vegetarian_users),
]
