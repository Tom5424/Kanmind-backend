import re
from django.contrib.auth import authenticate
from django.contrib.auth.models import User 
from rest_framework import serializers
from auth_app.models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField() 
    repeated_password = serializers.CharField(write_only=True) 


    class Meta:
        model = User
        fields = ["fullname", "email", "password", "repeated_password"]


    def validate_fullname(self, value):
        pattern = r"^[a-zäöüß]+(?: [a-zäöüß]+){1,2}$"
        if not re.match(pattern, value, re.IGNORECASE):
            raise serializers.ValidationError(detail="Enter your full name (e.g., Max Mustermann).")
        return value
        

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(detail="A user with this email already exist!")
        return value


    def validate_password(self, value):
        if len(value.strip()) < 8:
            raise serializers.ValidationError(detail="Password must at least 8 characters long!")
        return value.strip()    


    def validate(self, attrs):
        if attrs["password"] != attrs["repeated_password"]:
            raise serializers.ValidationError(detail="Passwords must match!")
        return attrs


    def create(self, validated_data):
        validated_data.pop("repeated_password")
        fullname = validated_data.pop("fullname")
        email = validated_data["email"]
        username = email.split("@", 1)[0] ### Takes the letters before the @ sign and asssign it to the username
        validated_data["username"] = username
        user = User.objects.create_user(**validated_data)
        CustomUser.objects.create(user=user, fullname=fullname)
        return user
    

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