from django.shortcuts import render
from django.shortcuts import render
from .models import Transaction, TransactionLineItem, InventoryItem
from .serializers import (
    InventoryItemDetailSerializer,
    MultipleInventoryItemSeriaizer,
    TransactionDetailSerializer,
    TransactionSerializer,
    LineItemSerializer,
    InventoryItemSerializer,
    TransactionWithLineItemSerializer,
    LineItemCreateSerializer,
    LineItemWithInventoryItemSerializer,
)
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, status
from rest_framework.response import Response


class TransactionView(generics.CreateAPIView):
    serializer_class = TransactionSerializer

    def post(self, request, *args, **kwargs):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            transaction = serializer.save()
            serializer = TransactionWithLineItemSerializer(transaction)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LineItemView(generics.CreateAPIView):
    serializer_class = LineItemCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = LineItemCreateSerializer(data=request.data)
        if serializer.is_valid():
            line_item = serializer.save()
            serializer = LineItemCreateSerializer(line_item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InventoryItemView(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        serializer = MultipleInventoryItemSeriaizer(data=request.data)
        if serializer.is_valid():
            inventory_item = serializer.save()
            serializer = LineItemWithInventoryItemSerializer(inventory_item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionDeleteView(generics.DestroyAPIView):
    queryset = Transaction.objects.all()

    def delete(self, request, *args, **kwargs):
        try:
            transaction = Transaction.objects.get(id=kwargs["pk"])
        except Transaction.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"error": "transaction not found"},
            )
        qs = TransactionLineItem.objects.filter(item=transaction)
        if qs.exists():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"error": "cannot delete because line items exists"},
            )
        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TransactionDetailView(generics.RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        try:
            transaction = Transaction.objects.get(id=kwargs["pk"])
        except Transaction.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"error": "transaction not found"},
            )
        line_items = TransactionLineItem.objects.filter(item=transaction)
        inventory_items = []
        for item in line_items:
            inventory_item = InventoryItem.objects.filter(inventory_item=item)
            inventory_items.append(
                InventoryItemDetailSerializer(inventory_item, many=True).data
            )
        custom_response = {
            "transaction": TransactionDetailSerializer(transaction).data,
            "line_items": LineItemCreateSerializer(line_items, many=True).data,
            "inventory_items": inventory_items,
        }
        return Response(custom_response, status=status.HTTP_200_OK)
