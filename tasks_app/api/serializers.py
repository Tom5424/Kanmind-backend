from rest_framework import serializers
from django.contrib.auth.models import User
from tasks_app.models import Task
from boards_app.models import Board
from tasks_app.choices import priority, status


class TaskAssigneeAndReviewerSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()


    class Meta:
        model = User
        fields = ["id", "email", "fullname"]


    def get_fullname(self, obj):
        return obj.customuser.fullname


class TaskListSerializer(serializers.ModelSerializer):
    assignee = TaskAssigneeAndReviewerSerializer(source="assignee_id", read_only=True)
    reviewer = TaskAssigneeAndReviewerSerializer(source="reviewer_id", read_only=True)
    comments_count = serializers.SerializerMethodField()


    class Meta:
        model = Task
        fields = ["id", "title", "description", "status", "priority", "assignee", "reviewer", "due_date", "comments_count"]


    def get_comments_count(self, obj):
        return 0
    

class TaskCreateSerializer(serializers.ModelSerializer):
    assignee = TaskAssigneeAndReviewerSerializer(source="assignee_id", read_only=True)
    reviewer = TaskAssigneeAndReviewerSerializer(source="reviewer_id", read_only=True)
    board = serializers.PrimaryKeyRelatedField(queryset=Board.objects.all())
    reviewer_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True, required=False, allow_null=True)
    assignee_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True, required=False, allow_null=True)
    status = serializers.ChoiceField(choices=status, error_messages={"invalid_choice": "'{input}' is not a valid choice. Valid choices are: to-do, in-progress, review or done"})
    priority = serializers.ChoiceField(choices=priority, error_messages={"invalid_choice": "'{input}' is not a valid choice. Valid choices are: low, medium or high"})
    creator = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    comments_count = serializers.SerializerMethodField()


    class Meta:
        model = Task
        fields = ["id", "board", "title", "description", "status", "priority", "assignee", "assignee_id", "reviewer", "reviewer_id", "due_date", "creator", "comments_count"]


    def get_comments_count(self, obj):
        return 0
    

    def create(self, validated_data):
        assignee = validated_data.pop('assignee_id', None)
        reviewer = validated_data.pop('reviewer_id', None)
        creator = validated_data.pop('creator', None)
        board = validated_data.pop('board')
        if assignee and assignee not in board.members.all():
            assignee = None
        if reviewer and reviewer not in board.members.all():
            reviewer = None
        task = Task.objects.create(board=board, assignee_id=assignee, reviewer_id=reviewer, creator=creator, **validated_data)
        return task


class TaskUpdateSerializer(serializers.ModelSerializer):
    assignee = TaskAssigneeAndReviewerSerializer(source="assignee_id", read_only=True)
    reviewer = TaskAssigneeAndReviewerSerializer(source="reviewer_id", read_only=True)
    reviewer_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True, required=False, allow_null=True)
    assignee_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True, required=False, allow_null=True)
    status = serializers.ChoiceField(choices=status, error_messages={"invalid_choice": "'{input}' is not a valid choice. Valid choices are: to-do, in-progress, review or done"})
    priority = serializers.ChoiceField(choices=priority, error_messages={"invalid_choice": "'{input}' is not a valid choice. Valid choices are: low, medium or high"})


    class Meta:
        model = Task
        fields = ["id", "title", "description", "status", "priority", "assignee", "assignee_id", "reviewer", "reviewer_id", "due_date"]


    def validate(self, attrs):
        assignee = attrs.get("assignee_id", None)
        reviewer = attrs.get("reviewer_id", None)
        board_members = self.instance.board.members.all()
        if (assignee and assignee not in board_members) or (reviewer and reviewer not in board_members):
            raise serializers.ValidationError("assignee and reviewer must board members!")
        return attrs
    

    def update(self, instance, validated_data):
        validated_data.pop("board", None)
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.status = validated_data.get("status", instance.status)
        instance.priority = validated_data.get("priority", instance.priority)
        instance.assignee_id = validated_data.get("assignee_id", instance.assignee_id)
        instance.reviewer_id = validated_data.get("reviewer_id", instance.reviewer_id)
        instance.due_date = validated_data.get("due_date", instance.due_date)
        instance.save()
        return instance


class TaskAssignedOrReviewingListSerializer(serializers.ModelSerializer):
    assignee = TaskAssigneeAndReviewerSerializer(source="assignee_id", read_only=True)
    reviewer = TaskAssigneeAndReviewerSerializer(source="reviewer_id", read_only=True)
    board = serializers.PrimaryKeyRelatedField(queryset=Board.objects.all())
    status = serializers.ChoiceField(choices=status, error_messages={"invalid_choice": "'{input}' is not a valid choice. Valid choices are: to-do, in-progress, review or done"})
    priority = serializers.ChoiceField(choices=priority, error_messages={"invalid_choice": "'{input}' is not a valid choice. Valid choices are: low, medium or high"})
    comments_count = serializers.SerializerMethodField()


    class Meta:
        model = Task
        fields = ["id", "board", "title", "description", "status", "priority", "assignee", "reviewer", "due_date", "comments_count"]


    def get_comments_count(self, obj):
        return 0