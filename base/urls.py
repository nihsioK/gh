from django.urls import path
from .views import CategorySearchView, OpenAIChatView

urlpatterns = [
    path('search-by-category/', CategorySearchView.as_view(), name='search-by-category'),
    path('api/chat/', OpenAIChatView.as_view(), name='chat-api'),
    # include other URL patterns
]
