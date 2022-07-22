from django.shortcuts import render
from rest_framework.response import Response

from .models import Microservice, Menu, Submenu, PhisUser
from .serializers import MicroserviceSerializer, GroupSerializer, MenuSerializer, PermissionSerializer, \
    SubmenuSerializer, PhisUserSerializer
from rest_framework.decorators import api_view
from .roles import authenticated_user, admin_only

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


# Microservice
@api_view(['GET'])
def microserviceList(request, format=None):
    microservice = Microservice.objects.all()
    serializer = MicroserviceSerializer(microservice, many=True)
    return Response(serializer.data)


@authenticated_user
@admin_only
@api_view(['POST'])
def microserviceAdd(request, format=None):
    serializer = MicroserviceSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@authenticated_user
@admin_only
@api_view(['PUT'])
def microserviceEdit(request, pk):
    microservice = Microservice.objects.get(id=pk)
    serializer = MicroserviceSerializer(instance=microservice, data=request.data)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@authenticated_user
@admin_only
@api_view(['Patch'])
def microserviceRemove(request, pk):
    microservice = Microservice.objects.get(id=pk)
    data = request.data
    microservice.microserviceStatus = data.get("microserviceStatus", microservice.microserviceStatus)
    microservice.save()
    serializer = MicroserviceSerializer(microservice)

    return Response(serializer.data)


# Menu Views
@authenticated_user
@admin_only
@api_view(['GET'])
def menuList(request, format=None):
    menu = Menu.objects.all()
    serializer = MenuSerializer(menu, many=True)
    return Response(serializer.data)


@authenticated_user
@admin_only
@api_view(['POST'])
def menuAdd(request, format=None):
    serializer = MenuSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@authenticated_user
@admin_only
@api_view(['PUT'])
def menuEdit(request, pk):
    menu = Menu.objects.get(id=pk)
    serializer = MenuSerializer(instance=menu, data=request.data)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@authenticated_user
@admin_only
@api_view(['Patch'])
def menuRemove(request, pk):
    menu = Menu.objects.get(id=pk)
    data = request.data
    menu.menustatus = data.get("menustatus", menu.menustatus)
    menu.save()
    serializer = MenuSerializer(menu)

    return Response(serializer.data)


# Submenu View
@authenticated_user
@admin_only
@api_view(['POST'])
def submenuAdd(request, format=None):
    serializer = SubmenuSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@authenticated_user
@admin_only
@api_view(['PUT'])
def submenuEdit(request, pk):
    submenu = Submenu.objects.get(id=pk)
    serializer = SubmenuSerializer(instance=submenu, data=request.data)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@authenticated_user
@admin_only
@api_view(['Patch'])
def submenuRemove(request, pk):
    submenu = Submenu.objects.get(id=pk)
    data = request.data
    submenu.submenustatus = data.get("submenustatus", submenu.submenustatus)
    submenu.save()
    serializer = SubmenuSerializer(submenu)

    return Response(serializer.data)


# Role View
@api_view(['GET'])
def roleList(request, format=None):
    group = Group.objects.all()
    serializer = GroupSerializer(group, many=True)
    return Response(serializer.data)


@authenticated_user
@admin_only
@api_view(['POST'])
def roleAdd(request, format=None):
    serializer = GroupSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@authenticated_user
@admin_only
@api_view(['PUT'])
def roleEdit(request, pk):
    group = Group.objects.get(id=pk)
    serializer = GroupSerializer(instance=group, data=request.data)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@authenticated_user
@admin_only
@api_view(['GET'])
def roleFunctionList(request, format=None):
    permission = Permission.objects.all()
    serializer = PermissionSerializer(permission, many=True)
    return Response(serializer.data)


@authenticated_user
@admin_only
@api_view(['POST'])
def roleFunctionAdd(request, format=None):
    # somemodel_ct = ContentType.objects.get(app_label='myapp', model='somemodel')
    # permission = Permission(name=request.codename, codename=request.codename, content_type=request.content_type)
    # permission.save()
    # special_users = request.rolename
    # special_users.permissions.add(permission)
    permissions = Permission.objects.get(id=request.data['pid'])
    auth_group = Group.objects.get(name=request.data['rolename'])
    auth_group.permissions.add(permissions)

    group = Group.objects.all()
    serializer = GroupSerializer(group, many=True)

    return Response(serializer.data)


@authenticated_user
@admin_only
@api_view(['GET'])
def userList(request, format=None):
    user = PhisUser.objects.all()
    serializer = PhisUserSerializer(user, many=True)
    return Response(serializer.data)


@authenticated_user
@admin_only
@api_view(['POST'])
def userRoleAdd(request, format=None):
    my_group = Group.objects.get(id=request.data['group_id'])
    my_group.user_set.add(request.data['phisuser_id'])

    return Response("Role assigned successfully")
