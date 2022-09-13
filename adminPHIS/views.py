import json

import jwt
import requests
from django.shortcuts import render
from rest_framework import status, response
from rest_framework.response import Response
from .models import AuthorApplication, Microservice, Menu, Submenu, PhisUser, Post
from .serializers import MicroserviceSerializer, GroupSerializer, MenuSerializer, PermissionSerializer, \
    SubmenuSerializer, PhisUserSerializer, PostSerializer
from rest_framework.decorators import api_view
from .roles import authenticate_admin, authenticated_user, admin_only

from django.utils import timezone
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from jwt.exceptions import ExpiredSignatureError

AUTH_URL = 'https://fedgen.ml/auth'

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
@authenticated_user
def userSignup(request, format=None):
    data = request.data
    serializer = PhisUserSerializer(data=data)
    if serializer.is_valid():
        serializer.save(auth_user_id=data['auth_user_id'], user_role=data['user_role'], email=data['user_email'],
                        firstname=data['first_name'], lastname=data['last_name'])

    return Response(serializer.data)



@api_view(['GET'])
def createPost(request, format=None):
    data = request.data
    serializer = PostSerializer(data=data)
    if serializer.is_valid():
        serializer.save(auth_user_id=data['auth_user_id'], content_post_id=data['content_post_id'],
                        post_title=data['post_title'], post_content=data['post_content'])

    return Response(serializer.data)


@authenticated_user
@admin_only
@api_view(['POST'])
def approvePost(request, format=None):
    response = {
        'ok': 'True',
        'details': 'Post approved successfully',
    }

    post = Post.objects.get(content_post_id=request.data['content_post_id'])
    post_serializer = PostSerializer(post, many=True)
    post_data = post_serializer.data

    approve_data = {
        "content_post_id": post_data["content_post_id"],
        "auth_user_id": post_data["auth_user_id"]
    }
    r = requests.post('http://event.approve.post/', data=approve_data)

    return Response(response)

@api_view(['POST'])
@authenticate_admin
def engageApplication(request, format=None):
    response = Response()
    try:
        filter = request.data['filter']
        if filter == "approve":
            user = AuthorApplication.objects.filter(email=request.data['email']).first()
            if user is not None:
                auth_req = requests.post(AUTH_URL + '/event.assign.role', json={"user_email": request.data['email'], "user_role": "A"}, headers={'Authorization': request.headers['Authorization']})
                if auth_req.ok:
                    user.status = 'A'
                    user.updated_at = timezone.now()
                    user.save()
                    response.data = {"ok": True, "details": "User approved as author"}
            else:
                response.data = {"ok": False, "details": "User not found"}
        elif filter == "declined":
            user = AuthorApplication.objects.filter(email=request.data['email']).first()
            if user is not None:
                user.status = 'D'
                user.updated_at = timezone.now()
                user.save()
                response.data = {"ok": True, "details": "User approved as author"}
            else:
                response.data = {"ok": False, "details": "User not found"}
        else:
            response.data = {"ok": False, "details": "Invalid request"}
    except KeyError:
        response.data = {
            "ok": False,
            "details": "Invalid request"
        }
    return response

@api_view(['POST'])
@authenticated_user
def submitApplication(request, format=None):
    response = Response()
    try:
        data = request.data
        payload = request.payload
        user = PhisUser.objects.filter(auth_user_id=payload['id']).first()
        if user is not None:
            application = AuthorApplication(email=data['email'], google_scholar=data['google_scholar'], applied_at=timezone.now())
            application.save()
            response.data = {"ok": True, "details": "Application submitted"}
        else:
            res = requests.post(AUTH_URL + '/get.user', json={"id": payload['id']}, headers={'Authorization': request.headers['Authorization']})
            if res.ok:
                res_data = res.json()['data']
                application = AuthorApplication(email=data['email'], google_scholar=data['google_scholar'], applied_at=timezone.now())
                application.save()
                user = PhisUser(email=res_data['email'], auth_user_id=res_data['id'], firstname=res_data['firstname'], lastname=res_data['lastname'])
                
                user.save()
                response.data = {"ok": True, "details": "Application submitted"}
            else:
                response.data = {"ok": False, "details": "User record missing"}
    except KeyError:
        response.data = {"ok": False, "details": "Invalid request"}
    return response

@api_view(['GET'])
@authenticate_admin
def getApplication(request, format=None):
    response = Response()
    try:
        filter = request.data['filter']
        if filter == 'P' or filter == 'A' or filter == 'D':
            applications = [{"email":application.email, "gs": application.google_scholar, "status": application.status} for application in AuthorApplication.objects.filter(status=filter)]
            response.data = {"ok": True, "applications": applications}
        else:
           response.data = {"ok": False, "details": "Invalid request"}
    except KeyError:
        response.data = {"ok": False, "details": "Invalid request"}
    return response

@api_view(['GET'])
@authenticated_user
def getUserApplication(request, format=None):
    response = Response()
    app = AuthorApplication.objects.filter(email=request.data['email'])
    if app is not None:
        response.data = {
            "ok": True,
            "gs": app.google_scholar,
            "status": app.status
        }
    else:
        response.data = {
            "ok": False,
            "details": "No application found"
        }
