from django.http import HttpResponse
from django.shortcuts import redirect
import requests, os
from adminPHIS.serializers import PhisUserSerializer
import jwt
from rest_framework import exceptions
from rest_framework.response import Response

from adminPHIS.models import AuthorApplication, PhisUser
from rest_framework.exceptions import AuthenticationFailed

JWT_SECRET = os.environ['JWT_SECRET_KEY']
JWT_ALGORITHM = 'HS256'


def authenticated_user(view_func):
    # Authenticate requests from microservice
    # These requests have no users, only JWT
    def wrapper_func(request, *args, **kwargs):
        response = Response()
        request.user = None
        jwt_token = request.headers['Authorization']
        if jwt_token:
            try:
                payload = jwt.decode(jwt_token, JWT_SECRET,
                                     algorithms=[JWT_ALGORITHM])
                if payload is not None:
                    request.payload = payload
                    return view_func(request, *args, **kwargs)
            except (jwt.DecodeError, jwt.ExpiredSignatureError):
                raise AuthenticationFailed('Unathenticated')
            
            
        else:
            raise exceptions.AuthenticationFailed("Authorization header is not present")

    return wrapper_func

def authenticate_admin(view_func):
    def wrapper_func(request, *args, **kwargs):
        request.user = None
        jwt_token = request.headers.get('Authorization', None)
        if jwt_token:
            try:
                payload = jwt.decode(jwt_token, JWT_SECRET,
                                     algorithms=[JWT_ALGORITHM])
                if payload['role'] == "S":
                    return view_func(request, *args, **kwargs)
                else:
                    raise AuthenticationFailed('Unauthorized access')
            except (jwt.DecodeError, jwt.ExpiredSignatureError):
                raise AuthenticationFailed('Bad token')
        else:
            raise AuthenticationFailed('Unathenticated')

    return wrapper_func

# header_data = curl GET(jwt.get_unverified_header(token))
# try:
#     payload = jwt.decode(
#         token,
#         key='',
#         algorithms=[header_data['alg'], ]
#     )
# except ExpiredSignatureError as error:
#     print(f'Unable to decode token, error: {error}')


# def allowed_users(allowed_roles=[]):
#     def decorator(view_func):
#         def wrapper_func(request, *args, **kwargs):
#
#             group = None
#             if request.user.groups.exists():
#                 group = request.user.groups.all()[0].name
#
#             if group in allowed_roles:
#                 return view_func(request, *args, **kwargs)
#             else:
#                 return HttpResponse('You are not authorized to view this page')
#
#         return wrapper_func
#
#     return decorator


def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        # if group == 'admin2':
        #     return HttpResponse('You are not authorized to view this page')
        if group == 'admin1':
            return view_func(request, *args, **kwargs)
        else:
            return AuthenticationFailed('Unathenticated')

    return wrapper_function

