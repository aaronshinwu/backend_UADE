from django.db import models

# Modelo que representa a una persona que envía un mensaje
class Persona(models.Model):
    # Nombre de la persona (máximo 100 caracteres)
    nombre = models.CharField(max_length=100)
    # Apellido de la persona (máximo 100 caracteres)
    apellido = models.CharField(max_length=100)
    # Email de contacto (máximo 150 caracteres)
    email = models.CharField(max_length=150)

    def __str__(self):
        # Representación legible de la persona: "Apellido, Nombre"
        return f"{self.apellido}, {self.nombre}"
  
# Modelo que representa el motivo del mensaje
class Motivo(models.Model):
    # Texto del motivo (por ejemplo: "Clases", "Conciertos", etc.)
    motivo = models.CharField(max_length=25)
    
    def __str__(self):
        # Representación legible del motivo
        return self.motivo

# Modelo que representa un mensaje enviado por una persona con un motivo asociado
class Mensaje(models.Model):
    # Relación con la persona que envió el mensaje
    persona = models.ForeignKey(Persona, on_delete=models.RESTRICT, related_name='mensajes')
    # Relación con el motivo del mensaje
    motivo = models.ForeignKey(Motivo, on_delete=models.RESTRICT, related_name='mensajes')
    # Contenido del mensaje (máximo 500 caracteres)
    mensaje = models.CharField(max_length=500)

    def __str__(self):
        # Representación corta del mensaje: nombre de la persona + primeros 30 caracteres del mensaje
        texto = self.mensaje
        if len(texto) > 30:
            texto = texto[:30].rstrip() + "..."
        return f"{self.persona.nombre} {self.persona.apellido} - {texto}"
