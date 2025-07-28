from django.urls import path
from .views import LoginView
from rest_framework.authtoken import views


urlpatterns = [
    path('login/', LoginView.as_view(), name='login-view'),
]