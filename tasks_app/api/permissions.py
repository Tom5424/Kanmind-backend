from rest_framework.permissions import BasePermission
from django.shortcuts import get_object_or_404
from boards_app.models import Board 


class IsBoardOwnerOrMember(BasePermission):
    

    def has_permission(self, request, view):
        if request.method == 'POST':
            board_id = request.data.get('board')
            board = get_object_or_404(Board, id=board_id)
            return board.owner_id_id == request.user.id or request.user in board.members.all()