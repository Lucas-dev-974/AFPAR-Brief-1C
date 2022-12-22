from django.http import JsonResponse, HttpResponse

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import *
from Site.Lector import *
from Site.models import *

'''
    In this method we get request files and save it via the Lector created for thats. 
    The Lector return an statement of the import, how line inserted in db how many failed

    @param  request
    @return Json that is the status of the import
'''
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ImportCSV(request):
    file = request.FILES.get('csv_file') # Get CSV file emitted by the client
    status_import = lector(file)         # Transform the CSV to dataframe "pandas" & apply analyse strategie 
                                         #    & save into database the correct & incorrect rows 
                                         
    # Create log with the correct rows imported & incorrect rows imported and the filename of file
    ImportLog.objects.create(log = status_import, file_name = file, importe_date = datetime.datetime.now())
    return JsonResponse({"status": status_import})

'''
    This method delete all imported fails
'''
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteFailed(request):
    models.FailInvoice.objects.all().delete()
    return JsonResponse({'status': 'ok'})

'''
    This methode get all failed imported CSV, create pandas dataframe with the data,
    transform the dataframe to csv file to client download and delete imported fails
'''
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def downloadImportFailed(request):
    import_failed = FailInvoice.objects.all()
    csv = getDataframe(import_failed)

    FailInvoice.objects.all().delete()

    response = HttpResponse('text/csv')
    response['Content-Disposition'] = 'attachment; filename=export.csv'
    csv.to_csv(path_or_buf=response)
    
    return  response    



'''
    This method will return the last log registered for the imports
    @params request
    @return Json
'''
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getImportLog(request):
    last_import = ImportLog.objects.last()
    if last_import is not None:
        last_import = {
            "log": last_import.log,
            'file_name': last_import.file_name,
            'date_import': last_import.importe_date
        }
        return JsonResponse(last_import)

    return JsonResponse({'status': 'aucun log d\'import'}, 404)
