from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from django.views import View
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .serializers import CotisationSerializer, CotisationSimplifiedSerializer, CotisationSimplified
from .models import Cotisation
from django.contrib.auth.models import User
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.renderers import JSONRenderer
from dateutil.relativedelta import relativedelta
from datetime import date
from userProfile.models import UserProfile


class CotisationPage(View):
    template_name = 'dashboard/cotisations/index.html'

    @method_decorator(login_required(login_url='/login'))
    def get(self, request, selected_user_id):
        return render(request, self.template_name, {'selected_user_id': selected_user_id})


class CotisationSimplifedAPI(viewsets.ModelViewSet):

    # renderer_classes = [JSONRenderer]
    queryset = Cotisation.objects.all().order_by('-created_at')
    serializer_class = CotisationSimplifiedSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, url_path="get_cotisations/(?P<user_id>[0-9]+)")
    def get_cotisations(self, request, user_id=None):

        user = User.objects.get(pk=user_id)
        cotisations = Cotisation.objects.filter(user=user).order_by('-created_at')
        userProfile = UserProfile.objects.get(user=user)

        base = date.today()
        base = base.replace(day=1)

        diff = relativedelta(base, userProfile.start_date)
        months = diff.years*12 + diff.months

        dates = [(userProfile.start_date + relativedelta(months=x)) for x in range(months+4)]

        cotisation_list = []
        for d in dates:
            exists = False
            for cotisation in cotisations:
                if d == cotisation.month:
                    cotisation_list.append(CotisationSimplified(date=d, cotisation=cotisation))
                    exists = True
            if not exists:
                cotisation_list.append(CotisationSimplified(date=d, cotisation=None))

        return Response(CotisationSimplifiedSerializer(cotisation_list, many=True).data)

    def create(self, request, *args, **kwargs):

        serializer_context = {
            'request': request,
        }

        serializer = CotisationSerializer(data=request.data, context=serializer_context)
        if serializer.is_valid():
            serializer.save()

            cotisationOject = Cotisation.objects.get(pk=serializer.data['id'])
            cotisation = CotisationSimplified(date=serializer.data['month'], cotisation=cotisationOject)
            cotSer = CotisationSimplifiedSerializer(cotisation)

            return Response(cotSer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):

        cotisation = Cotisation.objects.get(pk=kwargs['pk'])
        cotisation.delete()

        return Response({}, status=status.HTTP_200_OK)
