import json
from adminPHIS.models import Followers

import jwt
import requests, os
from django.shortcuts import render
from rest_framework import status, response
from rest_framework.response import Response
from .models import AuthorApplication, Microservice, Menu, Submenu, PhisUser, Post
from .serializers import MicroserviceSerializer, GroupSerializer, MenuSerializer, PermissionSerializer, \
    SubmenuSerializer, PhisUserSerializer, PostSerializer
from rest_framework.decorators import api_view
from .roles import authenticate_admin, authenticated_user, admin_only, public_route
from django.utils import timezone
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from jwt.exceptions import ExpiredSignatureError

AUTH_URL = 'https://fedgen.ml/auth'
CONTENT_URL = "https://fedgen.ml/content"
secret = os.environ['JWT_SECRET_KEY']
page = 10
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


@api_view(['POST'])
@authenticate_admin
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
@api_view(['PUT'])
@authenticate_admin
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



@api_view(['Patch'])
@authenticate_admin
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

@api_view(['GET'])
@authenticate_admin
def menuList(request, format=None):
    menu = Menu.objects.all()
    serializer = MenuSerializer(menu, many=True)
    response = {
        'ok': 'True',
        'details': 'List of Menu',
        'data': serializer.data,
    }
    return Response(response)

@api_view(['POST'])
@authenticate_admin
def menuAdd(request, format=None):
    response = Response()
    user = PhisUser.objects.filter(auth_user_id=request.data['user_id']).first()
    microservice = Microservice.objects.filter(microserviceName=request.data['microservice']).first()
    data = request.data
    menu = Menu.objects.filter(menuname=data['menuname']).first()
    if user is not None and microservice is not None and menu is None:
        menu = Menu(user=user, microservice=microservice, menuname=data['menuname'], menustatus=data['menustatus'], comment=data['comment'])
        menu.save()
        response.data = {
            'ok': 'True',
            'details': 'Menu added'
        }
        response.status_code = 201
    else:
        response.data = {
            'ok': False,
            "details": "Duplicate"
        }
        response.status_code = 409
    return response



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



@api_view(['Patch'])
@authenticate_admin
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

@api_view(['POST'])
@authenticate_admin
def submenuAdd(request, format=None):
    response = Response()
    user = PhisUser.objects.filter(auth_user_id=request.data['user_id']).first()
    menu = Menu.objects.filter(menuname=request.data['menu']).first()
    data = request.data
    submenu = Submenu.objects.filter(submenuname=data['submenuname']).first()
    
    if user is not None and menu is not None and submenu is None:
        submenu = Submenu(user=user, menu=menu, submenuname=data['submenuname'], comment=data['comment'], submenuroute=data['submenuroute'], submenudescription=data['submenudescription'], submenustatus=data['submenustatus'])
        submenu.save()
        response.data = {
            'ok': 'True',
            'details': 'Submenu added'
        }
        response.status_code = 201
    else:
        response.data = {
            'ok': False,
            "details": "Duplicate"
        }
        response.status_code = 409
    return response



@api_view(['PUT'])
@authenticate_admin
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


@api_view(['Patch'])
@authenticate_admin
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



@api_view(['POST'])
@authenticate_admin
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



@api_view(['PUT'])
@authenticate_admin
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

@api_view(['GET'])
@authenticate_admin
def roleFunctionList(request, format=None):
    permission = Permission.objects.all()
    serializer = PermissionSerializer(permission, many=True)
    response = {
        'ok': 'True',
        'details': 'List of Role functions',
        'data': serializer.data,
    }
    return Response(response)


@api_view(['POST'])
@authenticate_admin
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

@api_view(['POST'])
@authenticate_admin
def userRoleAdd(request, format=None):
    response = Response()
    user = PhisUser.objects.get(email=request.data['user_email'])
    new_role = request.data['user_role']
    if user is not None:
        user.user_role = new_role
        user.save()
        role_data = {
            "user_email": request.data['user_email'],
            "user_role": new_role
        }
        content_data = {
            "auth_user_id": user.auth_user_id,
            "user_role": new_role
        }
        header = {'Authorization': request.headers.get('Authorization', None)}
        auth_request = requests.post('https://fedgen.ml/auth/event.assign.role',  json=role_data, headers=header)
        content_request = requests.post('https://fedgen.ml/content/event.assign.role', json=content_data, headers=header)
            
        response.data = {"ok": True, "details": "User role changed"}
        
    else:
        response.data = {"ok": False, "details": "User not found"}

    return response


# @authenticated_user
# @admin_only
@api_view(['GET'])
def userRoleList(request, format=None):
    user = PhisUser.groups.get(phisuser_id=2)
    serializer = PhisUserSerializer(user, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@authenticated_user
def userSignup(request, format=None):
    response = Response()
    data = request.data
    user = PhisUser.objects.filter(email=data['user_email']).first()
    if user is None:
        new_user = PhisUser(auth_user_id=data['auth_user_id'], email=data['user_email'], firstname=data['first_name'], lastname=data['last_name'], user_role=data['user_role'])
        new_user.save()
        response.data = {
            "ok": True,
            "email": data['user_email']
        }
    else:
        response.data = {
            "ok": True,
            "message": "User exists",
        }

    return response



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
            phis_user = PhisUser.objects.filter(email=request.data['email']).first()
            if user is not None and phis_user is not None:
                auth_req = requests.post(AUTH_URL + '/event.assign.role', json={"user_email": request.data['email'], "user_role": "A"}, headers={'Authorization': request.headers['Authorization']})
                if auth_req.ok:
                    requests.post(CONTENT_URL + '/event.assign.role', json={"auth_user_id": phis_user.auth_user_id, "user_role": "A"}, headers={'Authorization': request.headers['Authorization']})
                    user.status = 'A'
                    phis_user.user_role = "A"
                    user.updated_at = timezone.now()
                    user.save()
                    phis_user.save()
                    auth_data = {
                        "filter": "author",
                        "google_scholar": user.google_scholar,
                        "research_gate": user.research_gate,
                        "scopus": user.scopus,
                        "pub_med": user.pub_med,
                        "capic_status": user.capic_status,
                        "email": phis_user.email
                    }
                    notification_data = {
                        "filter": "author_approve",
                        "first_name": phis_user.firstname,
                        "to": phis_user.email,
                        "token": secret
                    }
                    # Send request to auth microservice
                    res = requests.post(AUTH_URL + '/update.user', json=auth_data, headers={'Authorization': request.headers['Authorization']})
                    # Send event to notification microservice
                    res1 = requests.post('https://fedgen.ml/notify/author', json=notification_data, headers={'Authorization': request.headers['Authorization']})
                    response.data = {"ok": True, "details": "User approved as author"}
            else:
                response.data = {"ok": False, "details": "User not found"}
        elif filter == "declined":
            user = AuthorApplication.objects.filter(email=request.data['email']).first()
            phis_user = PhisUser.objects.filter(email=request.data['email']).first()
            if user is not None and phis_user is not None:
                user.status = 'D'
                user.updated_at = timezone.now()
                user.save()
                response.data = {"ok": True, "details": "User declined as author"}
                notification_data = {
                    "filter": "author_declined",
                    "first_name": phis_user.firstname,
                    "to": phis_user.email,
                    "token": secret
                }
                res1 = requests.post('https://fedgen.ml/notify/author', json=notification_data, headers={'Authorization': request.headers['Authorization']})
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
            application = AuthorApplication.objects.filter(email=data['email']).first()
            if application is None:
                application = AuthorApplication(email=data['email'], google_scholar=data['google_scholar'], 
                                                research_gate=data['research_gate'], applied_at=timezone.now(),
                                                scopus=data['scopus'], pub_med=data['pub_med'], capic_status=data['capic_status'])
                application.save()
                user.save()
                response.data = {"ok": True, "details": "Application submitted"}
            elif application.status == 'D':
                application.status = 'P'
                application.research_gate = data['research_gate']
                application.google_scholar = data['google_scholar']
                application.scopus = data['scopus']
                application.pub_med = data['pub_med']
                application.capic_status = data['capic_status']
                application.save()
                response.data = {"ok": True, "details": "Application has been updated"}
            else:
                response.data = {"ok": False, "details": "You have already applied"}
        else:
            res = requests.post(AUTH_URL + '/get.user', json={"id": payload['id']}, headers={'Authorization': request.headers['Authorization']})
            if res.ok:
                res_data = res.json()['data']
                user = PhisUser(email=res_data['email'], auth_user_id=res_data['id'], firstname=res_data['firstname'], lastname=res_data['lastname'])
                user.save()
                application = AuthorApplication.objects.filter(email=data['email'], status='P').first()
                if application is None:
                    application = AuthorApplication(email=data['email'], google_scholar=data['google_scholar'], 
                                                    research_gate=data['research_gate'], applied_at=timezone.now(),
                                                    scopus=data['data'], pub_med=data['pub_med'], capic_status=data['capic_status'])
                    application.save()
                    user.save()
                    response.data = {"ok": True, "details": "Application submitted"}
                else:
                    response.data = {"ok": False, "details": "You have already applied"}  
            else:
                response.data = {"ok": False, "details": "User record missing"}
    except KeyError:
        response.data = {"ok": False, "details": "Invalid request"}
    return response

@api_view(['GET'])
@authenticate_admin
def getApplication(request, format=None):
    response = Response()
    applications = [
        {"email":application.email, 
        "gs": application.google_scholar, 
        "status": application.status,
        "rg": application.research_gate,
        "sc": application.scopus,
        "pb": application.pub_med,
        "ace": application.capic_status,
        "firstname": PhisUser.objects.filter(email=application.email).first().firstname,
        "lastname": PhisUser.objects.filter(email=application.email).first().lastname
        } for application in AuthorApplication.objects.filter(status="P")]
    response.data = {"ok": True, "applications": applications}
    
    return response

@api_view(['GET'])
@public_route
def getAuthor(request, pk):
    response = Response()
    if request.payload is not None: # is the request made by an authourised user
        phis_user_id = request.payload['id']
        user = PhisUser.objects.filter(auth_user_id=request.payload['id'])
        author = PhisUser.objects.filter(auth_user_id=pk).first()
        application = AuthorApplication.objects.filter(email=author.email, status="A").first()
        if author is not None and application is not None and user is not None: # If request is from a logged in user
            follower = application.followers_data
            if follower is not None:
                find = follower.get(phis_user_id)
                if find is not None:
                    isFollower = True
                else:
                    isFollower = False
            else:
                isFollower = False
            application = {
                "email": application.email,
                "gs": application.google_scholar, 
                "status": application.status,
                "rg": application.research_gate,
                "sc": application.scopus,
                "pb": application.pub_med,
                "ace": application.capic_status,
                "about": author.about,
                "isFollower": isFollower,
                "number_followers": application.number_followers,
                "firstname": PhisUser.objects.filter(email=application.email).first().firstname,
                "lastname": PhisUser.objects.filter(email=application.email).first().lastname
                } 
            response.data = {"ok": True, "data": application}
        else:
            response.data = {"ok": False}
    else: # If is a public request
        author = PhisUser.objects.filter(auth_user_id=pk).first()
        application = AuthorApplication.objects.filter(email=author.email, status="A").first()
        if author is not None and application is not None:
            application = {
                "email": application.email,
                "gs": application.google_scholar, 
                "status": application.status,
                "rg": application.research_gate,
                "sc": application.scopus,
                "pb": application.pub_med,
                "ace": application.capic_status,
                "about": author.about,
                "number_followers": application.number_followers,
                "firstname": PhisUser.objects.filter(email=application.email).first().firstname,
                "lastname": PhisUser.objects.filter(email=application.email).first().lastname
                } 
            response.data = {"ok": True, "data": application}
        else:
            response.data = {"ok": False}

    
    return response

@api_view(['GET'])
@authenticated_user
def getUser(request, format=None):
    response = Response()
    user = PhisUser.objects.filter(auth_user_id=request.payload['id']).first()
    application = AuthorApplication.objects.filter(email=user.email, status="A").first()
    if application is not None and user is not None:
        response.data = {
            "ok": True,
            "author": True,
            "application": {
                "email": application.email,
                "gs": application.google_scholar, 
                "status": application.status,
                "rg": application.research_gate,
                "sc": application.scopus,
                "pb": application.pub_med,
                "ace": application.capic_status,
                "number_followers": application.number_followers,
                } ,
            "user": {
                "email": user.email,
                "firstname": user.firstname,
                "lastname": user.lastname,
                "about": user.about,
                "role": user.user_role
            }
        }
    elif user is not None and application is None:
        response.data = {
            "ok": True,
            "author": False,
            "user": {
                "email": user.email,
                "firstname": user.firstname,
                "lastname": user.lastname,
                "about": user.about,
                "role": user.user_role
            }
        }
    else:
        response.data = {
            "ok": False,
            "message": "NotFound"
        }
        response.status_code = 404
    return response

@api_view(['PATCH'])
@authenticated_user
def UpdateAuthor(request, format=None):
    response = Response()
    data = request.data
    user = PhisUser.objects.filter(auth_user_id=request.payload['id']).first()
    application = AuthorApplication.objects.filter(email=user.email).first()
    if application is not None and user is not None:
        application.google_scholar = data['google_scholar']
        application.research_gate = data['research_gate']
        application.scopus = data['scopus']
        application.pub_med = data['pub_med']
        application.capic_status = data['capic_status']
        application.save()
        response.data = {
            "ok": True,
        }
    else:
        response.data = {
            "ok": False
        }
    return response

@api_view(['GET'])
@authenticated_user
def getUserBio(request, format=None):
    response = Response()
    user = PhisUser.objects.filter(auth_user_id=request.payload['id']).first()
    if user is not None:
        response.data = {
            "ok": True,
            "bio": user.about
        }
    else:
        response.data = {
            "ok": False,
            "details": "No user found"
        }
    return response

@api_view(['PATCH'])
@authenticated_user
def updateUserBio(request, format=None):
    response = Response()
    user = PhisUser.objects.filter(auth_user_id=request.payload['id']).first()
    try:
        bio = request.data['bio']
        if user is not None:
            user.about = bio
            user.save()
            response.data = {
                "ok": True
            }
        else:
            response.data = {
                "ok": False,
                "details": "No user found"
            }
    except KeyError:
        response.data = {
                "ok": False,
                "details": "Invalid request"
            }
    return response

@api_view(['POST'])
@authenticated_user
def followAuthor(request, format=None):
    response = Response()
    try:
        author_id = request.data['author_id']
        phis_user_id = request.payload['id']
        phis_user = PhisUser.objects.filter(auth_user_id=phis_user_id).first()
        author = PhisUser.objects.filter(auth_user_id=author_id).first()
        application = AuthorApplication.objects.get(email=author.email)
        if application is not None and author is not None and phis_user is not None:
            if author.user_role != 'P':
                followers = application.followers_data
                if followers is not None:
                    find = followers.get(phis_user_id)
                    if find is None:
                        application.number_followers += 1
                        application.followers_data[phis_user_id] = {
                            "auth_user_id": phis_user_id, 
                            "firstname": phis_user.firstname, 
                            "lastname": phis_user.lastname
                            }
                        application.save()

                        phis_user.following_data[author_id] = {
                            "auth_user_id": author_id, 
                            "firstname": author.firstname, 
                            "lastname": author.lastname
                        }
                        phis_user.save()
                        response.data = {
                            "ok": True,
                            "details": "Followed"
                        }
                        response.status_code = 200
                    else:
                        response.data = {
                                "ok": False,
                                "details": "User already a follower"
                            }
                        response.status_code = 409
                else:
                    application.number_followers += 1
                    data = {phis_user_id: phis_user_id}
                    application.followers_data = data
                    application.save()
                    response.data = {
                        "ok": True,
                        "details": "Followed"
                    }
                    response.status_code = 200
            else:
                response.data = {
                    "ok": False,
                    "details": "Author not Found"
                }
                response.status_code = 404
                
        else:
            response.data ={
                "ok": False,
                "message": "BadRequest"
            }
            response.status_code = 400
    except KeyError:
        response.data ={
            "ok": False,
            "message": "BadRequest"
        }
        response.status_code = 400
    return response

@api_view(['PATCH'])
@authenticated_user
def unfollowAuthor(request, format=None):
    response = Response()
    try:
        author_id = request.data['author_id']
        phis_user_id = request.payload['id']
        phis_user = PhisUser.objects.filter(auth_user_id=phis_user_id).first()
        author = PhisUser.objects.filter(auth_user_id=author_id).first()
        application = AuthorApplication.objects.get(email=author.email)
        if application is not None and author is not None and phis_user is not None:
            if author.user_role != 'P':
                followers = application.followers_data
                if followers is not None:
                    find = followers.get(phis_user_id)
                    if find is not None and application.number_followers != 0:
                        application.followers_data.pop(phis_user_id)
                        application.number_followers -= 1
                        application.save()

                        phis_user.following_data.pop(author_id)
                        phis_user.save()

                        response.data = {
                            "ok": True,
                            "details": "UnFollowed"
                        }
                        response.status_code = 200
                    elif find is not None and application.number_followers == 0:
                        response.data = {
                            "ok": False,
                            "details": "Invalid request"
                        }
                        response.status_code = 400
                    else:
                        response.data = {
                            "ok": False,
                            "details": "Invalid request: user is not a follower"
                        }
                        response.status_code = 400
                else:
                    application.followers_data = {}
                    application.number_followers = 0
                    application.save()
                    response.data = {
                        "ok": False,
                        "details": "Cannot unfollow"
                    }
            else:
                response.data ={
                    "ok": False,
                    "message": "BadRequest"
                }
                response.status_code = 400

        else:
            response.data ={
                "ok": False,
                "message": "BadRequest"
            }
            response.status_code = 400
    except KeyError:
        response.data ={
            "ok": False,
            "message": "BadRequest"
        }
        response.status_code = 400
    return response

@api_view(['GET'])
@authenticated_user
def getFollowing(request, format=None):
    phis_user_id = request.payload['id']
    phis_user = PhisUser.objects.filter(auth_user_id=phis_user_id).first()
    response = Response()
    response.data = {
        "data": phis_user.following_data
    }
    response.status_code = 200
    return response 


