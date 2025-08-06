from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .serializers import BoardCreateSerializer, BoardListSerializer, BoardDetailSerializer
from .permissions import IsBoardOwnerOrMember
from boards_app.models import Board


class BoardListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]


    def get(self, request):
        user = request.user
        boards = Board.objects.filter(Q(owner_id=user.id) | Q(members=user)).distinct()
        serializer = BoardListSerializer(boards, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        serializer = BoardCreateSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    

class BoardDetailView(APIView):
    permission_classes = [IsAuthenticated, IsBoardOwnerOrMember]
    authentication_classes = [TokenAuthentication, SessionAuthentication]


    def get(self, request, board_id):
        board = get_object_or_404(Board, id=board_id)
        self.check_object_permissions(request=request, obj=board)
        serializer = BoardDetailSerializer(board)
        return Response(data=serializer.data, status=status.HTTP_200_OK)