from transaction.models import TransactionTable
from transaction import views
from django.urls import path, include
from rest_framework import routers
from django.contrib import admin

router = routers.DefaultRouter()
router.register(r'transactions', views.TransactionViewSet,
                basename='TransactionTable')
router.register(r'transactionslistitem', views.TransactionListItemViewSet,
                basename='TransactionLineItem')
router.register(r'addinventory', views.InventoryViewSet,
                basename='InventoryItem')
router.register(r'fulldetails', views.ViewFullTransactionDetailViewSet,
                basename='FullDetails')

# Wire API using automatic URL routing.
# login URLs for the browsable API.
transaction_urls = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
