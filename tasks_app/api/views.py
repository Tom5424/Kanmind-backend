from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from django.shortcuts import get_object_or_404
from .serializers import TaskCreateSerializer, TaskUpdateSerializer, TaskAssignedOrReviewingListSerializer 
from .permissions import IsBoardOwnerOrMember, IsBoardOwnerOrTaskCreator
from tasks_app.models import Task


class TaskCreateUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsBoardOwnerOrMember]
    authentication_classes = [TokenAuthentication, SessionAuthentication]


    def get_permissions(self):
        if self.request.method == "DELETE":
            return [IsAuthenticated(), IsBoardOwnerOrTaskCreator()]
        return [IsAuthenticated(), IsBoardOwnerOrMember()]


    def post(self, request):
        serializer = TaskCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


    def patch(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        self.check_object_permissions(request=request, obj=task)
        serializer = TaskUpdateSerializer(task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    

    def delete(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        self.check_object_permissions(request=request, obj=task)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskAssignedToMeListView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]


    def get(self, request):
        user = request.user
        tasks = Task.objects.filter(assignee_id=user.id)
        serializer = TaskAssignedOrReviewingListSerializer(tasks, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class TaskReviewingListView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]


    def get(self, request):
        user = request.user
        tasks = Task.objects.filter(reviewer_id=user.id)
        serializer = TaskAssignedOrReviewingListSerializer(tasks, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)            