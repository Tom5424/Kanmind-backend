from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from django.shortcuts import get_object_or_404
from .serializers import TaskCreateSerializer, TaskUpdateSerializer, TaskAssignedOrReviewingListSerializer, CommentCreateListSerializer 
from .permissions import IsBoardOwnerOrMember, IsBoardOwnerOrTaskCreator, IsCommentCreator
from tasks_app.models import Task, Comment


class TaskCreateUpdateDeleteView(APIView):
    """Create, update and delete tasks within a board."""
    

    permission_classes = [IsAuthenticated, IsBoardOwnerOrMember]
    authentication_classes = [TokenAuthentication, SessionAuthentication]


    def get_permissions(self):
        """Return the appropriate permission classes based on request method."""
        if self.request.method == "DELETE":
            return [IsAuthenticated(), IsBoardOwnerOrTaskCreator()]
        return [IsAuthenticated(), IsBoardOwnerOrMember()]


    def post(self, request):
        """Create a new task."""
        serializer = TaskCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


    def patch(self, request, task_id):
        """Partially update an existing task."""
        task = get_object_or_404(Task, id=task_id)
        self.check_object_permissions(request=request, obj=task)
        serializer = TaskUpdateSerializer(task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    

    def delete(self, request, task_id):
        """Delete an existing task."""
        task = get_object_or_404(Task, id=task_id)
        self.check_object_permissions(request=request, obj=task)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentCreateListView(APIView):
    """Create, and list comments within a task."""


    permission_classes = [IsAuthenticated, IsBoardOwnerOrMember]
    authentication_classes = [TokenAuthentication, SessionAuthentication]


    def get(self, request, task_id):
        """Get list of comments within a task."""
        task = get_object_or_404(Task, id=task_id)
        comments = task.comments.order_by("created_at")
        self.check_object_permissions(request=request, obj=task)
        serializer = CommentCreateListSerializer(comments, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


    def post(self, request, task_id):
        """Create a comment within a task."""
        user = request.user
        task = get_object_or_404(Task, id=task_id)
        self.check_object_permissions(request=request, obj=task)
        serializer = CommentCreateListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=user, task=task)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class CommentDeleteView(APIView):
    """Delete a comment within a task."""


    permission_classes = [IsAuthenticated, IsCommentCreator]
    authentication_classes = [TokenAuthentication, SessionAuthentication]


    def delete(self, request, task_id, comment_id):
        """Delete a comment within a task."""
        get_object_or_404(Task, id=task_id)
        comment = get_object_or_404(Comment, id=comment_id)
        self.check_object_permissions(request=request, obj=comment)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskAssignedToMeListView(APIView):
    """Get a list tasks where the authenticated user is assignee."""


    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]


    def get(self, request):
        """Get a list tasks where the authenticated user is assignee."""
        user = request.user
        tasks = Task.objects.filter(assignee_id=user.id)
        serializer = TaskAssignedOrReviewingListSerializer(tasks, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class TaskReviewingListView(APIView):
    """Get a list tasks where the authenticated user is reviewer."""


    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]


    def get(self, request):
        """Get a list tasks where the authenticated user is reviewer."""
        user = request.user
        tasks = Task.objects.filter(reviewer_id=user.id)
        serializer = TaskAssignedOrReviewingListSerializer(tasks, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)            