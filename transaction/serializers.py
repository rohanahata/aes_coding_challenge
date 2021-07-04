from .models import *
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

class TransectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ['transaction_number',]
        
    def to_representation(self, instance):
        rep = super(TransectionSerializer, self).to_representation(instance)
        rep['company'] = instance.company.name
        rep['branch'] = instance.branch.short_name
        rep['department'] = instance.department.name
        return rep
    

class TransactionLineItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = TransactionLineItemDetail
        fields = '__all__'
        
    def to_representation(self, instance):
        rep = super(TransactionLineItemSerializer, self).to_representation(instance)
        rep['article'] = instance.article.name
        rep['colour'] = instance.colour.name
        return rep

class InventoryItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = InventoryItem
        fields = '__all__'
        
    def to_representation(self, instance):
        rep = super(InventoryItemSerializer, self).to_representation(instance)
        rep['article'] = instance.article.name
        rep['colour'] = instance.colour.name
        rep['company'] = instance.company.name
        return rep
    
class ViewFullTransactionDetailsSerializer(serializers.ModelSerializer):
    line_items  = TransactionLineItemSerializer(source = 'tr_item_detail.all',many = True)
    inventory_items = SerializerMethodField()

    class Meta:
        model = Transaction
        fields = '__all__'
        
    def to_representation(self, instance):
        rep = super(ViewFullTransactionDetailsSerializer, self).to_representation(instance)
        rep['company'] = instance.company.name
        rep['branch'] = instance.branch.short_name
        rep['department'] = instance.department.name
        return rep
    
    def get_inventory_items(self,obj):
        data = []
        for dt in obj.tr_item_detail.all():
            for inv in dt.inv_line.all():
                sr = InventoryItemSerializer(instance = inv)
                data.append(sr.data)
        return data        