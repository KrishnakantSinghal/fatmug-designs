# Generated by Django 4.2.7 on 2023-11-24 12:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('contact_details', models.TextField(help_text='Contact information of the vendor.')),
                ('address', models.TextField(help_text='Physical address of the vendor.')),
                ('vendor_code', models.CharField(help_text='A unique identifier for the vendor.', max_length=6)),
                ('on_time_delivery_rate', models.FloatField(default=0, help_text='Tracks the percentage of on-time deliveries.')),
                ('quality_rating_avg', models.FloatField(default=0, help_text='Average rating of quality based on purchase orders.')),
                ('average_response_time', models.FloatField(default=0, help_text='Average time taken to acknowledge purchase orders (days).')),
                ('fulfillment_rate', models.FloatField(default=0, help_text='Percentage of purchase orders fulfilled successfully.')),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('po_number', models.CharField(help_text='Unique number identifying the PO.', max_length=100)),
                ('order_date', models.DateTimeField(help_text='Date when the order was placed.')),
                ('delivery_date', models.DateTimeField(help_text='Expected or actual delivery date of the order.')),
                ('items', models.JSONField(default=dict, help_text='Details of items ordered.')),
                ('quantity', models.IntegerField(default=0, help_text='Total quantity of items in the PO.')),
                ('status', models.CharField(help_text='Current status of the PO (e.g., pending, completed, canceled).', max_length=20)),
                ('quality_rating', models.FloatField(help_text='Rating given to the vendor for this PO.', null=True)),
                ('issue_date', models.DateTimeField(auto_now_add=True, help_text='Timestamp when the PO was issued to the vendor.')),
                ('acknowledgment_date', models.DateTimeField(blank=True, help_text='Timestamp when the vendor acknowledged the PO.', null=True)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fatmug_app.vendor')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalPerformance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, help_text='Date of the performance record.')),
                ('on_time_delivery_rate', models.FloatField(default=0, help_text='Historical record of the on-time delivery rate.')),
                ('quality_rating_avg', models.FloatField(default=0, help_text='Historical record of the quality rating average.')),
                ('average_response_time', models.FloatField(default=0, help_text='Historical record of the average response time. (days)')),
                ('fulfillment_rate', models.FloatField(default=0, help_text='Historical record of the fulfilment rate.')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fatmug_app.vendor')),
            ],
        ),
    ]
