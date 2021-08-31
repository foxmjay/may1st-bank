from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .serializers import UserProfileSerializer
from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.renderers import JSONRenderer
from django.views import View
from .models import UserProfile


class UserProfilePage(View):
    template_name = 'dashboard/userprofiles/index.html'

    @method_decorator(login_required(login_url='/login'))
    def get(self, request, selected_user_id):
        return render(request, self.template_name, {'selected_user_id': selected_user_id})


class UserProfileAPI(viewsets.ModelViewSet):

    # renderer_classes = [JSONRenderer]

    queryset = UserProfile.objects.all().order_by('-created_at')
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, url_path="get_userprofile_by_userid/(?P<user_id>[0-9]+)")
    def get_userprofile_by_userid(self, request, user_id=None):

        user = User.objects.get(pk=user_id)
        userProfile = UserProfile.objects.filter(user=user).first()
        userProfileSer = UserProfileSerializer(userProfile)

        return Response(userProfileSer.data)
