# Generated by Django 5.2.1 on 2025-05-18 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('teachers', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='materia',
            name='docente',
        ),
        migrations.AddField(
            model_name='materia',
            name='docentes',
            field=models.ManyToManyField(related_name='materias', to='teachers.docente'),
        ),
    ]
