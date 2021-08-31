from django.urls import include, path, re_path
from rest_framework import routers
from .views import UserCreditPage, UserCreditSimplifedAPI

router = routers.DefaultRouter()
router.register(r'api', UserCreditSimplifedAPI, 'cotisation-list')

urlpatterns = [
    re_path(r'', include(router.urls)),
    re_path(r'^index/(?P<credit_id>[0-9]+)', UserCreditPage.as_view()),
]
