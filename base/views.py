from rest_framework import viewsets
from .models import Partner, BankCashback
from .serializers import PartnerSerializer, BankCashbackSerializer
from rest_framework.response import Response
from rest_framework import status

class PartnerViewSet(viewsets.ModelViewSet):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):  # Check if the request data is a list
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return super(PartnerViewSet, self).create(request, *args, **kwargs)

class BankCashbackViewSet(viewsets.ModelViewSet):
    queryset = BankCashback.objects.all()
    serializer_class = BankCashbackSerializer

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):  # Check if the request data is a list
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return super(BankCashbackViewSet, self).create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save()
