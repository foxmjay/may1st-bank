from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from django.views import View
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Parameter
from .serializers import ParameterSerializer
from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser
from rest_framework import status


class ParameterPage(View):
    template_name = 'dashboard/parameters/index.html'

    @method_decorator(login_required(login_url='/login'))
    def get(self, request):
        return render(request, self.template_name, {})


class ParameterAPI(viewsets.ModelViewSet):

    queryset = Parameter.objects.all()
    serializer_class = ParameterSerializer
    permission_classes = [permissions.IsAuthenticated]
