from django.urls import path
from .views import custom_register, CustomLoginView, GetAllUsersView, UpdateUserView, GetUserByTokenView, UpdateRoleUserView,GetUserByIdView, DeleteUserById

urlpatterns = [
    path('registration/', custom_register, name='custom-registration'),
    path('login/', CustomLoginView.as_view(), name='custom-login'),
    path('users/', GetAllUsersView.as_view(), name='get_all_users'),
    path('users/<int:pk>/', DeleteUserById.as_view(), name='user-deleted'),
    path('users/me/', GetUserByTokenView.as_view(), name='get_user_by_token'),
    path('users/edit/<int:user_id>/', GetUserByIdView.as_view(), name='get_user_by_token'),
    path('users/update/', UpdateUserView.as_view(), name='update_user'),
    path('users/update/admin/<int:user_id>/', UpdateRoleUserView.as_view(), name='update_user_from_admin'),
]

