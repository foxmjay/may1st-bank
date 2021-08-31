from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from django.views import View
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .serializers import UserSerializer, UserCreateSerializer
from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser
from rest_framework import status
from userProfile.models import UserProfile
from parameter.models import Parameter


class UsersPage(View):
    template_name = 'dashboard/users/index.html'

    @method_decorator(login_required(login_url='/login'))
    def get(self, request):
        return render(request, self.template_name, {})


class UserAPI(viewsets.ModelViewSet):

    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(pk=serializer.data['id'])
            parameters = Parameter.objects.first()
            userProfile = UserProfile(user=user, amount=parameters.cotisation_amount, start_date=parameters.start_date)
            userProfile.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
