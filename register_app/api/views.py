from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer


class RegisterView(APIView):
   """Create a new user."""
   

   def post(self, request):
      """Create a new user."""
      serializer = RegisterSerializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      user = serializer.save()
      token, created = Token.objects.get_or_create(user=user)
      return Response(data={"token": token.key, "fullname": user.customuser.fullname, "email": user.email, "user_id": user.id}, status=status.HTTP_201_CREATED)