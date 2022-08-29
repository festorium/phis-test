import json

import jwt
import requests
from django.shortcuts import render
from rest_framework import status, response
from rest_framework.response import Response

from .models import Microservice, Menu, Submenu, PhisUser
from .serializers import MicroserviceSerializer, GroupSerializer, MenuSerializer, PermissionSerializer, \
    SubmenuSerializer, PhisUserSerializer
from rest_framework.decorators import api_view
from .roles import authenticated_user, admin_only

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from jwt.exceptions import ExpiredSignatureError


# Microservice
@api_view(['GET'])
def microserviceList(request, format=None):
    microservice = Microservice.objects.all()
    serializer = MicroserviceSerializer(microservice, many=True)

    response = {
        'ok': 'True',
        'details': 'List of Microservices',
        'data': serializer.data,
    }
    return Response(response)


@authenticated_user
@admin_only
@api_view(['POST'])
def microserviceAdd(request, format=None):
    serializer = MicroserviceSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
    response = {
        'ok': 'True',
        'details': 'Microservice added',
        'data': serializer.data,
    }
    return Response(response)


@authenticated_user
@admin_only
@api_view(['PUT'])
def microserviceEdit(request, pk):
    microservice = Microservice.objects.get(id=pk)
    serializer = MicroserviceSerializer(instance=microservice, data=request.data)
    if serializer.is_valid():
        serializer.save()
    response = {
        'ok': 'True',
        'details': 'Microservice edited',
        'data': serializer.data,
    }
    return Response(response)


@authenticated_user
@admin_only
@api_view(['Patch'])
def microserviceRemove(request, pk):
    microservice = Microservice.objects.get(id=pk)
    data = request.data
    microservice.microserviceStatus = data.get("microserviceStatus", microservice.microserviceStatus)
    microservice.save()
    serializer = MicroserviceSerializer(microservice)
    response = {
        'ok': 'True',
        'details': 'Microservice status changed',
        'data': serializer.data,
    }
    return Response(response)


# Menu Views
@authenticated_user
@admin_only
@api_view(['GET'])
def menuList(request, format=None):
    menu = Menu.objects.all()
    serializer = MenuSerializer(menu, many=True)
    response = {
        'ok': 'True',
        'details': 'List of Menu',
        'data': serializer.data,
    }
    return Response(response)


@authenticated_user
@admin_only
@api_view(['POST'])
def menuAdd(request, format=None):
    serializer = MenuSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
    response = {
        'ok': 'True',
        'details': 'Menu added',
        'data': serializer.data,
    }
    return Response(response)


@authenticated_user
@admin_only
@api_view(['PUT'])
def menuEdit(request, pk):
    menu = Menu.objects.get(id=pk)
    serializer = MenuSerializer(instance=menu, data=request.data)
    if serializer.is_valid():
        serializer.save()
    response = {
        'ok': 'True',
        'details': 'Menu edited',
        'data': serializer.data,
    }
    return Response(response)


@authenticated_user
@admin_only
@api_view(['Patch'])
def menuRemove(request, pk):
    menu = Menu.objects.get(id=pk)
    data = request.data
    menu.menustatus = data.get("menustatus", menu.menustatus)
    menu.save()
    serializer = MenuSerializer(menu)
    response = {
        'ok': 'True',
        'details': 'Menu status changed',
        'data': serializer.data,
    }
    return Response(response)


# Submenu View
@authenticated_user
@admin_only
@api_view(['POST'])
def submenuAdd(request, format=None):
    serializer = SubmenuSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
    response = {
        'ok': 'True',
        'details': 'Submenu added',
        'data': serializer.data,
    }
    return Response(response)


@authenticated_user
@admin_only
@api_view(['PUT'])
def submenuEdit(request, pk):
    submenu = Submenu.objects.get(id=pk)
    serializer = SubmenuSerializer(instance=submenu, data=request.data)
    if serializer.is_valid():
        serializer.save()
    response = {
        'ok': 'True',
        'details': 'Submenu edited',
        'data': serializer.data,
    }
    return Response(response)


@authenticated_user
@admin_only
@api_view(['Patch'])
def submenuRemove(request, pk):
    submenu = Submenu.objects.get(id=pk)
    data = request.data
    submenu.submenustatus = data.get("submenustatus", submenu.submenustatus)
    submenu.save()
    serializer = SubmenuSerializer(submenu)
    response = {
        'ok': 'True',
        'details': 'Submenu status changed',
        'data': serializer.data,
    }
    return Response(response)


# Role View
@api_view(['GET'])
def roleList(request, format=None):
    group = Group.objects.all()
    serializer = GroupSerializer(group, many=True)
    response = {
        'ok': 'True',
        'details': 'List of Roles',
        'data': serializer.data,
    }
    return Response(response)


@authenticated_user
@admin_only
@api_view(['POST'])
def roleAdd(request, format=None):
    serializer = GroupSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
    response = {
        'ok': 'True',
        'details': 'Role added',
        'data': serializer.data,
    }
    return Response(response)


@authenticated_user
@admin_only
@api_view(['PUT'])
def roleEdit(request, pk):
    group = Group.objects.get(id=pk)
    serializer = GroupSerializer(instance=group, data=request.data)
    if serializer.is_valid():
        serializer.save()
    response = {
        'ok': 'True',
        'details': 'Role edited',
        'data': serializer.data,
    }
    return Response(response)


@authenticated_user
@admin_only
@api_view(['GET'])
def roleFunctionList(request, format=None):
    permission = Permission.objects.all()
    serializer = PermissionSerializer(permission, many=True)
    response = {
        'ok': 'True',
        'details': 'List of Role functions',
        'data': serializer.data,
    }
    return Response(response)


@authenticated_user
@admin_only
@api_view(['POST'])
def roleFunctionAdd(request, format=None):
    permissions = Permission.objects.get(id=request.data['pid'])
    auth_group = Group.objects.get(name=request.data['rolename'])
    auth_group.permissions.add(permissions)

    group = Group.objects.all()
    serializer = GroupSerializer(group, many=True)

    return Response(serializer.data)


# @authenticated_user
# @admin_only
@api_view(['GET'])
def userList(request, format=None):
    user = PhisUser.objects.all()
    serializer = PhisUserSerializer(user, many=True)
    response = {
        'ok': True,
        'details': 'List of Users',
        'data': serializer.data,
    }
    return Response(response)


@authenticated_user
@admin_only
@api_view(['POST'])
def userRoleAdd(request, format=None):
    my_group = Group.objects.get(id=request.data['group_id'])
    my_group.user_set.add(request.data['phisuser_id'])
    response = {
        'ok': 'True',
        'details': 'Role assigned successfully',
    }

    user = PhisUser.groups.get(phisuser_id=request.data['phisuser_id'])
    user_serializer = PhisUserSerializer(user, many=True)
    user_data = user_serializer.data

    group = Group.objects.get(id=request.data['group_id'])
    role_serializer = GroupSerializer(instance=group, data=request.data)

    role_data = {
        "user_id": user_data["id"],
        "user_role": role_serializer["name"]
    }
    r = requests.post('http://event.assign.role/', data=role_data)

    return Response(response)


# @authenticated_user
# @admin_only
@api_view(['GET'])
def userRoleList(request, format=None):
    user = PhisUser.groups.get(phisuser_id=2)
    serializer = PhisUserSerializer(user, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def userSignup(request, format=None):
    r = requests.get('https://event.user.signup/')

    data = json.loads(r.json)
    serializer = PhisUserSerializer(data=data)
    if serializer.is_valid():
        serializer.save(userid=data.user_id, user_role=data.user_role, email=data.user_email)

    return Response(serializer.data)
