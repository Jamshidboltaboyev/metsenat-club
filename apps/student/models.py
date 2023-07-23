from django.contrib.auth import get_user_model
from django.db import models

from apps.sponsor.models import Sponsor


class University(models.Model):
    name = models.CharField(max_length=256)
    address = models.CharField(max_length=256)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Student(models.Model):
    class DegreeType(models.TextChoices):
        BACHELOR = "BACHELOR", "Bakalavr"
        MASTER = "MASTER", "Magister"

    university = models.ForeignKey(University, on_delete=models.CASCADE)
    degree = models.CharField(max_length=10, choices=DegreeType.choices)

    full_name = models.CharField(max_length=100)
    balance = models.PositiveIntegerField(default=0)
    phone_number = models.CharField(max_length=256)
    contract_sum = models.PositiveIntegerField()
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    initiator = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, editable=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.full_name

    @property
    def university_name(self):
        return self.university.name


class Transfer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT, related_name='students_transfer')
    sponsor = models.ForeignKey(Sponsor, on_delete=models.PROTECT, related_name='sponsor_transfer')
    amount = models.PositiveIntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    initiator = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, editable=False)
