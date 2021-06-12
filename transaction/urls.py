from django.urls import path
from . import views


app_name = "Transaction"

transaction_urls = [
    path("add_transaction/", views.TransactionView.as_view(), name="add_transaction"),
    path("add_line_item/", views.LineItemView.as_view(), name="add_line_item"),
    path(
        "add_inventory_item/",
        views.InventoryItemView.as_view(),
        name="add_inventory_item",
    ),
    path(
        "delete_transaction/<int:pk>/",
        views.TransactionDeleteView.as_view(),
        name="delete_transaction",
    ),
    path(
        "transaction_detail/<int:pk>/",
        views.TransactionDetailView.as_view(),
        name="transaction_detail",
    ),
]
