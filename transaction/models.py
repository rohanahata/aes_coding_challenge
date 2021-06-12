from django.db import models


# Masters required in transaction models
class BranchMaster(models.Model):
    short_name = models.CharField(max_length=10, unique=True)
    contact_person_name = models.CharField(max_length=20)
    gst_number = models.CharField(max_length=20)
    address1 = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=10)
    mobile = models.CharField(blank=True, null=True, max_length=10)


class DepartmentMaster(models.Model):
    name = models.CharField(max_length=20, unique=True)


class CompanyLedgerMaster(models.Model):
    name = models.CharField(max_length=32, unique=True)
    gst_number = models.CharField(max_length=20, unique=True)
    supplier_status = models.BooleanField(default=False)
    address1 = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=10)
    mobile = models.CharField(max_length=10)
    remarks = models.CharField(max_length=200, blank=True)


class ArticleMaster(models.Model):
    name = models.CharField(max_length=80, unique=True)
    short_name = models.CharField(max_length=50, unique=True)
    blend_pct = models.CharField(max_length=50)
    twists = models.PositiveIntegerField(blank=True, null=True)
    remarks = models.CharField(max_length=64, blank=True)


class ColorMaster(models.Model):
    article = models.ForeignKey(ArticleMaster, on_delete=models.PROTECT)
    name = models.CharField(max_length=20)
    short_name = models.CharField(max_length=20)
    remarks = models.CharField(max_length=64, blank=True)


class Transaction(models.Model):
    TRANSACTION_CHOICES = (
        ("pending", "pending"),
        ("completed", "completed"),
        ("close", "close"),
    )
    company = models.ForeignKey(CompanyLedgerMaster, on_delete=models.PROTECT)
    branch = models.ForeignKey(BranchMaster, on_delete=models.PROTECT)
    department = models.ForeignKey(DepartmentMaster, on_delete=models.PROTECT)
    transaction_number = models.CharField(max_length=50, unique=True)
    transaction_status = models.CharField(max_length=200, choices=TRANSACTION_CHOICES)
    remarks = models.CharField(max_length=200)


class TransactionLineItem(models.Model):
    UNIT_CHOICES = (("kg", "kg"), ("metre", "metre"))
    item = models.ForeignKey(Transaction, on_delete=models.PROTECT)
    article = models.ForeignKey(ArticleMaster, on_delete=models.PROTECT)
    colour = models.ForeignKey(ColorMaster, on_delete=models.PROTECT)
    date = models.DateTimeField()
    quantity = models.DecimalField(max_digits=5, decimal_places=4)
    rate = models.IntegerField()
    unit = models.CharField(max_length=200, choices=UNIT_CHOICES)


class InventoryItem(models.Model):
    UNIT_CHOICES = (("kg", "kg"), ("metre", "metre"))
    inventory_item = models.ForeignKey(TransactionLineItem, on_delete=models.PROTECT)
    article = models.ForeignKey(ArticleMaster, on_delete=models.PROTECT)
    colour = models.ForeignKey(ColorMaster, on_delete=models.PROTECT)
    company = models.ForeignKey(CompanyLedgerMaster, on_delete=models.PROTECT)
    gross_quantity = models.DecimalField(max_digits=5, decimal_places=4)
    net_quantity = models.DecimalField(max_digits=5, decimal_places=4)
    unit = models.CharField(max_length=200, choices=UNIT_CHOICES)
