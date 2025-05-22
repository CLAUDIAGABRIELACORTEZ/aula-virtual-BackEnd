from django.db import models
from accounts.models import CustomUser
from core.models import Curso, Materia

class Alumno(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'rol': 'alumno'})
    curso = models.ForeignKey(Curso, on_delete=models.SET_NULL, null=True, related_name='alumnos')
    # materias = models.ManyToManyField(Materia, related_name='alumnos', blank=True)  # Opcional: para materias específicas

    def __str__(self):
        return f"{self.user.nombre} {self.user.apellido}"
