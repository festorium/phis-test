from rest_framework import serializers
from .models import Microservice, Menu, PhisUser, Submenu, Role
from django.contrib.auth.models import Group, Permission


class PhisUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhisUser
        fields = ('id', 'email', 'firstname', 'lastname', 'user_role', 'auth_user_id')


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhisUser
        fields = ('id', 'auth_user_id', 'content_post_id', 'post_title', 'post_content')


class MicroserviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Microservice
        fields = ('id', 'microserviceName', 'microserviceStatus')


class GroupSerializer(serializers.ModelSerializer):
    # codename = serializers.RelatedField(
    #     source='Permission',
    #     read_only=True
    # )
    permissions = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='codename'
    )

    class Meta:
        model = Group
        fields = ('id', 'name', 'permissions',)


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('id', 'codename', 'content_type',)


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ('id', 'menuname', 'comment', 'user', 'microservice', 'menustatus')

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('id', 'rolename', 'roleshortname', 'roledescription', 'rolestatus', 'comment', 'user')


class SubmenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submenu
        fields = ('id', 'menu', 'submenuname', 'submenuroute', 'submenudescription', 'comment', 'role', 'submenustatus')
        depth = 1
