from django.urls import path
from .views import TaskCreateView, TaskAssignedToMeListView 


urlpatterns = [
    path("tasks/", TaskCreateView.as_view(), name="task-create-view"),
    path("tasks/assigned-to-me/", TaskAssignedToMeListView.as_view(), name="tasks-assigned-to-me-list"),
]