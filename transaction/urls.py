from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'transaction_add', views.TransactionView, basename='transaction_add')
router.register(r'line_items_add', views.TransactionLineItemView, basename='line_items_add')
router.register(r'inventory_item_add', views.InventoryItemView, basename='inventory_item_add')
router.register(r'full_transaction_details', views.ViewFullTransactionDetailsView, basename='full_transaction_details')
urlpatterns = router.urls