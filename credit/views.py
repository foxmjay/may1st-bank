from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from django.views import View
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .serializers import CreditSerializer, CreditSerializerList
from .models import Credit
from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.renderers import JSONRenderer
from django.http import JsonResponse
from dateutil.relativedelta import relativedelta
from datetime import date


class CreditPage(View):
    template_name = 'dashboard/credits/index.html'

    @method_decorator(login_required(login_url='/login'))
    def get(self, request, selected_user_id=None):
        return render(request, self.template_name, {'selected_user_id': selected_user_id})


class CreditAPI(viewsets.ModelViewSet):

    # renderer_classes = [JSONRenderer]

    queryset = Credit.objects.all().order_by('-created_at')
    serializer_class = CreditSerializerList
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, url_path="get_credit_status")
    def get_credit_status(self, request):
        choices = Credit._meta.get_field('status').choices
        return Response(choices)

    def create(self, request, *args, **kwargs):

        serializer_context = {
            'request': request,
        }

        serializer = CreditSerializer(data=request.data, context=serializer_context)
        if serializer.is_valid():
            serializer.save()

            credit_object = Credit.objects.get(pk=serializer.data['id'])
            credit = CreditSerializerList(credit_object)

            return Response(credit.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, url_path="get_credits_by_user/(?P<selected_user_id>[0-9]+)")
    def get_credits_by_user(self, request, selected_user_id=None):

        user = User.objects.filter(id=selected_user_id).first()
        credits = Credit.objects.filter(user=user).order_by('-created_at')
        creditSer = CreditSerializerList(credits, many=True)

        return Response(creditSer.data, status=status.HTTP_201_CREATED)
