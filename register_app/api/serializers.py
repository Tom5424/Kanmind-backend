from django.contrib.auth.models import User 
from rest_framework import serializers
from register_app.models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField() 
    repeated_password = serializers.CharField(min_length=10, write_only=True) 


    class Meta:
        model = User
        fields = ["fullname", "email", "password", "repeated_password"]


    def create(self, validated_data):
        validated_data.pop("repeated_password")
        fullname = validated_data.pop("fullname")
        email = validated_data["email"]
        username = email.split("@", 1)[0] ### Takes the letters before the @ sign and asssign it to the username
        validated_data["username"] = username
        user = User.objects.create_user(**validated_data)
        CustomUser.objects.create(user=user, fullname=fullname)
        return user