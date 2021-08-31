from django.urls import include, path, re_path
from rest_framework import routers
from .views import CotisationPage, CotisationSimplifedAPI

router = routers.DefaultRouter()
router.register(r'api', CotisationSimplifedAPI, 'cotisation-list')

urlpatterns = [
    re_path(r'', include(router.urls)),
    re_path(r'^index/(?P<selected_user_id>[0-9]+)', CotisationPage.as_view()),
]
