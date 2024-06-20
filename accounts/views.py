from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from .serializers import *
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from .utils import unhash_token
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound, AuthenticationFailed
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi





class UserRegistrationAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        token_data = {
            "refresh": str(refresh),
            "access": str(access_token),
        }
        return Response(token_data, status=status.HTTP_201_CREATED)






class UpdateProfileView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"

    def get_queryset(self):
        decoded_token = unhash_token(self.request.headers)
        user_id = decoded_token.get('user_id')
        return User.objects.filter(id=user_id)


class PasswordResetView(APIView):
    queryset = User.objects.all()
    serializer_class = PasswordResetSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=PasswordResetSerializer
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        decoded_token = unhash_token(request.headers)
        user_id = decoded_token.get("user_id")

        if not user_id:
            raise AuthenticationFailed("User ID not found in token")

        old_password = serializer.validated_data.get("old_password")
        new_password = serializer.validated_data.get("new_password")

        user = get_object_or_404(User, id=user_id)

        if not check_password(old_password, user.password):
            return Response(
                {"error": "Incorrect old password!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.password = make_password(new_password)
        user.save()

        return Response({"data": "Password changed successfully"}, status=status.HTTP_200_OK)


class RetrieveProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        decoded_token = unhash_token(self.request.headers)
        user_id = decoded_token.get('user_id')

        if not user_id:
            raise NotFound("User not found")

        user = get_object_or_404(User, id=user_id)
        serializer = self.get_serializer(user)

        return Response(serializer.data)






class DeleteProfileAPIView(generics.DestroyAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    def get_queryset(self):
        decoded_token = unhash_token(self.request.headers)
        user_id = decoded_token.get('user_id')
        return User.objects.filter(id=user_id)



