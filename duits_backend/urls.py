# duits_backend/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView


from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="DUITS API",
      default_version='v1',
      description="API Documentation for the Dhaka University IT Society Backend",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="admin@duits.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # 1. Instant Redirect to API hub
    path('', RedirectView.as_view(url='/api/v1/', permanent=False), name='home'),
    
    # 2. Django Admin
    path('admin/', admin.site.urls),
    
    # 3. DRF Browsable API Login (Fixes the missing POST/PUT buttons)
    path('api-auth/', include('rest_framework.urls')),
    
    # 4. Authentication (Djoser + JWT)
    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/auth/', include('djoser.urls.jwt')),
    
    # 5. ALL Core Apps (This connects to the api/urls.py file above!)
    path('api/v1/', include('api.urls'), name='api-root'),
    
    # 6. Swagger Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Media URL serving for local development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)