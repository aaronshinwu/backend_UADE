from django.urls import path
from django.views.decorators.csrf import csrf_exempt 
from .views import MensajeAPIView, MensajeDetalleAPIView, MensajesPorMotivoView, MensajePublicCreateView
from .views_admin import AdminTokenObtainPairView

urlpatterns = [

    path('Mensajes/', csrf_exempt(MensajePublicCreateView.as_view()), name='mensaje-create'),
    path('Mensajes/admin/', MensajeAPIView.as_view(), name='mensaje-list-admin'),
    path('Mensajes/<int:id_mensaje>/', MensajeDetalleAPIView.as_view(), name='mensaje-detalle'),
    path('Mensajes/filtrar/', MensajesPorMotivoView.as_view(), name='mensajes-filtrar'),
    path('token-admin/', AdminTokenObtainPairView.as_view(), name='token_admin'),
]