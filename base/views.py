from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from .models import Partner, BankCashback, Cards
from .serializers import PartnerSerializer, BankCashbackSerializer, CardsSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.views import APIView

# Custom Pagination Class
class SmallSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

# Applying Custom Pagination to a ViewSet
class PartnerViewSet(viewsets.ModelViewSet):
    queryset = Partner.objects.all()
    serializer_class = PartnerSerializer
    pagination_class = SmallSetPagination  # Apply custom pagination

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return super(PartnerViewSet, self).create(request, *args, **kwargs)
        
    @action(detail=False, methods=['delete'])
    def delete_all(self, request):
        Partner.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class BankCashbackViewSet(viewsets.ModelViewSet):
    queryset = BankCashback.objects.all()
    serializer_class = BankCashbackSerializer
    pagination_class = SmallSetPagination  # Apply custom pagination

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return super(BankCashbackViewSet, self).create(request, *args, **kwargs)
        
    @action(detail=False, methods=['delete'])
    def delete_all(self, request):
        Cards.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
 

class CardsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Cards.objects.all()
    serializer_class = CardsSerializer
    pagination_class = SmallSetPagination  # Apply custom pagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CategorySearchView(APIView):

    def get(self, request):
        # Retrieve the 'main_category' from query parameters
        main_category = request.query_params.get('main_category', None)
        
        if not main_category:
            return Response({"error": "Main category parameter is required."}, status=400)

        # Filter Partner and BankCashback by 'main_category'
        partners = Partner.objects.filter(main_category=main_category)
        bankcashbacks = BankCashback.objects.filter(main_category=main_category)

        # Serialize the data
        partner_serializer = PartnerSerializer(partners, many=True)
        bankcashback_serializer = BankCashbackSerializer(bankcashbacks, many=True)

        # Combine the results
        result = {
            'partners': partner_serializer.data,
            'bank_cashbacks': bankcashback_serializer.data
        }

        return Response(result)

