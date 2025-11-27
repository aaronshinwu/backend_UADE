from django.urls import path
from .views import MensajeAPIView, MensajeDetalleAPIView, MensajesPorMotivoView, MensajePublicCreateView
from .views_admin import AdminTokenObtainPairView

urlpatterns = [
    path('Mensajes/', MensajePublicCreateView.as_view(), name='mensaje-create'),  # publico
    path('Mensajes/admin/', MensajeAPIView.as_view(), name='mensaje-list-admin'),  # admin
    path('Mensajes/<int:id_mensaje>/', MensajeDetalleAPIView.as_view(), name='mensaje-detalle'),
    path('Mensajes/filtrar/', MensajesPorMotivoView.as_view(), name='mensajes-filtrar'),
    path('token-admin/', AdminTokenObtainPairView.as_view(), name='token_admin'),
]
