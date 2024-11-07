# from django.shortcuts import render

# # Create your views here.
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from .permissions import IsAdminUser, IsEditorOrAdmin, IsViewerOrAbove

# # View yang hanya bisa diakses oleh Admin
# class AdminOnlyView(APIView):
#     permission_classes = [IsAuthenticated, IsAdminUser]

#     def get(self, request):
#         return Response({"message": "Hanya Admin yang bisa mengakses ini."})

# # View yang bisa diakses oleh Editor dan Admin
# class EditorOrAdminView(APIView):
#     permission_classes = [IsAuthenticated, IsEditorOrAdmin]

#     def get(self, request):
#         return Response({"message": "Editor dan Admin bisa mengakses ini."})

# # View yang bisa diakses oleh Viewer ke atas (Viewer, Editor, Admin)
# class ViewerOrAboveView(APIView):
#     permission_classes = [IsAuthenticated, IsViewerOrAbove]

#     def get(self, request):
#         return Response({"message": "Viewer, Editor, dan Admin bisa mengakses ini."})

from django.shortcuts import redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import update_last_login
from allauth.account.utils import send_email_confirmation
from .serializers import CustomRegisterSerializer, CustomUserUpdateSerializer, CustomRoleUpdateSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from .permissions import IsOwner, IsPartnerOrOwner, IsUserOrAbove


User = get_user_model()

def email_confirmation(request, key):
    return redirect(f"http://localhost:5173/dj-rest-auth/registration/account-confirm-email/{key}")


def reset_password_confirm(request, uid, token):
    return redirect(f"http://localhost:5173/reset/password/confirm/{uid}/{token}")



class GetAllUsersView(ListAPIView):
    queryset = User.objects.all()  
    serializer_class = CustomRegisterSerializer
    permission_classes = [IsAuthenticated, IsOwner]  

class GetUserByTokenView(APIView):
    permission_classes = [IsAuthenticated, IsUserOrAbove] 
    
    def get(self, request):
        user = request.user  # Mendapatkan user dari token JWT
        
        return Response({
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role,
            'profile_picture': user.profile_picture.url if user.profile_picture else None,
        }, status=status.HTTP_200_OK)



class CustomLoginView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        
        # Otentikasi pengguna
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            # Jika otentikasi berhasil, buat refresh dan access token
            refresh = RefreshToken.for_user(user)
            
            # Update waktu login terakhir (opsional)
            update_last_login(None, user)
            
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'role': user.role
                }
            }, status=status.HTTP_200_OK)
        else:
            # Jika otentikasi gagal, kirim respon dengan pesan error
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def custom_register(request):
    if request.method == 'POST':
        serializer = CustomRegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            # Simpan user baru jika valid
            user = serializer.save()
            
            # Kirim email konfirmasi
            send_email_confirmation(request, user)
            
            # Buat token JWT untuk user baru
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'message': 'User registered successfully. Please verify your email.',
                'user': {
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'role': user.role,  # Tambahkan role di response
                    'profile_picture': user.profile_picture.url if user.profile_picture else None,  # Tambahkan profile_picture di response
                },
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
        else:
            # Jika ada kesalahan dalam serializer, kembalikan error
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateUserView(APIView):
    permission_classes = [IsAuthenticated, IsUserOrAbove]
    
    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = CustomUserUpdateSerializer(user, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'User updated successfully',
                'user': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        user = request.user
        serializer = CustomUserUpdateSerializer(user, data=request.data, partial=True)  
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'User updated successfully',
                'user': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateRoleUserView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]
    
    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = CustomRoleUpdateSerializer(user, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'User updated successfully',
                'user': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        user = request.user
        serializer = CustomRoleUpdateSerializer(user, data=request.data, partial=True)  
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'User updated successfully',
                'user': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
