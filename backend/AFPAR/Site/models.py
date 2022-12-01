from django.db import models

# Create your models here.

class Invoice(models.Model):
    invoice_no   = models.CharField(max_length=100, unique=True, blank=False, null=False)
    invoice_date = models.DateField(blank=False, null=False)
    country      = models.CharField(max_length=50, blank=False, null=False)

class FailInvoice(models.Model):
    invoice_no   = models.CharField(max_length=100, unique=True, blank=False, null=False)
    invoice_date = models.DateField(blank=False, null=False)
    country      = models.CharField(max_length=50, blank=False, null=False)

class RepearableInvoice(models.Model):
    invoice_no   = models.CharField(max_length=100, unique=True, blank=False, null=False)
    invoice_date = models.DateField(blank=False, null=False)
    country      = models.CharField(max_length=50, blank=False, null=False)

class Product(models.Model):
    stock_code  = models.CharField(max_length=50, blank=False, null=False)
    unit_price  = models.FloatField(blank=False, null=False)
    description = models.CharField(max_length=300, blank=True, null=True)

class InvoiceDetails(models.Model):
    quantity = models.IntegerField(blank=False, null=False)
    customer_id = models.CharField(max_length=50, blank=True, null=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)