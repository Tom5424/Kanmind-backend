from django.urls import path, include
from .views import register_view


urlpatterns = [
    path('registration/', register_view, name='register-view'),
]