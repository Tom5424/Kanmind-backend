from django.urls import path
from .views import TaskCreateUpdateDeleteView, TaskAssignedToMeListView, TaskReviewingListView, CommentCreateListView


urlpatterns = [
    path("tasks/", TaskCreateUpdateDeleteView.as_view(), name="task-create-update-delete-view"),
    path("tasks/<int:task_id>/", TaskCreateUpdateDeleteView.as_view(), name="task-create-update-delete-view"),
    path("tasks/<int:task_id>/comments/", CommentCreateListView.as_view(), name="comment-create-list-view"),
    path("tasks/assigned-to-me/", TaskAssignedToMeListView.as_view(), name="tasks-assigned-to-me-list"),
    path("tasks/reviewing/", TaskReviewingListView.as_view(), name="tasks-reviewing-list"),
]