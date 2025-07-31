from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import CustomEmailAuthTokenSerializer



class LoginView(ObtainAuthToken):
    serializer_class = CustomEmailAuthTokenSerializer


    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response(data={"token": token.key, "fullname": user.customuser.fullname, "email": user.email, "user_id": user.id}, status=status.HTTP_200_OK)