from django.urls import path
from .views import ClientTransactionsAPI

urlpatterns = [
    path('api/transactions/<int:client_id>/', ClientTransactionsAPI.as_view(), name='client-transactions'),
]
