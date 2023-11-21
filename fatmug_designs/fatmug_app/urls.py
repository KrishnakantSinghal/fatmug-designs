from django.urls import path
from .views import *

urlpatterns = [
    path('vendors/', VenderAPIView.as_view(), name="vendor_list"),
    path('vendors/<int:vendor_id>/', VenderAPIView.as_view(), name="vendor"),
]
