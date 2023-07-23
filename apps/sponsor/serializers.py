from rest_framework import serializers
from .models import Sponsor


class AppyForSponsorshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = (
            'sponsor_type', 'full_name',
            'balance', 'phone_number', 'company'
        )


class SponsorsListSerializers(serializers.ModelSerializer):
    spend_sum = serializers.FloatField(read_only=True, default=0)

    class Meta:
        model = Sponsor
        fields = ('id', 'full_name', 'phone_number', 'balance', 'created_at', 'status', 'spend_sum')


class SponsorsRetrieveSerializers(serializers.ModelSerializer):
    spend_sum = serializers.FloatField(read_only=True)

    class Meta:
        model = Sponsor
        fields = ('id', 'full_name', 'phone_number', 'balance', 'created_at', 'status', 'spend_sum')


class SponsorsUpdateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = ('sponsor_type', 'full_name', 'phone_number', 'balance', 'status', 'company')
