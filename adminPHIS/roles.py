from aiohttp.web_response import json_response
from django.http import HttpResponse
from django.shortcuts import redirect

import jwt
from rest_framework import exceptions

from phis_admin.adminPHIS.models import PhisUser

JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'


def authenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):

        request.user = None
        jwt_token = request.headers.get('authorization', None)
        if jwt_token:
            try:
                payload = jwt.decode(jwt_token, JWT_SECRET,
                                     algorithms=[JWT_ALGORITHM])
            except (jwt.DecodeError, jwt.ExpiredSignatureError):
                return json_response({'message': 'Token is invalid'},
                                     status=400)

            request.user = PhisUser.objects.get(id=payload['user_id'])
            # if request.user.is_authenticated:
            if request.user:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')
        else:
            raise exceptions.AuthenticationFailed("Authorization header is not present")

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
            return HttpResponse('You are not authorized to view this page')

    return wrapper_function
