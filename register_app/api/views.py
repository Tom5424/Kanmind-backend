from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer


@api_view(["POST"])
def register_view(request):
   serializer = RegisterSerializer(data=request.data)
   if serializer.is_valid():
      user = serializer.save()
      token, created = Token.objects.get_or_create(user=user)
      return Response(data={"token": token.key, "fullname": user.customuser.fullname, "email": user.email, "user_id": user.id}, status=status.HTTP_201_CREATED)
   return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)