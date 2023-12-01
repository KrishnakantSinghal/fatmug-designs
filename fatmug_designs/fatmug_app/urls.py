# urls.py

from django.urls import path
from .views import (
    AdminTokensView,
    VendorAPIView,
    PerformanceMetricsView,
    PurchaseOrderView,
    AcknowledgePOView,
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # Endpoint for obtaining admin tokens.
    path('admin-tokens/', AdminTokensView.as_view(), name='admin-tokens'),

    # Endpoint for refreshing admin tokens.
    path('admin_refresh_token/', TokenRefreshView.as_view(), name="admin-refresh-token"),

    # Endpoints for managing vendors.
    path('vendors/', VendorAPIView.as_view(), name="vendor_list"),
    path('vendors/<int:vendor_id>/', VendorAPIView.as_view(), name="vendor"),
    path("vendors/<int:vendor_id>/performance", PerformanceMetricsView.as_view(), name="vendor-performance"),

    # Endpoints for managing purchase orders.
    path('purchase_orders/', PurchaseOrderView.as_view(), name="purchase-order"),
    path('purchase_orders/<int:po_id>/', PurchaseOrderView.as_view(), name="purchase-order"),
    path("purchase_orders/<int:po_id>/acknowledge", AcknowledgePOView.as_view(), name="update-acknowledgement"),
]
