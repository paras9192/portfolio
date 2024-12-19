import requests
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from django.db import transaction
from django.shortcuts import redirect

from apps.accounts.models import User
from .serializer import CreateUserSerializer, UserSerializer, UpdateUserSerializer
from rest_framework.permissions import IsAuthenticated
from chalkmate.rest_permissions import IsAuthenticatedOrCreateOnly, IsOwnerOrReadOnly
from chalkmate.utils import custom_success_response, login_yucampus_profile
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
from chalkmate.viewsets import ModelViewSet as CustomModelViewSet
from datetime import datetime
from rest_framework.exceptions import ValidationError

EMAIL_HOST_USER = settings.EMAIL_HOST_USER

def pageLogout(request):
    if request.method == "POST":
        logout(request)
        response = redirect('home')
        response.delete_cookie('login_token')
        return response


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticatedOrCreateOnly, IsOwnerOrReadOnly)

    def get_serializer_class(self, *args, **kwargs):
        method = self.request.method.lower()
        if method in ('get', 'delete'):
            return UserSerializer
        return CreateUserSerializer if method == 'post' else UpdateUserSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        signup_type = data.get("signup_type")
        if signup_type == "YUCAMPUS":
            email = data.get("email")
            password_yucampus = data.get("password_yucampus")
            password = data.get("password")
            if not email and not password_yucampus:
                raise ValidationError({"message": ["email id  is required"]})
            user_data = login_yucampus_profile(email=email, password=password_yucampus)
            if not user_data or not user_data.get("data"):
             raise ValidationError({"message": ["Failed to authenticate with YUCAMPUS."]})
            user_info = user_data["data"]
            user = User.objects.create(
                email=email,
                username=email,
                is_active=True,
                is_staff=False,
                is_superuser=False,
            )
            user.set_password(password)  # Hash the password
            user.save()
            id=user_info.get("user_id"),
            serializer = self.get_serializer(user)
            headers = self.get_success_headers(serializer.data)
            return custom_success_response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            return
        

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        # email_html_message = render_to_string('email/welcome.html', {'data': 'any dynamic data'})
        # email_plaintext_message = strip_tags(email_html_message)

        # send_mail(
        #     "Welcome to Yucampus", 
        #     email_plaintext_message, 
        #     EMAIL_HOST_USER, 
        #     [user.email, EMAIL_HOST_USER], 
        #     html_message=email_html_message
        # )

        headers = self.get_success_headers(serializer.data)
        return custom_success_response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_account(self, request):
        return custom_success_response(self.get_serializer(request.user).data)


class Login(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        # add error handling for this
        
        return custom_success_response(
            {
                'token': token.key,
                'user': UserSerializer(user).data,
            },
            status=status.HTTP_200_OK
        )


