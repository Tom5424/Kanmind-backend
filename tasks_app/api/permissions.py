from rest_framework.permissions import BasePermission
from django.shortcuts import get_object_or_404
from boards_app.models import Board 
from tasks_app.models import Task


class IsBoardOwnerOrMember(BasePermission):


    def get_board(self, request, view):
        task_id = view.kwargs.get('task_id')
        if task_id:
            task = get_object_or_404(Task, id=task_id)
            return task.board
        board_id = request.data.get('board')
        if board_id:
            return get_object_or_404(Board, id=board_id)
        return None


    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        board = self.get_board(request, view)
        if not board:
            return False
        return board.owner_id_id == request.user.id or request.user in board.members.all()
    

    def has_object_permission(self, request, view, obj):
        if request.method in ['POST', 'PATCH', 'PUT', 'DELETE']:
            board = obj.board
            return board.owner_id_id == request.user.id or request.user in board.members.all()


class IsBoardOwnerOrTaskCreator(BasePermission):
    

    def has_object_permission(self, request, view, obj):
        board = obj.board
        creator_id = obj.creator_id
        return board.owner_id_id == request.user.id or request.user.id == creator_id