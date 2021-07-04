from django.db import models
from django.db.models.deletion import RESTRICT
import uuid
from datetime import date,datetime

# Masters required in transaction models
class BranchMaster(models.Model):
    short_name = models.CharField(max_length=10, unique=True)
    contact_person_name = models.CharField(max_length=20)
    gst_number = models.CharField(max_length=20)
    address1 = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=10)
    mobile = models.CharField(blank=True, null=True, max_length=10)
    
    def __str__(self):
        return self.short_name


class DepartmentMaster(models.Model):
    name = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return self.name


class CompanyLedgerMaster(models.Model):
    name = models.CharField(max_length=32, unique=True)
    gst_number = models.CharField(max_length=20, unique=True)
    supplier_status = models.BooleanField(default=False)
    address1 = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=10)
    mobile = models.CharField(max_length=10)
    remarks = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return self.name


class ArticleMaster(models.Model):
    name = models.CharField(max_length=80, unique=True)
    short_name = models.CharField(max_length=50, unique=True)
    blend_pct = models.CharField(max_length=50)
    twists = models.PositiveIntegerField(blank=True, null=True)
    remarks = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return self.name

class ColorMaster(models.Model):
    article = models.ForeignKey(ArticleMaster, on_delete=models.PROTECT)
    name = models.CharField(max_length=20)
    short_name = models.CharField(max_length=20)
    remarks = models.CharField(max_length=64, blank=True)
    
    def __str__(self):
        return self.name

class Transaction(models.Model):
    
    tr_status = [
            ("PENDING","PENDING"),
            ("COMPLETED","COMPLETED"),
            ("CLOSE","CLOSE"),
            ]
    
    company = models.ForeignKey(to = CompanyLedgerMaster,on_delete = models.CASCADE,related_name="tn_company")
    branch = models.ForeignKey(to = BranchMaster,on_delete=models.CASCADE,related_name="tn_branch")
    department = models.ForeignKey(to = DepartmentMaster,on_delete = models.CASCADE,related_name = "tn_department")
    transaction_number = models.CharField(max_length = 50)
    transaction_status = models.CharField(max_length = 20,choices = tr_status)
    remarks = models.CharField(null = True,blank = True,max_length = 200)
    
    def __str__(self):
        return '%s_%s_%s' %(self.company.name,self.branch.short_name,self.department.name)

    def save(self, *args, **kwargs):
        unique_id = (str(uuid.uuid1()).replace('-',''))[1::2]
        current_year = date.today().year
        tr_latest = Transaction.objects.latest('id').transaction_number.split('/')
        count = 1 if tr_latest[-1] != str(current_year) else int(tr_latest[1]) + 1
        self.transaction_number = f'{unique_id}/{count}/{current_year}'
        super(Transaction, self).save(*args, **kwargs)
    
    
class TransactionLineItemDetail(models.Model):
    
    unit_choice = [
            ("KG","KG"),
            ("METRE","METRE"),
            ]
    
    transaction = models.ForeignKey(to = Transaction,on_delete=RESTRICT,related_name = "tr_item_detail")
    article = models.ForeignKey(to = ArticleMaster,on_delete=models.CASCADE,related_name = "td_article")
    colour = models.ForeignKey(to = ColorMaster,on_delete=models.CASCADE,related_name = "td_colour")
    quantity = models.DecimalField(max_digits=15,decimal_places = 2)
    rate_per_unit = models.IntegerField()
    unit = models.CharField(choices = unit_choice,max_length = 12)
    required_on_date = models.DateTimeField()
    
    def __str__(self):
        return '%s_%s' %(self.article.name,self.colour.name)
    
class InventoryItem(models.Model):
    
    unit__choice = [
            ("KG","KG"),
            ("METRE","METRE"),
            ]
    
    line_item = models.ForeignKey(to = TransactionLineItemDetail,on_delete = RESTRICT,related_name='inv_line')
    article = models.ForeignKey(to = ArticleMaster,on_delete = models.CASCADE,related_name = "invent_article")
    colour = models.ForeignKey(to = ColorMaster,on_delete = models.CASCADE,related_name="invent_colour")
    company = models.ForeignKey(to = CompanyLedgerMaster,on_delete=models.CASCADE,related_name="invent_company")
    gross_quantity = models.DecimalField(max_digits=15,decimal_places=3)
    net_quantity = models.DecimalField(max_digits=15,decimal_places=3)
    unit = models.CharField(choices = unit__choice,max_length = 12)

    def __str__(self):
        return '%s_%s_%s' %(self.company.name,self.article.name,self.colour.name)