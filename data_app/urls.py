from django.urls import path
from .views import ClientTransactionsAPI
from django.contrib import admin

urlpatterns = [
    path('transactions/<int:client_id>/', ClientTransactionsAPI.as_view(), name='client-transactions'),

]
