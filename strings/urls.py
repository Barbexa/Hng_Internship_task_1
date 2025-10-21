from django.urls import path
from .views import StringListCreateAPIView, StringRetrieveDestroyView, NaturalLanguageView


urlpatterns =[
    path('strings/', StringListCreateAPIView.as_view(), name='string-list-create'),
    path('strings/<str:pk>/', StringRetrieveDestroyView.as_view(), name='string-detail-delete'),
    path('strings/filter-by-natural-language', NaturalLanguageView.as_view(), name='natural-language-filter' ),
    


]