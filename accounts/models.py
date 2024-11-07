from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager

# Model Custom User
class CustomUserModel(AbstractBaseUser, PermissionsMixin):
    # Peran Pengguna
    USER_ROLES = (
        ('owner', 'Owner/Developer'),
        ('partner', 'Partner/Mitra'),
        ('user', 'User'),
    )
    
    email = models.EmailField(_("Email Address"), unique=True, max_length=255)
    first_name = models.CharField(_("First Name"), max_length=100)
    last_name = models.CharField(_("Last Name"), max_length=100, null=True, blank=True)
    role = models.CharField(max_length=10, choices=USER_ROLES, default='user')  # Field untuk Role
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)  # Field untuk Foto Profil
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name']

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.email