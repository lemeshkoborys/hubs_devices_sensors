from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserForAdminModelSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated


class UserListAPIView(generics.ListAPIView):

    """
    UserListAPIView - class based view.
    Allows admin users to retrieve all users data
    """

    permission_classes = (
        IsAuthenticated,
        IsAdminUser,
    )

    queryset = User.objects.all()
    serializer_class = UserForAdminModelSerializer
