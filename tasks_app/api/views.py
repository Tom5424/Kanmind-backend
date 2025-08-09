# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.authentication import TokenAuthentication, SessionAuthentication
# from rest_framework.exceptions import ValidationError, NotFound
# from django.contrib.auth.models import User
# from django.core.exceptions import ValidationError as DjangoValidationError
# from django.core.validators import validate_email
# from .serializers import UserEmailAndFullnameSerializer


# class EmailCheckView(APIView):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [TokenAuthentication, SessionAuthentication]


#     def get(self, request):
#         email = request.query_params.get("email")
#         if not email:
#             raise ValidationError({"email": "The email is missing!"})
#         try:
#             validate_email(email)
#             user = User.objects.get(email=email)
#         except DjangoValidationError:
#             raise ValidationError({"email": "Invalid email!"})
#         except User.DoesNotExist:
#             raise NotFound({"email": "The email dont exist!"})
#         serializer = UserEmailAndFullnameSerializer(user)
#         return Response(data=serializer.data, status=status.HTTP_200_OK)