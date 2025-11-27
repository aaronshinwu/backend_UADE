from django.db import migrations

def crear_motivos_iniciales(apps, schema_editor):
   
    Motivo = apps.get_model('api', 'Motivo')
    # Lista de motivos que queremos crear
    motivos = ['Clases', 'Conciertos', 'Otros']
    
    for nombre in motivos:
        Motivo.objects.get_or_create(motivo=nombre)

class Migration(migrations.Migration):

    dependencies = [
    ('api', '0003_mensaje_motivo_mensaje_persona'),
    ]

    operations = [
        migrations.RunPython(crear_motivos_iniciales),
    ]
