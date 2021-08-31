from django.urls import include, path, re_path
from rest_framework import routers
from .views import CreditPage, CreditAPI

router = routers.DefaultRouter()
router.register(r'api', CreditAPI, 'credit-list')

urlpatterns = [
    re_path(r'', include(router.urls)),
    re_path(r'^index/$', CreditPage.as_view()),
    re_path(r'^index/(?P<selected_user_id>\d+)', CreditPage.as_view()),
]
