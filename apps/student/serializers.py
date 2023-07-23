from rest_framework import serializers
from .models import Student, Transfer


class StudentsListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'full_name', 'degree', 'university_name', 'balance', 'contract_sum')


class StudentsRetrieveSerializers(serializers.ModelSerializer):
    sponsors = serializers.SerializerMethodField(method_name='sponsors_list', read_only=True)

    class Meta:
        model = Student
        fields = ('id', 'full_name', 'degree', 'university_name', 'balance', 'contract_sum', 'sponsors')

    def sponsors_list(self, obj):
        transfers = Transfer.objects.filter(student_id=obj.id)

        return [{
            'id': transfer.id,
            'sponsor_full_name': transfer.sponsor.full_name,
            'spend_sum': transfer.amount
        } for transfer in transfers]


class StudentsCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('full_name', 'phone_number', 'degree', 'university', 'due_date', 'contract_sum')


class AddSponsorToStudentSerializers(serializers.Serializer):
    student_id = serializers.IntegerField(required=True)
    sponsor_id = serializers.IntegerField(required=True)
    amount = serializers.IntegerField(required=True)


class UpdateSponsorToStudentSerializers(serializers.Serializer):
    amount = serializers.IntegerField(required=True)


class DeleteSponsorToStudentSerializers(serializers.Serializer):
    student_id = serializers.IntegerField(required=True)
    sponsor_id = serializers.IntegerField(required=True)
