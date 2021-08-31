from django.urls import include, path, re_path
from rest_framework import routers
from .views import DashboardLogin, DashboardLogout

urlpatterns = [
    re_path(r'^$', DashboardLogin.as_view()),
    re_path(r'^login', DashboardLogin.as_view()),
    re_path(r'^logout', DashboardLogout.as_view()),
]
