from rest_framework import serializers
from .models import Microservice, Menu, PhisUser, Submenu
from django.contrib.auth.models import Group, Permission


class PhisUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhisUser
        fields = ('id', 'email', 'firstname', 'lastname')


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
        fields = ('id', 'menuname', 'comment', 'microservice', 'menustatus')


class SubmenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submenu
        fields = ('id', 'menu', 'submenuname', 'submenuroute', 'submenudescription', 'comment', 'submenustatus')
