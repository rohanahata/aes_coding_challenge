from .serializers import *
from rest_framework import response, status, viewsets
from .models import *

class TransactionView(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransectionSerializer

class TransactionLineItemView(viewsets.ModelViewSet):
    queryset = TransactionLineItemDetail.objects.all()
    serializer_class = TransactionLineItemSerializer

class InventoryItemView(viewsets.ModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer

class ViewFullTransactionDetailsView(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = ViewFullTransactionDetailsSerializer