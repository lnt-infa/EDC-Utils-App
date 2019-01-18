'''
Created on Dec 28, 2018

Url definition for the EDC Env Manager app

@author: lntrapad
'''

from django.urls import path,include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    # ex: /edcmgmt/
    path('', views.index, name='index'),

    # ex: /edcmgmt/environment
    path('environment/', views.envs, name='Env'),
    path('environment/new/', views.new_env, name='New Env'),
    path('environment/<int:env_id>/', views.env, name='Env'),
    path('environment/<int:env_id>/edit', views.edit_env, name='Edit Env'),
    path('environment/delete/<int:env_id>', views.del_env, name='env-del'),

    # ex: /edcmgmt/resource
    path('resource/ext', views.resource_ext_all, name='res-ext'),
    path('resource/ext/<int:env_id>/', views.resource_ext, name='res-ext'),
    path('resource/saved', views.resource_saved, name='res-saved'),
    path('resource/delete/<int:res_id>', views.resource_del, name='res-del'),
    path('resource/deploy', views.resource_deploy, name='res-deploy'),
    path('resource/deploy_check/<int:env_id>/<int:res_id>', views.resource_deploy_checks, name='res-deploy-checks'),
    path('resource/<int:env_id>/<slug:resource_name>', views.resource_detail, name='res-detail'),
    path('resource/export/<int:env_id>/<slug:resource_name>', views.resource_export, name='res-export'),
    path('resource/save/<int:env_id>/<slug:resource_name>', views.resource_save, name='res-save'),

    # ex: /edcmgmt/attributes
    path('attribute/ext/', views.attributes_ext_all, name='attr-ext'),
    path('attribute/<int:env_id>/<str:attr_name>', views.attribute_ext_detail, name='attr-detail'),
    path('attribute/ext/<int:env_id>/', views.attributes_ext, name='attr-ext'),
    path('attribute/save/<int:env_id>/<str:attr_name>', views.attributes_save, name='attr-save'),
    path('attribute/export/<int:env_id>/<str:attr_name>', views.attributes_export, name='attr-export'),
    path('attribute/saved/', views.attributes_saved, name='attr-saved'),
    path('attribute/delete/<int:attr_id>', views.attributes_del, name='attr-del'),
    path('attribute/deploy', views.attributes_deploy, name='attr-deploy'),
    path('attribute/deploy_check/<int:env_id>/<int:attr_id>', views.attributes_deploy_checks, name='attr-deploy-checks'),

    # ex: /edcmgmt/reusableconfig
    path('reusableconfig/<int:env_id>/', views.reusableconfig, name='reuse-conf'),
]
