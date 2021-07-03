

from transaction import serializers

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse

from transaction.models import TransactionTable, TransactionLineItem, InventoryItem
from rest_framework import viewsets
from transaction.serializers import (
    TransactionSerializer, TransactionLineItemSerializer, InventorySerializer, ViewFullTransactionDetailsSerializer,)
from rest_framework.response import Response

# Create your views here.


class TransactionViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = TransactionTable.objects.all()
        serializer = TransactionSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


class TransactionListItemViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = TransactionLineItem.objects.all()
        serializer = TransactionLineItemSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TransactionLineItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


class InventoryViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = InventoryItem.objects.all()
        serializer = InventorySerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = InventorySerializer(
            data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201, safe=False)
        return JsonResponse(serializer.errors, status=400)


class ViewFullTransactionDetailViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = InventoryItem.objects.all()
        serializer = ViewFullTransactionDetailsSerializer(queryset, many=True)
        return Response(serializer.data)
