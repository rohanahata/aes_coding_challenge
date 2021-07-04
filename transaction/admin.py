from django.contrib import admin
from .models import *

@admin.register(BranchMaster)
class BranchMasterAdmin(admin.ModelAdmin):
    list_display= ["id","short_name","contact_person_name","pin_code","mobile"]
    search_fields=["short_name","mobile"]
    list_display_links = list_display

@admin.register(DepartmentMaster)
class DepartmentMasterAdmin(admin.ModelAdmin):
    list_display= ["id","name"]
    search_fields=["name"]
    list_display_links = list_display

@admin.register(CompanyLedgerMaster)
class CompanyLedgerMasterAdmin(admin.ModelAdmin):
    list_display= ["id","name","gst_number","supplier_status","mobile"]
    search_fields=["mobile","name"]
    list_display_links = list_display

@admin.register(ArticleMaster)
class ArticleMasterAdmin(admin.ModelAdmin):
    list_display= ["id","name","short_name","blend_pct","twists"]
    search_fields=["short_name","name"]
    list_display_links = list_display

@admin.register(ColorMaster)
class ColorMasterAdmin(admin.ModelAdmin):
    list_display= ["id","article","name","short_name"]
    search_fields=["name","short_name"]
    list_display_links = list_display

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display= ["id","company","branch","transaction_number","transaction_status"]
    search_fields=["name","short_name","transaction_number"]
    list_display_links = list_display

@admin.register(TransactionLineItemDetail)
class TransactionLineItemDetailAdmin(admin.ModelAdmin):
    list_display= ["id","article","colour","required_on_date"]
    list_display_links = list_display

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display= ["id","line_item","article","colour"]
    list_display_links = list_display