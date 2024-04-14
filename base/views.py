from rest_framework import viewsets
from .models import Partner, BankCashback
from .serializers import PartnerSerializer, BankCashbackSerializer

class PartnerViewSet(viewsets.ModelViewSet):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer

class BankCashbackViewSet(viewsets.ModelViewSet):
    queryset = BankCashback.objects.all()
    serializer_class = BankCashbackSerializer
