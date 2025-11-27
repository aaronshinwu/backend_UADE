from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Mensaje
from .serializers import MensajeSerializer
from utils.pagination import CustomPagination


# Vista pública de inicio de API
def inicio(request):
    mensaje = "<h1>Bienvenido a la API del formulario</h1>"
    return HttpResponse(mensaje)


# Vista pública para crear mensajes
class MensajePublicCreateView(generics.CreateAPIView):
    queryset = Mensaje.objects.all()
    serializer_class = MensajeSerializer
    permission_classes = [AllowAny]


# Obtener y crear mensajes desde admin
class MensajeAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @swagger_auto_schema(
        operation_description="Obtener todos los mensajes registrados. Requiere autenticación de admin.",
        responses={200: MensajeSerializer(many=True)}
    )
    def get(self, request):
        mensajes = Mensaje.objects.all()
        paginator = CustomPagination()
        resultados = paginator.paginate_queryset(mensajes, request)
        serializer = MensajeSerializer(resultados, many=True)
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        operation_description="Crear un nuevo mensaje. Solo admin.",
        request_body=MensajeSerializer,
        responses={201: MensajeSerializer}
    )
    def post(self, request):
        serializer = MensajeSerializer(data=request.data)
        if serializer.is_valid():
            mensaje = serializer.save()
            return Response(MensajeSerializer(mensaje).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Vista CRUD del mensaje desde admin
class MensajeDetalleAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @swagger_auto_schema(
        operation_description="Obtener mensaje por ID. Solo admin.",
        responses={200: MensajeSerializer, 404: 'No encontrado'}
    )
    def get(self, request, id_mensaje):
        try:
            mensaje = Mensaje.objects.get(pk=id_mensaje)
        except Mensaje.DoesNotExist:
            return Response({'error': 'Mensaje no existente'}, status=status.HTTP_404_NOT_FOUND)
        serializer = MensajeSerializer(mensaje)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Eliminar mensaje por ID. Solo admin.",
        responses={204: 'Mensaje eliminado', 404: 'No encontrado'}
    )
    def delete(self, request, id_mensaje):
        try:
            mensaje = Mensaje.objects.get(pk=id_mensaje)
        except Mensaje.DoesNotExist:
            return Response({'error': 'Mensaje no existente'}, status=status.HTTP_404_NOT_FOUND)
        mensaje.delete()
        return Response({'mensaje': 'Mensaje eliminado exitosamente.'}, status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        operation_description="Actualizar mensaje por ID. Solo admin.",
        request_body=MensajeSerializer,
        responses={200: 'Mensaje actualizado', 400: 'Error de validación'}
    )
    def put(self, request, id_mensaje):
        try:
            mensaje = Mensaje.objects.get(pk=id_mensaje)
        except Mensaje.DoesNotExist:
            return Response({'error': 'Mensaje no existente'}, status=status.HTTP_404_NOT_FOUND)

        serializer = MensajeSerializer(mensaje, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Mensaje actualizado exitosamente'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Vista para filtrar mensajes de admin
class MensajesPorMotivoView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @swagger_auto_schema(
        operation_description="Obtener mensajes filtrados por motivo. Solo admin.",
        manual_parameters=[
            openapi.Parameter('motivo', openapi.IN_QUERY, description="Motivo: Clases, Conciertos, Otros", type=openapi.TYPE_STRING)
        ],
        responses={200: MensajeSerializer(many=True), 400: 'Motivo inválido'}
    )
    def get(self, request):
        motivo = request.GET.get('motivo', None)
        if motivo not in ['Clases', 'Conciertos', 'Otros']:
            return Response({'error': 'Motivo inválido. Debe ser Clases, Conciertos u Otros.'},
                            status=status.HTTP_400_BAD_REQUEST)
        mensajes = Mensaje.objects.filter(motivo__motivo=motivo)
        serializer = MensajeSerializer(mensajes, many=True)
        return Response(serializer.data)
