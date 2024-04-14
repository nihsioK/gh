from rest_framework import serializers
from .models import Partner, BankCashback, Cards

class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = '__all__'

class BankCashbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankCashback
        fields = '__all__'
        
class CardsSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')  # To show the owner's username

    class Meta:
        model = Cards
        fields = ['id', 'bank', 'card', 'owner', 'owner_username']
