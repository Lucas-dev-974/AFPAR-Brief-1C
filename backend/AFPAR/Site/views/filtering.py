from rest_framework.permissions import IsAuthenticated
from Site.models import Region, Invoice
from rest_framework.decorators import *
from django.http import JsonResponse
from Site.Lector import *
from Site.Serializers import *

''' In this file we can find all to get filtering parameters '''


'''
    This method return all regions for filter search
'''
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getPays(request):
    _pays = RegionSerializer(Region.objects.all(), many=True)
    pays  = []
    for pay in _pays.data:
        pays.append(pay['region_name'])
    return JsonResponse(pays, safe=False)


'''
    This method return years range where data is present
'''
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMinAndMaxYear(request):
    young_year = Invoice.objects.order_by('invoice_date__year').first().invoice_date
    older_year = Invoice.objects.order_by('-invoice_date__year').first().invoice_date

    years = [int(young_year.strftime('%Y'))]
    diff  = int(older_year.strftime('%Y')) - int(young_year.strftime('%Y'))

    for i in range(diff):
        years.append(years[len(years) - 1] + 1)

    years.append('Toutes')
    print(years)
    return JsonResponse({'years': years})