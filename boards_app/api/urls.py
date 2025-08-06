from django.urls import path
from .views import BoardListCreateView, BoardDetailView 


urlpatterns = [
    path("boards/", BoardListCreateView.as_view(), name="boards-list-create-view"),
    path("boards/<int:board_id>/", BoardDetailView.as_view(), name="board-detail-view"),
]