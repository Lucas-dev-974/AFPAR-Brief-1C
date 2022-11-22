from rest_framework_simplejwt import views as jwt_views
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/', include('Site.urls'))
]
