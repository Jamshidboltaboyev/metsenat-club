from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='obtain-token'),
    path('reshresh-token/', TokenObtainPairView.as_view(), name='refresh-token'),
]
