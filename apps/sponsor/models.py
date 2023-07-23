from django.db import models


class Sponsor(models.Model):
    class SponsorStatus(models.TextChoices):
        PENDING = "PENDING", "Yangi"
        APPROVED = "APPROVED", "Tasdiqlangan"
        CANCELED = "CANCELED", "Bekor qilingan"

    class SponsorType(models.TextChoices):
        LEGAL_ENTITY = "LEGAL_ENTITY", "Yuridik shaxs"
        PHYSICAL_PERSON = "PHYSICAL_PERSON", "Jismoniy shaxs"

    status = models.CharField(max_length=32, choices=SponsorStatus.choices, default=SponsorStatus.PENDING)
    sponsor_type = models.CharField(max_length=15, choices=SponsorType.choices)

    full_name = models.CharField(max_length=100)
    balance = models.PositiveIntegerField()
    phone_number = models.CharField(max_length=50)
    company = models.CharField(max_length=256, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'sponsor'

    def __str__(self):
        return self.full_name
