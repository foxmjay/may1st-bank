

from django.contrib import admin
from django.urls import path, include, re_path

from rest_framework import routers
#from users.views import UserList

#router = routers.DefaultRouter()
#router.register(r'list', UserList)


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'', include('login.urls')),
    re_path(r'^dashboard/', include('dashboard.urls')),
    re_path(r'^operations/', include('operation.urls')),
    re_path(r'^users/', include('users.urls')),
    re_path(r'^parameters/', include('parameter.urls')),
    re_path(r'^cotisations/', include('cotisation.urls')),
    re_path(r'^credits/', include('credit.urls')),
    re_path(r'^userprofiles/', include('userProfile.urls')),
    re_path(r'^user_credits/', include('userCredit.urls')),


    #path('', include(router.urls)),
]
