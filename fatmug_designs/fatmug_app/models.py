from django.db import models
import uuid

# Create your models here.
class Vendor(models.Model):
    name = models.CharField(max_length=200)
    contact_details = models.TextField(help_text="Contact information of the vendor.")
    address = models.TextField(help_text="Physical address of the vendor.")
    vendor_code = models.CharField(max_length=6, help_text="A unique identifier for the vendor.")
    on_time_delivery_rate = models.FloatField(help_text="Tracks the percentage of on-time deliveries.", default=0)
    quality_rating_avg = models.FloatField(help_text="Average rating of quality based on purchase orders.", default=0)
    average_response_time = models.FloatField(help_text="Average time taken to acknowledge purchase orders.", default=0)
    fulfillment_rate = models.FloatField(help_text="Percentage of purchase orders fulfilled successfully.", default=0)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.vendor_code = str(uuid.uuid4().int % 10**6).zfill(6)   
        super().save(*args, **kwargs)


class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=100, help_text="Unique number identifying the PO.")
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True, help_text="Date when the order was placed.")
    delivery_date = models.DateTimeField(help_text="Expected or actual delivery date of the order.")
    items = models.JSONField(default=dict, help_text="Details of items ordered.")
    quantity = models.IntegerField(default=0, help_text="Total quantity of items in the PO.")
    status = models.CharField(max_length=20, help_text="Current status of the PO (e.g., pending, completed, canceled).")
    quality_rating = models.FloatField(null=True, help_text="Rating given to the vendor for this PO.")
    issue_date = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the PO was issued to the vendor.")
    acknowledgment_date = models.DateTimeField(null=True, help_text="Timestamp when the vendor acknowledged the PO.")
    

class HistoricalPerformance(models.Model):
    vender = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField(help_text="Date of the performance record.")
    on_time_delivery_rate = models.FloatField(help_text="Historical record of the on-time delivery rate.", default=0)
    quality_rating_avg = models.FloatField(help_text="Historical record of the quality rating average.", default=0)
    average_response_time = models.FloatField(help_text="Historical record of the average response time.", default=0)
    fulfillment_rate = models.FloatField(help_text="Historical record of the fulfilment rate.", default=0)
    