# teachers/models.py

from django.db import models
from accounts.models import CustomUser

class Docente(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'rol': 'docente'})
    # materias = models.ManyToManyField("core.Materia", related_name="docentes_asignados", blank=True)

    def __str__(self):
        return f"{self.user.nombre} {self.user.apellido}"
