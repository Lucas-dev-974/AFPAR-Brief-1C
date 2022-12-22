from django.urls import path
from Site.views import *

urlpatterns = [
    # Authentification
    path('auth/check', checkToken, name="check_token"),
    path('auth/login', login,      name="login"),
    
    # CSV urls Import / download / log
    path('csv/import',         ImportCSV),
    path('csv/import/log',     getImportLog),
    path('csv/fails/download', downloadImportFailed),

    path('regions/top', topRegions),
    path('regions',     byRegions),

    path('products/top', topProducts),
    path('products',     byProducts),

    path('regions/products', RegionsProduct),

    # Filtering choices
    path('pays',  getPays),
    path('years', getMinAndMaxYear),
]
