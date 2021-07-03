from django.db.models import fields
from rest_framework import serializers

from transaction.models import TransactionTable, TransactionLineItem, InventoryItem


class TransactionLineItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionLineItem
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionTable
        fields = '__all__'


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = '__all__'


class ViewFullTransactionDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = InventoryItem
        fields = '__all__'
        depth = 2
