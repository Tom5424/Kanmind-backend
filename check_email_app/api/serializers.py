from rest_framework import serializers
from django.contrib.auth.models import User


class UserEmailAndFullnameSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()


    class Meta:
        model = User
        fields = ["id", "email", "fullname"]
    

    def get_fullname(self, obj):
        return obj.customuser.fullname