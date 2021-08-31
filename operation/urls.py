from django.urls import include, path, re_path
from rest_framework import routers
from .views import OperationAPI, OperationPage
router = routers.DefaultRouter()
router.register(r'api', OperationAPI,'operations-list')
from . import views

urlpatterns = [
    re_path(r'', include(router.urls)),
    re_path(r'^index', OperationPage.as_view()),
]

