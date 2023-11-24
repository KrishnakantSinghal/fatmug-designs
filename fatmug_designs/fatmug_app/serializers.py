from rest_framework import serializers
from .models import *
from django.utils import timezone
import uuid
from .track_performance import *


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ["id", "name", "contact_details", "address"]
        
    def create(self, validated_data):
        vendor_code = str(uuid.uuid4().int % 10**6).zfill(6)
        vendor = Vendor.objects.create(**validated_data, vendor_code=vendor_code)
        return vendor
                
                
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
        po_number = str(uuid.uuid4().int % 10**6).zfill(6)
        purchase_order = PurchaseOrder.objects.create(**validated_data, po_number=po_number)
        
        if status=="complete":
            purchase_order.acknowledgment_date = timezone.now()
            purchase_order.save()

        create_performance_matrics(purchase_order.vendor)
        return purchase_order
    
    def update(self, instance, validated_data):

        if validated_data:
            for key, value in validated_data.items():
                setattr(instance, key, value)

        if "status" in validated_data.keys():
            status = validated_data.get("status")
            if status == "complete":
                instance.acknowledgment_date = timezone.now()
            
            else:
                instance.acknowledgment_date = None
                
            instance.save()
            
        create_performance_matrics(instance.vendor)
        return instance
    