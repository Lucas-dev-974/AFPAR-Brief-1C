from rest_framework import serializers, viewsets
from Site.models import *

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(max_length=100, required=True)


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Region
        fields = ['region_name']

class TopRegionSelrializer(serializers.ModelSerializer):
    invoice_details = serializers.IntegerField()
    class Meta:
        model = Region
        fields = ['region_name', 'invoice_details']

        
class ProductSerializer(serializers.ModelSerializer):
    invoice_detail = serializers.IntegerField()
    
    class Meta:
        model  = Product
        fields = '__all__'

class TopProductSerializer(serializers.ModelSerializer):
    details = serializers.IntegerField()

    class Meta:
        model = Product
        fields = ['description', 'stock_code', 'details']

class InvoiceDetailsSerializer(serializers.ModelSerializer):
    product  =  ProductSerializer(many=False)
    
    class Meta:
        model  = InvoiceDetails
        fields = ['quantity', 'product']


class InvoiceSerializer(serializers.ModelSerializer):
    details = InvoiceDetailsSerializer(many=True)

    class Meta:
        model  = Invoice
        fields = ['invoice_no', 'invoice_date', 'details']


