from rest_framework import serializers
from .models import Mensaje, Persona, Motivo

# Serializer para persona
class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = ['nombre', 'apellido', 'email']

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("El email es obligatorio.")

        if '@' not in value or ' ' in value:
            raise serializers.ValidationError("El email debe contener '@' y no tener espacios.")
        
        partes = value.split('@')
        if len(partes) != 2 or '.' not in partes[1]:
            raise serializers.ValidationError("El email debe tener un formato válido.")
        
        if value.startswith('@') or value.endswith('@'):
            raise serializers.ValidationError("El email no puede empezar ni terminar con '@'.")
        
        return value


# Serializer para Mensaje
class MensajeSerializer(serializers.ModelSerializer):
    persona = PersonaSerializer()
    motivo = serializers.SlugRelatedField(
        queryset=Motivo.objects.all(),
        slug_field='motivo'
    )

    class Meta:
        model = Mensaje
        fields = ['persona', 'motivo', 'mensaje']

    # Validación del mensaje
    def validate_mensaje(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("El mensaje debe tener al menos 10 caracteres.")
        return value

    # Validación general para evitar duplicados
    def validate(self, data):
        persona_data = data.get('persona')
        motivo = data.get('motivo')
        mensaje = data.get('mensaje')

        if not (persona_data and motivo and mensaje):
            return data

        email = persona_data.get('email')
        persona = Persona.objects.filter(email=email).first()

        if persona:
            mensajes_iguales = Mensaje.objects.filter(
                persona=persona,
                motivo=motivo,
                mensaje=mensaje
            )
            if self.instance:
                mensajes_iguales = mensajes_iguales.exclude(pk=self.instance.pk)

            if mensajes_iguales.exists():
                raise serializers.ValidationError(
                    "Ya existe un mensaje igual de esta persona con el mismo motivo."
                )
        return data

    # Crear mensaje y persona
    def create(self, validated_data):
        persona_data = validated_data.pop('persona')
        persona_obj, _ = Persona.objects.get_or_create(
            email=persona_data['email'],
            defaults={
                'nombre': persona_data.get('nombre', ''),
                'apellido': persona_data.get('apellido', '')
            }
        )
        mensaje = Mensaje.objects.create(
            persona=persona_obj,
            motivo=validated_data['motivo'],
            mensaje=validated_data['mensaje']
        )
        return mensaje

    # Actualizar mensaje y persona
    def update(self, instance, validated_data):
        persona_data = validated_data.pop('persona', None)
        motivo_data = validated_data.get('motivo')

        if persona_data:
            persona = instance.persona
            persona.nombre = persona_data.get('nombre', persona.nombre)
            persona.apellido = persona_data.get('apellido', persona.apellido)
            persona.email = persona_data.get('email', persona.email)
            persona.save()

        if motivo_data:
            instance.motivo = motivo_data

        instance.mensaje = validated_data.get('mensaje', instance.mensaje)
        instance.save()
        return instance

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['mensaje_id'] = instance.id
        return rep
