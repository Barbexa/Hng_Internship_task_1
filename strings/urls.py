from django.urls import path
from .views import StringListCreateView, StringListView, StringRetrieveDestroyView, NaturalLanguageView


urlpatterns =[
    path('strings/create/', StringListCreateView.as_view(), name='string-list-create'),
    path('strings/', StringListView.as_view(), name='string-list-filter'),
    path('strings/<str:pk>/', StringRetrieveDestroyView.as_view(), name='string-detail-delete'),
    path('strings/filter-by-natural-language', NaturalLanguageView.as_view(), name='natural-language-filter' ),


]