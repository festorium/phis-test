import json, datetime
from adminPHIS.models import Followers

import jwt
import requests, os
from django.shortcuts import render
from rest_framework import status, response
from rest_framework.response import Response
from .models import AuthorApplication, Microservice, Menu, Submenu, Role, PhisUser, Post
from .serializers import MicroserviceSerializer, GroupSerializer, MenuSerializer, PermissionSerializer, \
    SubmenuSerializer, PhisUserSerializer, PostSerializer, RoleSerializer
from rest_framework.decorators import api_view
from .roles import authenticate_admin, authenticated_user, admin_only, public_route
from django.utils import timezone
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from jwt.exceptions import ExpiredSignatureError

AUTH_URL = "https://phis.fedgen.net/auth"
CONTENT_URL = "https://phis.fedgen.net/content"
BACKEND_URL = "https://phis.fedgen.net"
secret = "QYmXTKt6bnzaFi76H7R88FQ"
page = 10


# UTILITIES
def generate_token():
    payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=3),
            'iat': datetime.datetime.utcnow()
        }

    token = jwt.encode(payload, secret, algorithm='HS256')
    
    return token

def send_notification_message(message, to, url=None):
    """Sends in-app notification to user"""
    event_data = {
                "to": to,
                "message": message,
                "url": url
            }
    token = generate_token()
    header = {'Authorization': token}
    req = requests.post(BACKEND_URL + '/notify/messages', json=event_data, headers=header)

    if req.ok:
        return True
    else:
        return False
    
def _get_user_from_auth_microservice(request, user_id):
    res = requests.post(AUTH_URL + '/get.user', json={"id": user_id}, headers={'Authorization': request.headers['Authorization']})
    if res.ok:
        res_data = res.json()['data']
        user = PhisUser.objects.filter(auth_user_id=user_id).first()
        if user is None:
            user = PhisUser(email=res_data['email'], auth_user_id=res_data['id'], firstname=res_data['firstname'], lastname=res_data['lastname'])
            user.save()
        return True
    else:
        return False

# Microservice
@api_view(['GET'])
@authenticate_admin
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
@api_view(['PATCH'])
@authenticate_admin
def microserviceEdit(request, pk):
    microservice = Microservice.objects.get(id=pk)
    if microservice is not None:
        serializer = MicroserviceSerializer(microservice, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = {
                'ok': True,
                'details': 'Microservice edited',
            }
    else:
        response = {
            'ok': False,
            'details': 'NotFound',
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


@api_view(['PATCH'])
@authenticated_user
def menuEdit(request, pk):
    data = request.data
    menu = Menu.objects.get(id=pk)
    if menu is not None:
        serializer = MenuSerializer(menu, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = {
                'ok': True,
                'details': 'Menu edited',
            }
    else:
        response = {
            'ok': False,
            'details': 'NotFound'
        }
    return Response(response)



@api_view(['PATCH'])
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

@api_view(['GET'])
@authenticate_admin
def submenuList(request, format=None):
    submenu = Submenu.objects.all()
    serializer = SubmenuSerializer(submenu, many=True)
    response = {
        'ok': 'True',
        'details': 'List of Submenu',
        'data': serializer.data,
    }
    return Response(response)



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



@api_view(['PATCH'])
@authenticate_admin
def submenuEdit(request, pk):
    data = request.data
    submenu = Submenu.objects.get(id=pk)
    if submenu is not None:
        serializer = SubmenuSerializer(submenu, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = {
                'ok': True,
                'details': 'Submenu edited',
            }
    else:
        response = {
            'ok': False,
            'details': 'NotFound'
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
    group = Role.objects.all()
    serializer = RoleSerializer(group, many=True)
    response = {
        'ok': 'True',
        'details': 'List of Roles',
        'data': serializer.data,
    }
    return Response(response)





@api_view(['POST'])
@authenticate_admin
def roleAdd(request, format=None):
    response = Response()
    user = PhisUser.objects.filter(auth_user_id=request.data['user_id']).first()
    data = request.data
    role = Role.objects.filter(rolename=data['rolename']).first()
    if user is not None and role is None:
        role = Role(user=user, rolename=data['rolename'], roleshortname=data['roleshortname'], roledescription=data['roledescription'], rolestatus=data['rolestatus'], comment=data['comment'])
        role.save()
        response.data = {
            'ok': 'True',
            'details': 'Role added'
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
def roleEdit(request, pk):
    data = request.data
    role = Role.objects.get(id=pk)
    if role is not None:
        serializer = RoleSerializer(role, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = {
                'ok': True,
                'details': 'Role edited',
            }
    else:
        response = {
            'ok': False,
            'details': 'NotFound'
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
    response = Response()
    data = request.data
    role_id = Role.objects.filter(id=request.data['role_id']).first()
    submenu = Submenu.objects.filter(id=data['submenu_id']).first()
    
    if role_id is not None and submenu is not None:
        submenu.role.add(role_id)
        response.data = {
            'ok': 'True',
            'details': 'Role Right Assigned'
        }
        response.status_code = 201
    else:
        response.data = {
            'ok': False,
            "details": "Duplicate"
        }
        response.status_code = 409
    return response


# roleFunctionRem
@api_view(['POST'])
@authenticate_admin
def roleFunctionRem(request, format=None):
    data = request.data
    role_id = Role.objects.filter(id=data['role_id']).first()
    submenu = Submenu.objects.filter(id=data['submenu_id']).first()
    
    response = Response(
        {
            'ok': 'True' if role_id and submenu else 'False',
            'details': 'Role Right Unassigned' if role_id and submenu else 'No Right'
        },
        status=201 if role_id and submenu else 409
    )

    if role_id and submenu:
        submenu.role.remove(role_id)
    
    return response


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
        auth_request = requests.post(BACKEND_URL + '/auth/event.assign.role',  json=role_data, headers=header)
        content_request = requests.post(BACKEND_URL + '/content/event.assign.role', json=content_data, headers=header)
            
        response.data = {"ok": True, "details": "User role changed"}
        
    else:
        response.data = {"ok": False, "details": "User not found"}

    return response

# userRoleRem
@api_view(['POST'])
@authenticate_admin
def userRoleRem(request):
    if 'user_email' not in request.data:
        response = Response({"ok": False, "details": "Missing user_email field"}, status=status.HTTP_400_BAD_REQUEST)
        return response
        
    response = Response()

    user = get_object_or_404(PhisUser, email=request.data['user_email'])
    new_role = "P"

    try:
        user.objects.update(user_role=new_role)
        role_data = {
            "user_email": request.data['user_email'],
            "user_role": new_role
        }
        content_data = {
            "auth_user_id": user.auth_user_id,
            "user_role": new_role
        }
        header = {'Authorization': request.headers.get('Authorization', None)}
        auth_request = requests.post(BACKEND_URL + '/auth/event.assign.role',  json=role_data, headers=header)
        auth_request.raise_for_status()
        content_request = requests.post(BACKEND_URL + '/content/event.assign.role', json=content_data, headers=header)
        content_request.raise_for_status()
    except requests.exceptions.RequestException as e:
        response.data = {"ok": False, "details": "Error sending HTTP request: " + str(e)}
        response.status = status.HTTP_500_INTERNAL_SERVER_ERROR
        return response
        
    response.data = {"ok": True, "details": "User role changed"}
    response.status = status.HTTP_200_OK
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
                    res1 = requests.post(BACKEND_URL + '/notify/author', json=notification_data, headers={'Authorization': request.headers['Authorization']})
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
                res1 = requests.post(BACKEND_URL + '/notify/author', json=notification_data, headers={'Authorization': request.headers['Authorization']})
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
        author = PhisUser.objects.filter(auth_user_id=pk).first()
        application = AuthorApplication.objects.filter(email=author.email, status="A").first()
        if author is not None and application is not None: # If request is from a logged in user
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
                "profile_picture": author.profile_picture,
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
                "firstname": author.firstname,
                "lastname": author.lastname
                } 
            response.data = {"ok": True, "data": application}
            response.status_code = 200

        elif author is not None and application is None:
            response.data = {"ok": False, "message": "User has not applied to be an author"}
            response.status_code = 403

        else:
            _get_user_from_auth_microservice(request, pk)
            response.data = {"ok": False, "message": "User not Found"}
            response.status_code = 404

    else: # If is a public request
        author = PhisUser.objects.filter(auth_user_id=pk).first()
        application = AuthorApplication.objects.filter(email=author.email, status="A").first()
        if author is not None and application is not None:
            application = {
                 "profile_picture": author.profile_picture,
                "email": application.email,
                "gs": application.google_scholar, 
                "status": application.status,
                "rg": application.research_gate,
                "sc": application.scopus,
                "pb": application.pub_med,
                "ace": application.capic_status,
                "about": author.about,
                "number_followers": application.number_followers,
                "firstname": author.firstname,
                "lastname": author.lastname
                } 
            response.data = {"ok": True, "data": application}
            response.status_code = 200

        elif author is not None and application is None:
            response.data = {"ok": False, "message": "User has not applied to be an author"}
            response.status_code = 403

        else:
            _get_user_from_auth_microservice(request, pk)
            response.data = {"ok": False, "message": "User not Found"}
            response.status_code = 404

    
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
                "role": user.user_role,
                "profile_picture": user.profile_picture
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
                "role": user.user_role,
                "profile_picture": user.profile_picture
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

        # If User, Author, and Author application are found
        if application is not None and author is not None and phis_user is not None:
            if author.user_role != 'P':
                followers = application.followers_data

                # If author has followers add new follower to followers_data JSON
                # else create a new following_data JSON for the author
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


                        # If User is not following any author
                        # create new JSON with author data
                        if phis_user.following_data is None:
                            data = {author_id: {
                                    "auth_user_id": author_id, 
                                    "firstname": author.firstname, 
                                    "lastname": author.lastname
                                }
                            }
                            phis_user.following_data = data
                            phis_user.save()
                        else:
                            phis_user.following_data[author_id] = {
                                    "auth_user_id": author_id, 
                                    "firstname": author.firstname, 
                                    "lastname": author.lastname
                                }
                            phis_user.save()
                            
                        # send notification
                        message = """
                        {} {} followed you
                        """.format(phis_user.firstname, phis_user.lastname)
                        to = author_id
                        send_notification_message(message, to)

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
                    # Add to author followers data
                    application.number_followers += 1
                    data = {phis_user_id: {
                            "auth_user_id": phis_user_id, 
                            "firstname": phis_user.firstname, 
                            "lastname": phis_user.lastname
                            }}
                    application.followers_data = data
                    application.save()

                    
                    # If User is not following any author
                    # create new JSON with author data
                    if phis_user.following_data is None:
                        data = {author_id: {
                                "auth_user_id": author_id, 
                                "firstname": author.firstname, 
                                "lastname": author.lastname
                            }
                        }
                        phis_user.following_data = data
                        phis_user.save()
                    else:
                        phis_user.following_data[author_id] = {
                                "auth_user_id": author_id, 
                                "firstname": author.firstname, 
                                "lastname": author.lastname
                            }
                        phis_user.save()

                    # Send notification
                    message = """
                    {} {} followed you
                    """.format(phis_user.firstname, phis_user.lastname)
                    to = author_id
                    send_notification_message(message, to)

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

                        # If user is not following any author
                        # create empty JSON
                        if phis_user.following_data is None:
                            phis_user.following_data = {}
                            phis_user.save()
                        else:
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

@api_view(['PATCH'])
@authenticated_user
def setProfilePicture(request, format=None):
    data = request.data
    response = Response()
    phis_user_id = request.payload['id']
    phis_user = PhisUser.objects.filter(auth_user_id=phis_user_id).first()
    if phis_user is not None and data.get('path'):
        phis_user.profile_picture = data['path']
        phis_user.save()
        response.data = {
            "ok": True,
            "updated": True
        }
        response.status_code = 200
    else:
        response.data = {
            "ok": False,
            "updated": False
        }
        response.status_code = 404

    return response

@api_view(['GET'])
@authenticated_user
def hasUserAppliedToBeAuthor(request, format=None):
    response = Response()
    phis_user_id = request.payload['id']
    phis_user = PhisUser.objects.filter(auth_user_id=phis_user_id).first()
    if phis_user is not None:
        application = AuthorApplication.objects.filter(email=phis_user.email).first()
        if application is not None:
            response.data = {
                "ok": True
            }
            response.status_code = 200
        else:
            response.data = {
                "ok": False
            }
            response.status_code = 404
    else:
        response.data = {
            "ok": False
        }
        response.status_code = 404

    return response



@api_view(['GET'])
def get_profile_picture(request, user_id):
    response = Response()
    user = PhisUser.objects.filter(auth_user_id=user_id).first()
    if user is not None:
        response.data = {
            "ok": True,
            "path": user.profile_picture
        }
        response.status_code = 200
    else:
        response.data = {
            "ok": False,
            "path": "/media/profiles/default.png"
        }
        response.status_code = 404

    return response