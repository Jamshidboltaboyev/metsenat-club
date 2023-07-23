from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.sponsor.models import Sponsor
from .models import Student, Transfer
from .serializers import (
    StudentsListSerializers,
    StudentsCreateSerializers,
    StudentsRetrieveSerializers,
    AddSponsorToStudentSerializers,
    DeleteSponsorToStudentSerializers, UpdateSponsorToStudentSerializers
)
from .validators import create_transfer, update_transfer


class StudentsListAPIView(ListAPIView):
    serializer_class = StudentsListSerializers
    http_method_names = ['get']
    authentication_classes = (JWTAuthentication,)

    def get_queryset(self):
        queryset = Student.objects.all()
        university = self.request.query_params.get('university', None)
        degree = self.request.query_params.get('degree', None)
        if degree is not None:
            queryset = queryset.filter(degree=degree)

        if university is not None:
            queryset = queryset.filter(university=university)
        return queryset


class StudentsRetrieveAPIView(RetrieveAPIView):
    serializer_class = StudentsRetrieveSerializers
    queryset = Student.objects.all()
    authentication_classes = (JWTAuthentication,)


class StudentsCreateAPIView(CreateAPIView):
    serializer_class = StudentsCreateSerializers
    queryset = Student.objects.all()
    authentication_classes = (JWTAuthentication,)


class AddSponsorToStudentCreateAPIView(CreateAPIView):
    serializer_class = AddSponsorToStudentSerializers
    queryset = Transfer.objects.all()
    authentication_classes = (JWTAuthentication,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            student = get_object_or_404(Student, pk=serializer.data['student_id'])
            sponsor = get_object_or_404(Sponsor, id=serializer.data['sponsor_id'])
            amount = serializer.data['amount']
            create_transfer(student=student, sponsor=sponsor, amount=amount)

        return Response(status=status.HTTP_201_CREATED)


class UpdateSponsorToStudentCreateAPIView(UpdateAPIView):
    serializer_class = UpdateSponsorToStudentSerializers
    queryset = Transfer.objects.all()
    authentication_classes = (JWTAuthentication,)

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            transfer = get_object_or_404(Transfer, pk=kwargs.get('pk'))
            amount = serializer.data['amount']
            with transaction.atomic():
                update_transfer(transfer, amount)
        return Response(status=status.HTTP_200_OK)


class DeleteSponsorToStudentCreateAPIView(DestroyAPIView):
    serializer_class = DeleteSponsorToStudentSerializers
    queryset = Transfer.objects.all()
    authentication_classes = (JWTAuthentication,)

    def delete(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            student = get_object_or_404(Student, pk=serializer.data['student_id'])
            sponsor = get_object_or_404(Sponsor, pk=serializer.data['sponsor_id'])
            transfer = get_object_or_404(Transfer, student_id=student.id, sponsor_id=sponsor.id)

            student.balance -= transfer.amount
            sponsor.balance += transfer.amount

            transfer.delete()
            student.save()
            sponsor.save()

        return Response(status=status.HTTP_200_OK)
