from django.contrib import admin
from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('microservice-list', views.microserviceList, name='microservice-list'),
    path('microservice-add', views.microserviceAdd, name='microservice-add'),
    path('microservice-edit/<int:pk>', views.microserviceEdit, name='microservice-edit'),
    path('microservice-remove/<int:pk>', views.microserviceRemove, name='microservice-remove'),

    path('user-list', views.userList, name='user-list'),
    path('role-list', views.roleList, name='role-list'),
    path('role-add', views.roleAdd, name='role-add'),
    path('role-edit/<int:pk>', views.roleEdit, name='role-edit'),
    path('rolefunc-list', views.roleFunctionList, name='rolefunc-list'),
    path('rolefunc-add', views.roleFunctionAdd, name='role-add'),
    path('userrole-add', views.userRoleAdd, name='userrole-add'),

    path('event.user.signup', views.userSignup, name='event-user-signup'),
    path('event.create.post', views.createPost, name='event-create-post'),
    path('event.approve.post', views.approvePost, name='event-approve-post'),

    path('menu-add', views.menuAdd, name='menu-add'),
    path('menu-list', views.menuList, name='menu-list'),
    path('menu-edit/<int:pk>', views.menuEdit, name='menu-edit'),
    path('menu-remove/<int:pk>', views.menuRemove, name='menu-remove'),

    path('submenu-add/', views.submenuAdd, name='submenu-add'),
    path('submenu-edit/<int:pk>', views.submenuEdit, name='submenu-edit'),
    path('submenu-remove/<int:pk>', views.submenuRemove, name='submenu-remove'),

    path('submit.application', views.submitApplication, name='submit-application'),
    path('get.application', views.getApplication, name='get-application'),
    path('engage.application', views.engageApplication, name='engage-application'),
    path('author/<str:pk>', views.getAuthor, name='get-author'),
    path('get.bio', views.getUserBio, name='get-bio'),
    path('update.bio', views.updateUserBio, name='update-bio'),
    path('follow', views.followAuthor, name='follow-author'),
    path('unfollow', views.unfollowAuthor, name='unfollow-author'),
    path('users', views.getUser, name='get-user'),
    path('update-author', views.UpdateAuthor, name='update-author'),
    path('following', views.getFollowing, name='following'),
]


urlpatterns = format_suffix_patterns(urlpatterns)
