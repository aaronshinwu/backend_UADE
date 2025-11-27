from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

# Configuración de la documentación automática de la API
schema_view = get_schema_view(
    openapi.Info(
        title='API del formulario',
        default_version='v1',
        description='Documentación general del proyecto API REST Formulario de Contacto'
    ),
    public=True,
    permission_classes=[AllowAny]
)

urlpatterns = [
    # Documentación de la API
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0)),

    # Panel de administración de Django
    path('admin/', admin.site.urls),

    # URLs de la aplicación principal
    path('api/', include('api.urls')),

    # Autenticación JWT
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]