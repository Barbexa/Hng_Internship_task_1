from django.urls import path
from .views import StringListCreateView, StringDetailView, StringListView


urlpatterns =[
    path('strings/', StringListCreateView.as_view(), name='string-list-create'),
    path('strings/', StringListView.as_view(), name='string-list-filter'),
    path('strings/<str:pk>/', StringDetailView.as_view(), name='string-detail'),


]