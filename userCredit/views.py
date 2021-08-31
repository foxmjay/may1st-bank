from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from django.views import View
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .serializers import UserCreditSimplified, UserCreditSimplifiedSerializer, UserCreditSerializer
from credit.models import Credit
from .models import UserCredit
from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.renderers import JSONRenderer
from django.http import JsonResponse
from dateutil.relativedelta import relativedelta
from datetime import date


class UserCreditPage(View):
    template_name = 'dashboard/user_credits/index.html'

    @method_decorator(login_required(login_url='/login'))
    def get(self, request, credit_id=None):
        return render(request, self.template_name, {'credit_id': credit_id})


class UserCreditSimplifedAPI(viewsets.ModelViewSet):

    # renderer_classes = [JSONRenderer]

    queryset = Credit.objects.all().order_by('-created_at')
    serializer_class = UserCreditSimplifiedSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, url_path="get_user_credits/(?P<credit_id>[0-9]+)")
    def get_user_credits(self, request, credit_id=None):

        credit = Credit.objects.get(pk=credit_id)
        userCredits = UserCredit.objects.filter(credit=credit).order_by('-created_at')

        base = date.today()
        base = base.replace(day=1)

        diff = relativedelta(base, credit.start_date)
        months = diff.years * 12 + diff.months
        dates = [(credit.start_date + relativedelta(months=x)) for x in range(months+4)]

        userCredit_list = []
        for d in dates:
            exists = False
            for uc in userCredits:
                if d == uc.month:
                    userCredit_list.append(UserCreditSimplified(date=d, cotisation=uc))
                    exists = True
            if not exists:
                userCredit_list.append(UserCreditSimplified(date=d, cotisation=None))

        return Response(UserCreditSimplifiedSerializer(userCredit_list, many=True).data)

    def create(self, request, *args, **kwargs):

        serializer_context = {
            'request': request,
        }

        serializer = UserCreditSerializer(data=request.data, context=serializer_context)
        if serializer.is_valid():
            serializer.save()

            userCreditOject = UserCredit.objects.get(pk=serializer.data['id'])
            userCreditSimplified = UserCreditSimplified(date=serializer.data['month'], cotisation=userCreditOject)
            cotSer = UserCreditSimplifiedSerializer(userCreditSimplified)

            return Response(cotSer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):

        userCredit = UserCredit.objects.get(pk=kwargs['pk'])
        userCredit.delete()
        return Response({}, status=status.HTTP_200_OK)
