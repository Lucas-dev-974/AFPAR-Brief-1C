from django.urls import path
from Site.views import *

urlpatterns = [
    path('auth/check', HelloView.as_view(), name="hello"),

    path('auth/login', Authentification.as_view(), name="authentification"),

    path('csv/import', ImportCSV)
]
