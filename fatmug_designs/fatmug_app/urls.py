from django.urls import path
from .views import *

urlpatterns = [
    path('admin-tokens/', AdminTokensView.as_view(), name='admin-tokens'),
    
    path('vendors/', VenderAPIView.as_view(), name="vendor_list"),
    path('vendors/<int:vendor_id>/', VenderAPIView.as_view(), name="vendor"),
    path("vendors/<int:vendor_id>/performance", PerformanceMetricsView.as_view(), name="vendor-performance"),
    
    path('purchase_orders/', PurchaseOrderView.as_view(), name="purchase-order"),
    path('purchase_orders/<int:po_id>/', PurchaseOrderView.as_view(), name="purchase-order"),
    path("purchase_orders/<int:po_id>/acknowledge", AcknowledgePOView.as_view(), name="update-acknowledgement"),
]
