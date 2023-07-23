from django.urls import path

from .views import AppyForSponsorShipCreateAPIView, SponsorsListAPIView, SponsorsRetrieveAPIView, SponsorsUpdateAPIView

urlpatterns = [
    path('apply', AppyForSponsorShipCreateAPIView.as_view(), name='appy-for-sponsorship'),
    path('list/', SponsorsListAPIView.as_view(), name='sponsors-list'),
    path('get/<int:pk>/', SponsorsRetrieveAPIView.as_view(), name='sponsor-detail'),
    path('update/<int:pk>/', SponsorsUpdateAPIView.as_view(), name='sponsor-update')
]
