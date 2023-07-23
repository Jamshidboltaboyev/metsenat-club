from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.sponsor.models import Sponsor
from apps.student.models import Transfer, Student


def create_transfer(student, sponsor, amount: int):
    if sponsor.status != Sponsor.SponsorStatus.APPROVED:
        raise ValidationError({'msg': "Sponsor balance is not active"})

    if sponsor.balance < amount:
        raise ValidationError({'msg': "Sponsor doesn't have enough money"})

    if student.balance + amount > student.contract_sum:
        raise ValidationError({"msg": "has gone over the amount of the loan contract"})

    with transaction.atomic():
        sponsor.balance -= amount
        student.balance += amount

        transfer = Transfer(sponsor_id=sponsor.id, student_id=student.id, amount=amount)

        sponsor.save()
        student.save()
        transfer.save()


def update_transfer(transfer: Transfer, amount: int):
    student = Student.objects.get(id=transfer.student_id)
    sponsor = Student.objects.get(id=transfer.sponsor_id)

    if transfer.amount > amount:
        student.balance -= amount
        sponsor.balance += amount
        transfer.amount = amount
    elif transfer.amount < amount:
        diff = amount - transfer.amount
        if sponsor.balance < diff:
            raise ValidationError({'msg': "Sponsor doesn't have enough money"})
        if student.balance + amount > student.contract_sum:
            raise ValidationError({"msg": "has gone over the amount of the loan contract"})
        student.balance += diff
        sponsor.balance -= diff
        transfer.amount = amount

    student.save()
    sponsor.save()
    transfer.save()
