from django.db import models
from accounts.models import CustomUser
from core.models import Curso, Materia
# notas/models.py

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
#    nueva agregacion par la parre de daros historicos

class HistoricoNota(models.Model):
    alumno = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'rol': 'alumno'},
        help_text="Usuario con rol 'alumno'."
    )
    curso = models.ForeignKey(
        Curso,
        on_delete=models.CASCADE,
        help_text="Curso en el que cursó la materia."
    )
    materia = models.ForeignKey(
        Materia,
        on_delete=models.CASCADE,
        help_text="Materia cursada."
    )

    nota_trim1 = models.FloatField(help_text="Nota final del 1er trimestre")
    nota_trim2 = models.FloatField(help_text="Nota final del 2do trimestre")
    nota_trim3 = models.FloatField(help_text="Nota final del 3er trimestre")

    año_académico = models.CharField(
        max_length=9,
        blank=True,
        null=True,
        help_text="Etiqueta de año o cohorte (opcional). Ej: '2023-I'."
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha en que se insertó este registro histórico."
    )

    def __str__(self):
        return f"{self.alumno} | {self.curso} | {self.materia} | {self.año_académico}"
