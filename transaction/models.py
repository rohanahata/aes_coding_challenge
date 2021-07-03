from django.db import models

from django.db import models
from datetime import datetime, date
from django.db.models.deletion import RESTRICT
from django.db.models.fields.related import ForeignKey

# count for transaction token number
count = 0

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

# Create your models here.


class TransactionTable(models.Model):

    PENDING = 'Pending'
    COMPLETED = 'Completed'
    CLOSE = 'Close'
    company = models.ForeignKey(
        CompanyLedgerMaster, on_delete=RESTRICT, related_name='transaction_company')
    branch = models.ForeignKey(
        BranchMaster, on_delete=RESTRICT, related_name='transaction_branch')
    department = models.ForeignKey(
        DepartmentMaster, on_delete=RESTRICT, related_name='transaction_department')
    transaction_number = models.CharField(
        max_length=10, blank=True, editable=True)
    TRANSACTION_STATUS = [
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
        (CLOSE, 'Close'),
    ]
    transaction_status = models.CharField(
        max_length=15,
        choices=TRANSACTION_STATUS,
    )
    remarks = models.CharField(max_length=200, default=None)

    def save(self, *args, **kwargs):
        global count
        count = count + 1
        day_of_year = datetime.now().timetuple().tm_yday

        if day_of_year == 1:
            count = 0

        self.transaction_number = f'TRN{count}{date.today().year}'
        super(TransactionTable, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.id} | {self.company.name} | {self.branch.short_name} | {self.department.name} | {self.transaction_number} | {self.transaction_status} | {self.remarks}'


class TransactionLineItem(models.Model):
    KG = 'KG'
    METRE = 'Metre'

    transaction = ForeignKey(TransactionTable, on_delete=RESTRICT)

    article = ForeignKey(ArticleMaster, on_delete=RESTRICT,
                         related_name='transaction_article')
    colour = ForeignKey(ColorMaster, on_delete=RESTRICT,
                        related_name='transaction_color')
    required_on_date = models.DateTimeField()
    qunatity = models.DecimalField(decimal_places=10, max_digits=19)
    rate_per_unit = models.IntegerField()
    UNIT = [
        (KG, 'KG'),
        (METRE, 'Metre')
    ]
    unit = models.CharField(max_length=5, choices=UNIT,)

    def __str__(self) -> str:
        return f'{self.id}  | {self.transaction} | {self.article.name} | {self.colour.name} | {self.required_on_date} | {self.qunatity} | {self.rate_per_unit} | {self.unit}'


class InventoryItem(models.Model):
    KG = 'KG'
    METRE = 'Metre'
    transaction_line_item = ForeignKey(TransactionLineItem, on_delete=RESTRICT)
    article = ForeignKey(ArticleMaster, on_delete=RESTRICT,
                         related_name='inven_article')
    colour = ForeignKey(ColorMaster, on_delete=RESTRICT,
                        related_name='inven_color')
    company = models.ForeignKey(
        CompanyLedgerMaster, on_delete=RESTRICT, related_name='inven_company')
    gross_quantity = models.DecimalField(max_digits=19, decimal_places=10)
    net_quantity = models.DecimalField(max_digits=19, decimal_places=10)
    UNIT = [
        (KG, 'KG'),
        (METRE, 'Metre')
    ]
    unit = models.CharField(max_length=5, choices=UNIT,)

    def __str__(self) -> str:
        return f'{self.id} | {self.transaction_line_item.id} | {self.article.name} | {self.colour.name} | {self.company.name} | {self.gross_quantity} | {self.net_quantity} | {self.unit}'
