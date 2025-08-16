from rest_framework import serializers
from django.contrib.auth.models import User
from boards_app.models import Board
from tasks_app.api.serializers import TaskListSerializer


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
       return obj.tasks.count()
    

    def get_tasks_to_do_count(self, obj):
       return obj.tasks.filter(status="to-do").count()
        

    def get_tasks_high_prio_count(self, obj):
        return obj.tasks.filter(priority="high").count()


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
       return obj.tasks.count()
    

    def get_tasks_to_do_count(self, obj):
        return obj.tasks.filter(status="to-do").count()


    def get_tasks_high_prio_count(self, obj):
        return obj.tasks.filter(priority="high").count()


class BoardMemberListSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()
    

    class Meta:
        model = User
        fields = ["id", "email", "fullname"]


    def get_fullname(self, obj):
        return obj.customuser.fullname


class BoardDetailSerializer(serializers.ModelSerializer):
    owner_id = serializers.PrimaryKeyRelatedField(read_only=True)
    members = BoardMemberListSerializer(many=True)
    tasks = TaskListSerializer(many=True)


    class Meta:
        model = Board
        fields = ["id", "title", "owner_id", "members", "tasks"]


class BoardUpdateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=False)
    members = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True, many=True, error_messages={"does_not_exist": "1 or more users dont exist!"})
    owner_data = BoardMemberListSerializer(source="owner_id", read_only=True)
    members_data = BoardMemberListSerializer(source="members", many=True, read_only=True)


    class Meta:
        model = Board
        fields = ["id", "title", "owner_data", "members_data", "members"]


    def validate_members(self, value):
        members = value
        if len(members) == 0:
            raise serializers.ValidationError("At least 1 member must be specified!")
        return value


    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        members = validated_data.get("members", instance.members)
        if members is not None:
            instance.members.set(members)
        instance.save()
        return instance