from rest_framework.permissions import BasePermission
from django.shortcuts import get_object_or_404
from boards_app.models import Board 


class IsBoardOwnerOrMember(BasePermission):
    

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        if request.method == 'POST':
            board_id = request.data.get('board')
            if not board_id:
                return False 
            board = get_object_or_404(Board, id=board_id)
            return board.owner_id_id == request.user.id or request.user in board.members.all()
        return True
    

    def has_object_permission(self, request, view, obj):
        if request.method in ['PATCH', 'PUT', 'DELETE']:
            board = obj.board
            return board.owner_id_id == request.user.id or request.user in board.members.all()