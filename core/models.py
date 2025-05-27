
from django.db import models
from accounts.models import CustomUser  # asegúrate que esté importado

class Curso(models.Model):
    nombre = models.CharField(max_length=50)
    nivel = models.CharField(max_length=20)  # Ej: primaria, secundaria

    #Cambios aqui por Rodrigo
    materias = models.ManyToManyField(
        'Materia',
        through='CursoMateria',
        related_name='cursos'
    )

    def __str__(self):
        return f"{self.nombre} - {self.nivel}"

class Materia(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre
    
class CursoMateria(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="materias_asociadas")
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name="cursos_asociados")

    def __str__(self):
        return f"{self.curso} ➜ {self.materia}"

class CursoMateriaDocente(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    docente = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'rol': 'docente'})

    class Meta:
        unique_together = [('curso', 'materia')]  # impide duplicar asignación de materia por curso
        verbose_name = "Asignación de materia"
        verbose_name_plural = "Asignaciones de materias"

    def __str__(self):
        return f"{self.materia.nombre} en {self.curso.nombre} por {self.docente.nombre}"
    
    def clean(self):
        if CursoMateriaDocente.objects.filter(
            curso=self.curso, materia=self.materia
        ).exclude(id=self.id).exists():
            raise ValidationError("Ya existe un docente asignado a esta materia en ese curso.")

