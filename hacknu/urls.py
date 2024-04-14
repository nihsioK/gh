from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from base.views import PartnerViewSet, BankCashbackViewSet, CardsViewSet
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

router = DefaultRouter()
router.register(r'partners', PartnerViewSet)
router.register(r'bankcashbacks', BankCashbackViewSet)
router.register(r'cards', CardsViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('', include(router.urls)),
]
