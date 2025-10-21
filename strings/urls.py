

# strings/urls.py (Final Corrected Configuration)

from django.urls import path
from .views import StringListCreateAPIView, StringRetrieveDestroyView, NaturalLanguageView 

urlpatterns = [
    # 1. LIST (GET) and CREATE (POST) on the REQUIRED /strings/ path
    path('strings/', StringListCreateAPIView.as_view(), name='string-list-create'), 
    
    # 2. DETAIL (GET) and DELETE (DELETE) on the REQUIRED /strings/{hash}/ path
    path('strings/<str:pk>/', StringRetrieveDestroyView.as_view(), name='string-detail-delete'),
    
    # 3. NATURAL LANGUAGE FILTER
    path('strings/filter-by-natural-language', NaturalLanguageView.as_view(), name='natural-language-filter'),
]