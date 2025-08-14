from django.urls import path
from .views import TaskCreateUpdateView, TaskAssignedToMeListView, TaskReviewingListView 


urlpatterns = [
    path("tasks/", TaskCreateUpdateView.as_view(), name="task-create-update-view"),
    path("tasks/<int:task_id>/", TaskCreateUpdateView.as_view(), name="task-create-update-view"),
    path("tasks/assigned-to-me/", TaskAssignedToMeListView.as_view(), name="tasks-assigned-to-me-list"),
    path("tasks/reviewing/", TaskReviewingListView.as_view(), name="tasks-reviewing-list"),
]