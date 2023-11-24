from .models import PurchaseOrder
from django.db.models import Avg, ExpressionWrapper, F, fields

def create_performance_matrics(vendor):
    purchase_orders = PurchaseOrder.objects.filter(vendor_id = vendor.id)
    completed_orders = purchase_orders.filter(status="complete")
    
    if purchase_orders.exists():
        if completed_orders.exists():
            on_time_delivery_purchase_orders = completed_orders.filter(delivery_date__gte=F('acknowledgment_date'))
            
            on_time_delivery_rate = (on_time_delivery_purchase_orders.count() / completed_orders.count()) * 100
            vendor.on_time_delivery_rate = on_time_delivery_rate
        
        average_quality_rating = purchase_orders.aggregate(average_quality_rating = Avg("quality_rating"))
        vendor.quality_rating_avg = round(average_quality_rating["average_quality_rating"], 2)

        average_response_time = purchase_orders.filter(acknowledgment_date__isnull=False).aggregate(average_response_time=Avg(
                ExpressionWrapper(F('acknowledgment_date')-F('order_date'), output_field=fields.DurationField())
            ))
        
        if average_response_time["average_response_time"]:        
            vendor.average_response_time = round(average_response_time["average_response_time"].total_seconds() // (24 * 3600), 2)
                
        completed_order_percentage = (completed_orders.count() / purchase_orders.count()) * 100
        vendor.fulfillment_rate = round(completed_order_percentage, 2)

        vendor.save()
