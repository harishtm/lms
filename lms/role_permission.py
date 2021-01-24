from rest_framework.permissions import BasePermission
from tutor.models import LmsUser


class UserRole(BasePermission):

    def has_permission(self, request, view):
        return LmsUser.objects.filter(id=request.user_id, role='1').exists()


class MentorRole(BasePermission):

    def has_permission(self, request, view):
        return LmsUser.objects.filter(id=request.user_id, role='2').exists()