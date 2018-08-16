# Django
from django.urls import path
# Project
from . import views


urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
]
