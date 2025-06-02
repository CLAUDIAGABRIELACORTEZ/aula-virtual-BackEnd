from .models import EvaluacionActividad, NotaActividad, Autoevaluacion

def nota_trimestre(alumno, curso, materia, trimestre):
    """
    Calcula la nota final de un alumno en un trimestre especificado.
    Algoritmo:
    1) Para cada dimensión ('ser', 'saber', 'hacer', 'decidir'):
       - Busca todas las EvaluacionActividad de ese curso/materia/trimestre/dimensión.
       - Recolecta las notas de NotaActividad hechas por ese alumno en esas actividades.
       - Si hay notas, hacer (sum(notas) / len(notas)) → promedio_dim.
       - Sumar promedio_dim al total.
    2) Buscar si existe Autoevaluacion de ese alumno/curso/materia/trimestre.
       - Si existe, sumar auto.nota al total.
    3) Retornar round(total, 2).
    """

    total = 0.0
    dimensiones = ["ser", "saber", "hacer", "decidir"]

    for dim in dimensiones:
        # 1.1. Obtener las actividades de esa dimensión
        actividades = EvaluacionActividad.objects.filter(
            curso=curso,
            materia=materia,
            trimestre=trimestre,
            dimension=dim
        )

        # 1.2. Obtener las notas que el alumno sacó en esas actividades
        notas_qs = NotaActividad.objects.filter(
            alumno=alumno,
            evaluacion__in=actividades
        ).values_list("nota", flat=True)

        if notas_qs:
            promedio_dim = sum(notas_qs) / len(notas_qs)
            total += promedio_dim
        # Si no hay notas_qs, contribuye 0 automáticamente

    # 2. Autoevaluación (0–5) al final
    auto = Autoevaluacion.objects.filter(
        alumno=alumno,
        curso=curso,
        materia=materia,
        trimestre=trimestre
    ).first()
    if auto:
        total += auto.nota

    return round(total, 2)
