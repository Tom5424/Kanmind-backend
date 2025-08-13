from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from .serializers import TaskCreateListSerializer, TaskAssignedOrReviewingListSerializer 
from .permissions import IsBoardOwnerOrMember
from tasks_app.models import Task


class TaskCreateView(APIView):
    permission_classes = [IsAuthenticated, IsBoardOwnerOrMember]
    authentication_classes = [TokenAuthentication, SessionAuthentication]


    def post(self, request):
        serializer = TaskCreateListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    

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