from django.urls import include, path, re_path
from rest_framework import routers
from .views import UserAPI, UsersPage

router = routers.DefaultRouter()
router.register(r'api', UserAPI)

urlpatterns = [
    re_path(r'', include(router.urls)),
    re_path(r'^index', UsersPage.as_view()),
]
