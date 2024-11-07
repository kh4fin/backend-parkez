# from dj_rest_auth.registration.serializers import RegisterSerializer
# from rest_framework import serializers
# from .models import CustomUserModel  # Sesuaikan nama modelmu

# class CustomRegisterSerializer(RegisterSerializer):
#     first_name = serializers.CharField(required=True)
#     last_name = serializers.CharField(required=False)

#     class Meta:
#         model = CustomUserModel
#         fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

#     def get_cleaned_data(self):
#         data = super().get_cleaned_data()
#         data['first_name'] = self.validated_data.get('first_name', '')
#         data['last_name'] = self.validated_data.get('last_name', '')
#         return data

#     def save(self, request):
#         user = super().save(request)
#         user.first_name = self.cleaned_data.get('first_name')
#         user.last_name = self.cleaned_data.get('last_name')
#         user.save()
#         return user


from rest_framework import serializers
from django.contrib.auth import get_user_model



User = get_user_model()

class CustomUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'profile_picture']  

class CustomRoleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'role', 'profile_picture']  


class CustomRegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=User.USER_ROLES, default='user')  # Field untuk Role
    profile_picture = serializers.ImageField(required=False, allow_null=True)  # Field untuk Foto Profil

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2', 'role', 'profile_picture']  # Tambahkan role dan profile_picture

    def validate(self, data):
        # Validasi password
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        # Hapus password1 dan password2 sebelum menyimpan user
        password = validated_data.pop('password1')
        validated_data.pop('password2')

        # Ambil role dan profile_picture jika tersedia
        role = validated_data.get('role', 'user')
        profile_picture = validated_data.get('profile_picture', None)

        # Buat user
        user = User(
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=role,  # Set role
            profile_picture=profile_picture,  # Set foto profil
        )
        user.set_password(password)  # Set password
        user.save()
        return user
