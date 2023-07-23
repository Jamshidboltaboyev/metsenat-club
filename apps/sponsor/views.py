from django.db.models import Sum
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Sponsor
from .serializers import SponsorsListSerializers, AppyForSponsorshipSerializer, SponsorsRetrieveSerializers


class AppyForSponsorShipCreateAPIView(CreateAPIView):
    serializer_class = AppyForSponsorshipSerializer
    queryset = Sponsor.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SponsorsListAPIView(ListAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorsListSerializers
    authentication_classes = (JWTAuthentication,)

    def list(self, request, *args, **kwargs):
        sponsors = Sponsor.objects.values('sponsor_transfer__id').annotate(
            spend_sum=Sum('sponsor_transfer__amount')).values(
            'id', 'full_name', 'phone_number', 'balance', 'created_at', 'status', 'spend_sum'
        )
        serializers = SponsorsListSerializers(sponsors, many=True)
        return Response(data=serializers.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        if self.request.query_params.get('status'):
            self.queryset = self.queryset.filter(
                status=self.request.query_params.get('status')
            )
        if self.request.query_params.get('date'):
            self.queryset = self.queryset.filter(
                created_at__day=self.request.query_params.get('date')
            )

        if self.request.query_params.get('sum'):
            self.queryset = self.queryset.filter(
                balance=self.request.query_params.get('sum')
            )
        return self.queryset


class SponsorsRetrieveAPIView(RetrieveAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorsRetrieveSerializers
    authentication_classes = (JWTAuthentication,)


class SponsorsUpdateAPIView(UpdateAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorsRetrieveSerializers
    http_method_names = ['put']
    authentication_classes = (JWTAuthentication,)

