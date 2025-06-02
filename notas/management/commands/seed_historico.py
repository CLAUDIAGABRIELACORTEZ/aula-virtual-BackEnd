
import random
from django.core.management.base import BaseCommand
from django.db import transaction
from django_seed import Seed

from accounts.models import CustomUser
from core.models import Curso, Materia
from notas.models import HistoricoNota

class Command(BaseCommand):
    help = "Puebla la tabla HistoricoNota con datos de prueba coherentes usando django-seed."

    def handle(self, *args, **kwargs):
        seeder = Seed.seeder()

        alumnos_qs = CustomUser.objects.filter(rol="alumno")
        cursos_qs = Curso.objects.all()
        materias_qs = Materia.objects.all()

        lista_alumnos = list(alumnos_qs.values_list("id", flat=True))
        lista_cursos = list(cursos_qs.values_list("id", flat=True))
        lista_materias = list(materias_qs.values_list("id", flat=True))

        if not lista_alumnos or not lista_cursos or not lista_materias:
            self.stdout.write(self.style.ERROR("❌ Faltan datos: asegúrate de tener alumnos, cursos y materias."))
            return

        HistoricoNota.objects.all().delete()  # limpia datos anteriores

        def generar_notas():
            base = random.uniform(50, 90)  # nota base razonable
            t1 = round(base + random.uniform(-5, 5), 2)
            t2 = round(t1 + random.uniform(-5, 5), 2)
            t3 = round(t2 + random.uniform(-5, 5), 2)
            return t1, t2, t3

        def generar_año():
            return random.choice(["2022-I", "2023-I", "2023-II", "2024-I"])

        for _ in range(500):  # Genera más de 50 entradas ahora
            alumno_id  = random.choice(lista_alumnos)
            curso_id   = random.choice(lista_cursos)
            materia_id = random.choice(lista_materias)
            t1, t2, t3 = generar_notas()

            HistoricoNota.objects.create(
                alumno_id=alumno_id,
                curso_id=curso_id,
                materia_id=materia_id,
                nota_trim1=t1,
                nota_trim2=t2,
                nota_trim3=t3,
                año_académico=generar_año()
            )

        self.stdout.write(self.style.SUCCESS("✅ Datos de prueba coherentes insertados en HistoricoNota."))
