from django.db import models
from accounts.models import CustomUser
from core.models import Curso, Materia

class EvaluacionActividad(models.Model):
    DIMENSIONES = [
        ('ser', 'Ser'),
        ('saber', 'Saber'),
        ('hacer', 'Hacer'),
        ('decidir', 'Decidir'),
    ]

    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    docente = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'rol': 'docente'})
    trimestre = models.CharField(max_length=20)  # Ej: "1er Trimestre"
    dimension = models.CharField(max_length=10, choices=DIMENSIONES)
    descripcion = models.CharField(max_length=255)  # Nombre de la actividad
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.dimension.upper()} - {self.descripcion} ({self.curso})"


class NotaActividad(models.Model):
    evaluacion = models.ForeignKey(EvaluacionActividad, on_delete=models.CASCADE, related_name="notas")
    alumno = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'rol': 'alumno'})
    nota = models.FloatField()

    class Meta:
        unique_together = ['evaluacion', 'alumno']

    def __str__(self):
        return f"{self.alumno} - {self.evaluacion}: {self.nota}"


class Autoevaluacion(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    alumno = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'rol': 'alumno'})
    trimestre = models.CharField(max_length=20)
    nota = models.FloatField(default=0)  # De 0 a 5

    class Meta:
        unique_together = ['curso', 'materia', 'alumno', 'trimestre']

    def __str__(self):
        return f"Autoevaluación {self.alumno} - {self.materia} ({self.trimestre})"
