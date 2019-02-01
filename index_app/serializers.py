from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User


class UserForAdminModelSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'last_login',
            'date_joined',
            'is_superuser',
            'is_staff',
            'is_active',
        )


class UserBaseSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
        )