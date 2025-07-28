from django.contrib.auth import authenticate
from django.contrib.auth.models import User 
from rest_framework import serializers


class CustomEmailAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(detail='Invalid input the entered email or password is wrong!')
        user = authenticate(username=user.username, password=password)
        if not user:
            raise serializers.ValidationError(detail='Invalid input the entered email or password is wrong!')
        attrs['user'] = user
        return attrs