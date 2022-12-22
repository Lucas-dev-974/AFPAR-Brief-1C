from django.http import JsonResponse

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import *
from Site.Lector import *
from Site.models import Region, Invoice


from django.db.models import Count

# Serializer
from Site.Serializers import *
import pprint

"""
    In this file we find methods to return data saved in database
"""



'''
    Util function to get the top x of sells by regions
'''
def getTopRegions(top):
    _regions = Region.objects.annotate(invoice_details = Count('invoice__details')).order_by('-invoice_details')
    regions  = {}

    for i in range(top):
        name    = _regions[i].region_name
        details = _regions[i].invoice_details
        regions[name] = details

    return regions

'''
    Util funciton to get the top x of sells by product
'''
def getTopProduct(top):
    _product = Product.objects.annotate(details = Count('product_details')).order_by('-details')
    products = {}

    for i in range(top):
        name    = _product[i].description
        details = _product[i].details
        products[_product[i].stock_code + ' - ' + name] = details

    return products



'''
    This method return the top x of regions that have sold products
'''
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def topRegions(request):
    nb_items = 6
    year     = None
    top_regions  = None

    if request.GET.get('year'):
        year = request.GET.get('year')

    if request.GET.get('nb_items'):
        nb_items = int(request.GET.get('nb_items'))

    if year is not None and year != 'Toutes' :
        top_regions = Region.objects.filter(invoice_region__invoice_date__year = year).annotate(invoice_details = Count('invoice_region__details')).order_by('-invoice_details')[:nb_items]
    else:
        top_regions = Region.objects.annotate(invoice_details = Count('invoice_region__details')).order_by('-invoice_details')[:nb_items]

    top_regions = TopRegionSelrializer(top_regions, many=True)

    regions = {}

    for region in top_regions.data:
        regions[region['region_name']] = region['invoice_details'] 

    return JsonResponse(regions)

'''
    This method return the total selled products for x regions
'''
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def byRegions(request):
    regions = None
    years   = None
    return_data = {}

    if request.GET.get('regions') is not None:
        regions = request.GET.get('regions')
    else:
        regions = ['France', 'Netherlands', 'United Kingdom', 'Australia', 'Finland', 'Italy']

    if request.GET.get('year') is not None:
        years = request.GET.get('year')
    else:   
        years = (Invoice.objects.latest('invoice_date').invoice_date).year


    if regions is not None:
        # If str like Italy,France,... so split it to get an array
        if type(regions) is str:
            regions = regions.split(',')

        for region in regions:  
            region_= Region.objects.filter( region_name = region ).first()
            if type(years) is not dict:
                invoices  = InvoiceDetails.objects.filter( invoice__country = region_).count()
            else:
                invoices  = InvoiceDetails.objects.filter( invoice__country = region_,  invoice__invoice_date__range = ['2011-01-01', '2011-01-30']).count()

            return_data[region] = invoices

    return JsonResponse(return_data)


'''
    This method returns the top x of products sold
'''
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def topProducts(request):
    nb_items = 6
    year = None
    top_products = None

    if request.GET.get('nb_items'):
        nb_items = int(request.GET.get('nb_items'))

    if request.GET.get('year'):
        year = request.GET.get('year')
    
    if year is not None and year != 'Toutes':
        top_products = Product.objects.filter(product_details__invoice__invoice_date__year = year).annotate(details = Count('product_details')).order_by('-details')[:nb_items]
    else:
        top_products = Product.objects.annotate(details = Count('product_details')).order_by('-details')[:nb_items]


    top_products = TopProductSerializer(top_products, many=True)

    products = {}
    for prod in top_products.data:
        products[prod['description'] + ' - ' + prod['stock_code']] = prod['details']
        
    return JsonResponse(products, safe=False)

'''
    This method return the total of sell for x product
'''
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def byProducts(request):
    return_data = {}
    products = None
    year     = None

    if request.GET.get('year'):
        year = request.GET.get('year')

    if request.GET.get('products') is not None:
        products = request.GET.get('products')

    if products is not None:
        if type(products) is str:
            products = products.split(',')

        for product in products:
            _product  = Product.objects.get(pk = product)
            if year is not None:
                products_ = InvoiceDetails.objects.filter(product = _product, invoice__invoice_date__year = year).count()
            else:
                products_ = InvoiceDetails.objects.filter(product = _product).count()
            return_data[_product.stock_code] = products_

    return JsonResponse(return_data)


@api_view(['GET'])
def RegionsProduct(request):
    return_data = {}
    regions     = 'United Kingdom'
    nb_products = 6

    if request.GET.get('regions'):
        regions = request.GET.get('regions')
        
    if request.GET.get('nb_products'):
        nb_products = request.GET.get('nb_products')

    if regions is not dict:
        regions = regions.split(',')

    for region in regions:
        region     = Region.objects.filter(region_name = region).first()
        _product   = Product.objects.filter(product_details__invoice__country = region).annotate(invoice_detail = Count('product_details')).order_by('-invoice_detail')[:nb_products]
        
        serialized = ProductSerializer(_product, many=True)
        total_sold = InvoiceDetails.objects.filter( invoice__country = region).count()

        return_data[region.region_name] = {
            'products':   serialized.data,
            'total_sold': total_sold
        }
    
    return JsonResponse(return_data, safe=False)
    