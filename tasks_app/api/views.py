from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from .serializers import TaskCreateListSerializer
from .permissions import IsBoardOwnerOrMember


class TaskCreateView(APIView):
    permission_classes = [IsAuthenticated, IsBoardOwnerOrMember]
    authentication_classes = [TokenAuthentication, SessionAuthentication]


    def post(self, request):
        serializer = TaskCreateListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)