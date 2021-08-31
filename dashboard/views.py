from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework import viewsets
from cotisation.models import Cotisation
from parameter.models import Parameter
from rest_framework import permissions


class DashboardPage(View):
    template_name = 'dashboard/home.html'

    @method_decorator(login_required(login_url='/login'))
    def get(self, request):
        return render(request, self.template_name, {})
