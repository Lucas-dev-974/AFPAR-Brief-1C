from django.db import models

# Create your models here.

class Region(models.Model):
    region_name = models.CharField(max_length=50, unique=True)

class Invoice(models.Model):
    invoice_no   = models.CharField(max_length=100, blank=False, null=False, primary_key=True)
    invoice_date = models.DateTimeField(blank=True, null=True)
    country      = models.ForeignKey(Region, on_delete=models.DO_NOTHING, related_name='invoice_region')
    customer_id  = models.BigIntegerField(blank=True, null=True)

class Product(models.Model):
    stock_code  = models.CharField(max_length=50, blank=False, null=False, primary_key=True)
    unit_price  = models.FloatField(blank=False, null=False)
    description = models.CharField(max_length=300, blank=True, null=True)

class InvoiceDetails(models.Model):
    quantity = models.IntegerField(blank=False, null=False)
    invoice  = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='details')
    product  = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_details')

class FailInvoice(models.Model):
    invoice_no   = models.CharField(max_length=100, blank=True, null=True)
    invoice_date = models.CharField(max_length=50, blank=True, null=True)
    country      = models.CharField(max_length=50, blank=False, null=False)
    stock_code   = models.CharField(max_length=50, blank=True, null=True)
    description  = models.CharField(max_length=350, blank=True, null=True)
    unit_price   = models.CharField(max_length=30, blank=True, null=True)
    customer_id  = models.CharField(max_length=50, blank=True, null=True)
    quantity     = models.CharField(max_length=30, blank=True, null=True)

class RepearableInvoice(models.Model):
    invoice_no   = models.CharField(max_length=100, blank=True, null=True)
    invoice_date = models.CharField(max_length=50, blank=True, null=True)
    country      = models.CharField(max_length=50, blank=False, null=False)
    stock_code   = models.CharField(max_length=50, blank=True, null=True)
    description  = models.CharField(max_length=350, blank=True, null=True)
    unit_price   = models.CharField(max_length=30, blank=True, null=True)
    customer_id  = models.CharField(max_length=50, blank=True, null=True)
    quantity     = models.CharField(max_length=30, blank=True, null=True)


class ImportLog(models.Model):
    log       = models.JSONField()
    file_name = models.CharField(max_length=50)
    importe_date = models.DateTimeField()
    