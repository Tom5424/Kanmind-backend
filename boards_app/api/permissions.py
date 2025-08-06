from rest_framework.permissions import BasePermission


class IsBoardOwnerOrMember(BasePermission):
    

    def has_object_permission(self, request, view, obj):
        return obj.owner_id_id == request.user.id or request.user in obj.members.all()
    

class IsBoardOwner(BasePermission):
    

    def has_object_permission(self, request, view, obj):
        return obj.owner_id_id == request.user.id    