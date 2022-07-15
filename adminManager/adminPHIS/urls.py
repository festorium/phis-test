from django.contrib import admin
from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('microservice-list/', views.microserviceList, name='microservice-list'),
    path('microservice-add/', views.microserviceAdd, name='microservice-add'),
    path('microservice-edit/<int:pk>/', views.microserviceEdit, name='microservice-edit'),
    path('microservice-remove/<int:pk>/', views.microserviceRemove, name='microservice-remove'),

    path('role-list/', views.roleList, name='role-list'),
    path('role-add/', views.roleAdd, name='role-add'),
    path('role-edit/<int:pk>/', views.roleEdit, name='role-edit'),
    path('rolefunc-list/', views.roleFunctionList, name='rolefunc-list'),
    path('rolefunc-add/', views.roleFunctionAdd, name='role-add'),

    path('menu-add/', views.menuAdd, name='menu-add'),
    path('menu-list/', views.menuList, name='menu-list'),
    path('menu-edit/<int:pk>/', views.menuEdit, name='menu-edit'),
    path('menu-remove/<int:pk>/', views.menuRemove, name='menu-remove'),

    path('submenu-add/', views.submenuAdd, name='submenu-add'),
    path('submenu-edit/<int:pk>/', views.submenuEdit, name='submenu-edit'),
    path('submenu-remove/<int:pk>/', views.submenuRemove, name='submenu-remove'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
