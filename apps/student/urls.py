from django.urls import path
from .views import (
    StudentsListAPIView,
    StudentsRetrieveAPIView,
    StudentsCreateAPIView,
    AddSponsorToStudentCreateAPIView,
    DeleteSponsorToStudentCreateAPIView,
    UpdateSponsorToStudentCreateAPIView
)

urlpatterns = [
    path('list/', StudentsListAPIView.as_view(), name='students-list'),
    path('get/<int:pk>/', StudentsRetrieveAPIView.as_view(), name='student-detail'),
    path('create/', StudentsCreateAPIView.as_view(), name='student-create'),

    path("sponsorship/attach/", AddSponsorToStudentCreateAPIView.as_view(), name='attach-sponsor-to-student'),
    path("sponsorship/detach/", DeleteSponsorToStudentCreateAPIView.as_view(), name='detach-sponsor-to-student'),
    path('sponsorship/update/<int:pk>', UpdateSponsorToStudentCreateAPIView.as_view(), name='update-sponsorship')
]
