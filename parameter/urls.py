from django.urls import include, path, re_path
from rest_framework import routers
from .views import ParameterPage, ParameterAPI

router = routers.DefaultRouter()
router.register(r'api', ParameterAPI)

urlpatterns = [
    re_path(r'', include(router.urls)),
    re_path(r'^index', ParameterPage.as_view()),
]
