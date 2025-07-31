from rest_framework import serializers
from django.contrib.auth.models import User
from boards_app.models import Board


class BoardCreateSerializer(serializers.ModelSerializer):
    owner_id = serializers.PrimaryKeyRelatedField(read_only=True)
    members = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True, many=True, error_messages={"does_not_exist": "1 or more users dont exist!"})
    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()


    class Meta:
        model = Board
        fields = ["id", "title", "member_count", "ticket_count", "tasks_to_do_count", "tasks_high_prio_count", "owner_id", "members"]
    

    def get_member_count(self, obj):
        return obj.members.count()


    def get_ticket_count(self, obj):
        return 0
    

    def get_tasks_to_do_count(self, obj):
        return 0


    def get_tasks_high_prio_count(self, obj):
        return 0


    def create(self, validated_data):
        user = self.context["request"].user
        members = validated_data.pop("members")
        members.append(user)
        board = Board.objects.create(owner_id=user, **validated_data)
        board.members.set(members)
        return board
    


class BoardListSerializer(serializers.ModelSerializer):
    owner_id = serializers.PrimaryKeyRelatedField(read_only=True)
    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()


    class Meta:
        model = Board
        fields = ["id", "title", "member_count", "ticket_count", "tasks_to_do_count", "tasks_high_prio_count", "owner_id"]
    

    def get_member_count(self, obj):
        return obj.members.count()


    def get_ticket_count(self, obj):
        return 0
    

    def get_tasks_to_do_count(self, obj):
        return 0


    def get_tasks_high_prio_count(self, obj):
        return 0