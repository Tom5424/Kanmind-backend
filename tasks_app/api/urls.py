from django.urls import path
from .views import TaskCreateView, TaskAssignedToMeListView, TaskReviewingListView 


urlpatterns = [
    path("tasks/", TaskCreateView.as_view(), name="task-create-view"),
    path("tasks/assigned-to-me/", TaskAssignedToMeListView.as_view(), name="tasks-assigned-to-me-list"),
    path("tasks/reviewing/", TaskReviewingListView.as_view(), name="tasks-reviewing-list"),
]