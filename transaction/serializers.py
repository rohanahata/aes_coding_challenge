from rest_framework import serializers
from .models import Transaction, TransactionLineItem, InventoryItem


class LineItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionLineItem
        fields = "__all__"

    def create(self, validated_data):
        return TransactionLineItem.objects.create(**validated_data)


class TransactionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"


class LineItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionLineItem
        fields = ("article", "colour", "date", "quantity", "rate", "unit")


class InventoryItemDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = "__all__"


class TransactionSerializer(serializers.ModelSerializer):
    line_items = LineItemSerializer(many=True, write_only=True)

    class Meta:
        model = Transaction
        fields = "__all__"

    def create(self, validated_data):
        line_items = validated_data.pop("line_items", [])
        item = Transaction.objects.create(**validated_data)
        for line_item in line_items:
            line_item["item"] = item
            TransactionLineItem.objects.create(**line_item)
        return item


class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = (
            "article",
            "colour",
            "company",
            "gross_quantity",
            "net_quantity",
            "unit",
        )

    def create(self, validated_data):
        return InventoryItem.objects.create(**validated_data)


class TransactionWithLineItemSerializer(serializers.ModelSerializer):
    line_items = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = "__all__"

    def get_line_items(self, object):
        line_items = TransactionLineItem.objects.filter(item=object)
        return LineItemSerializer(line_items, many=True).data


class MultipleInventoryItemSeriaizer(serializers.ModelSerializer):
    inventory_items = InventoryItemSerializer(many=True, write_only=True)

    class Meta:
        model = TransactionLineItem
        fields = "__all__"

    def create(self, validated_data):
        inventory_items = validated_data.pop("inventory_items", [])
        inventory_item = TransactionLineItem.objects.create(**validated_data)
        for item in inventory_items:
            item["inventory_item"] = inventory_item
            InventoryItem.objects.create(**item)
        return inventory_item


class LineItemWithInventoryItemSerializer(serializers.ModelSerializer):
    inventory_items = serializers.SerializerMethodField()

    class Meta:
        model = TransactionLineItem
        fields = "__all__"

    def get_inventory_items(self, object):
        inventory_items = InventoryItem.objects.filter(inventory_item=object)
        return InventoryItemSerializer(inventory_items, many=True).data
