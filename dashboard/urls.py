from django.urls import path, re_path
from .views import DashboardPage
from . import views

urlpatterns = [
    re_path(r'', DashboardPage.as_view()),
]
