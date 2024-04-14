from django.urls import path
from .views import CategorySearchView

urlpatterns = [
    path('search-by-category/', CategorySearchView.as_view(), name='search-by-category'),
    # include other URL patterns
]
