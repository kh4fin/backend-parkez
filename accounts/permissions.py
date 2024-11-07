# from rest_framework.permissions import BasePermission

# class IsAdminUser(BasePermission):
#     def has_permission(self, request, view):
#         return request.user.is_authenticated and request.user.role == 'admin'


# class IsEditorOrAdmin(BasePermission):
#     def has_permission(self, request, view):
#         return request.user.is_authenticated and (request.user.role == 'editor' or request.user.role == 'admin')


# class IsViewerOrAbove(BasePermission):
#     def has_permission(self, request, view):
#         return request.user.is_authenticated and request.user.role in ['viewer', 'editor', 'admin']

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
