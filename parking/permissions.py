from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'owner'
        # return request.user.role == 'owner'


class IsPartnerOrOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role == 'partner' or request.user.role == 'owner')


class IsUserOrAbove(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['user', 'partner', 'owner']
