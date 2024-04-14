from rest_framework import serializers
from .models import Partner, BankCashback

class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = '__all__'

class BankCashbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankCashback
        fields = '__all__'
