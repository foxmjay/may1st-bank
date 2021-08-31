from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework import viewsets
from .serializers import OperationSerializer, GlobalStatsSerializer
from cotisation.models import Cotisation
from parameter.models import Parameter
from rest_framework import permissions
from django.db.models import Count, Sum
from django.contrib.auth.models import User
from userCredit.models import UserCredit
from credit.models import Credit
from rest_framework.decorators import action
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


class OperationPage(View):
    template_name = 'dashboard/operations/index.html'

    @method_decorator(login_required(login_url='/login'))
    def get(self, request):
        return render(request, self.template_name, {})


class OperationAPI(viewsets.ModelViewSet):

    http_method_names = ['get']
    serializer_class = OperationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):

        queryset = Cotisation.objects.raw('SELECT auth_user.id , auth_user.first_name, auth_user.last_name , \
            ifnull((SELECT SUM(cotisation_cotisation.amount) from cotisation_cotisation where cotisation_cotisation.user_id = auth_user.id),0 ) as sumAmount,\
            ifnull( (select credit_credit.amount - SUM(userCredit_usercredit.amount) from userCredit_usercredit \
            join credit_credit on credit_credit.id = userCredit_usercredit.credit_id \
            where credit_credit.status = "inprogress" and credit_credit.user_id=auth_user.id group by userCredit_usercredit.credit_id \
            ),0 )as creditLeft,  \
            (select userProfile_userprofile.amount from userProfile_userprofile where userProfile_userprofile.user_id = auth_user.id) as cotisation_amount, \
            ( (select 1 + TIMESTAMPDIFF(MONTH,userProfile_userprofile.start_date,now()) from userProfile_userprofile where userProfile_userprofile.user_id = auth_user.id ) * ( select cotisation_amount) - (select sumAmount) ) as amountLeft \
            FROM auth_user  \
            group by auth_user.id')
        return queryset

    @action(detail=False, url_path="get_global_stats")
    def get_global_stats(self, request):

        userCount = User.objects.all().count()
        supposedGlobalSolde = Parameter.supposedAmount()*userCount

        globalStates = []

        globalSolde = Cotisation.objects.all().aggregate(sumAmount=Sum('amount'))['sumAmount']

        if globalSolde:
            globalSoldeLeft = supposedGlobalSolde - globalSolde

        globalCredit = Credit.objects.filter(status="inprogress").aggregate(sumAmount=Sum('amount'))['sumAmount']
        globalCredit = globalCredit if globalCredit else 0.0

        globalCreditLeft = UserCredit.objects.filter(credit__status="inprogress").aggregate(summs=Sum('amount'))['summs']

        if globalCreditLeft:
            globalCreditLeft = globalCredit - globalCreditLeft
        else:
            globalCreditLeft = 0

        globalStates.append({'title': 'Solde Globale', 'data': globalSolde})
        globalStates.append({'title': 'Montant Cotisation Restant', 'data': globalSoldeLeft})
        globalStates.append({'title': 'Montant total des credits', 'data': globalCredit})
        globalStates.append({'title': 'Montant credit restant', 'data': globalCreditLeft})
        globstatsSer = GlobalStatsSerializer(globalStates, many=True)

        return Response(globstatsSer.data)
