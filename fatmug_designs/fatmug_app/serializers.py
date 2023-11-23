from rest_framework import serializers
from .models import *
from django.utils import timezone

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ["name", "contact_details", "address"]
                
                
class PurchaseOrderSerializer(serializers.ModelSerializer):
    vendor_details = serializers.SerializerMethodField('get_vendor_details')
    
    def get_vendor_details(self, obj):
        serializer = VendorSerializer(obj.vendor)
        return serializer.data
    
    class Meta:
        model = PurchaseOrder
        fields = "__all__"
    

    def create(self, validated_data):
        status = validated_data.get("status")
        purchase_order = PurchaseOrder.objects.create(**validated_data)
        
        if status=="complete":
            purchase_order.acknowledgment_date = timezone.now()
            purchase_order.save()
            return purchase_order
    
        return purchase_order