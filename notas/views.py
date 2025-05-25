from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsDocente
from .models import EvaluacionActividad, NotaActividad, Autoevaluacion
from .serializers import EvaluacionActividadSerializer, NotaActividadSerializer, AutoevaluacionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import CustomUser
from students.models import Alumno
from students.serializers import AlumnoSerializer
from core.models import CursoMateriaDocente
from rest_framework import permissions
from rest_framework import status


# class EvaluacionActividadViewSet(viewsets.ModelViewSet):
#     queryset = EvaluacionActividad.objects.all()
#     serializer_class = EvaluacionActividadSerializer
#     permission_classes = [IsAuthenticated, IsDocente]

#     def perform_create(self, serializer):
#         serializer.save(docente=self.request.user)  # Asigna el docente automáticamente

class EvaluacionActividadViewSet(viewsets.ModelViewSet):
    queryset = EvaluacionActividad.objects.all()
    serializer_class = EvaluacionActividadSerializer
    permission_classes = [IsAuthenticated, IsDocente]

    def get_queryset(self):
        user = self.request.user
        curso_id = self.request.query_params.get("curso")
        materia_id = self.request.query_params.get("materia")
        trimestre = self.request.query_params.get("trimestre")
        queryset = EvaluacionActividad.objects.filter(docente=user)

        if curso_id:
            queryset = queryset.filter(curso_id=curso_id)
        if materia_id:
            queryset = queryset.filter(materia_id=materia_id)
        if trimestre:
            queryset = queryset.filter(trimestre=trimestre)
        return queryset

    def perform_create(self, serializer):
        serializer.save(docente=self.request.user)

class NotaActividadViewSet(viewsets.ModelViewSet):
    queryset = NotaActividad.objects.all()
    serializer_class = NotaActividadSerializer
    permission_classes = [IsAuthenticated, IsDocente]

    def create(self, request, *args, **kwargs):
        data = request.data
        alumno = data.get("alumno")
        evaluacion = data.get("evaluacion")

        nota_existente = NotaActividad.objects.filter(alumno=alumno, evaluacion=evaluacion).first()
        if nota_existente:
            nota_existente.nota = data.get("nota")
            nota_existente.save()
            serializer = self.get_serializer(nota_existente)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return super().create(request, *args, **kwargs)

# class AutoevaluacionViewSet(viewsets.ModelViewSet):
#     queryset = Autoevaluacion.objects.all()
#     serializer_class = AutoevaluacionSerializer
#     permission_classes = [IsAuthenticated, IsDocente]
class AutoevaluacionViewSet(viewsets.ModelViewSet):
    queryset = Autoevaluacion.objects.all()
    serializer_class = AutoevaluacionSerializer
    permission_classes = [IsAuthenticated, IsDocente]

    # def get_queryset(self):
    #     curso_id = self.request.query_params.get("curso")
    #     materia_id = self.request.query_params.get("materia")
    #     trimestre = self.request.query_params.get("trimestre")

    #     queryset = Autoevaluacion.objects.all()

    #     if curso_id:
    #         queryset = queryset.filter(curso_id=curso_id)
    #     if materia_id:
    #         queryset = queryset.filter(materia_id=materia_id)
    #     if trimestre:
    #         queryset = queryset.filter(trimestre=trimestre)

    #     return queryset
    def create(self, request, *args, **kwargs):
        data = request.data
        alumno = data.get("alumno")
        curso = data.get("curso")
        materia = data.get("materia")
        trimestre = data.get("trimestre")

        existente = Autoevaluacion.objects.filter(
            alumno=alumno, curso=curso, materia=materia, trimestre=trimestre
        ).first()

        if existente:
            existente.nota = data.get("nota")
            existente.save()
            serializer = self.get_serializer(existente)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return super().create(request, *args, **kwargs)



class ListaAlumnosMateriaView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsDocente]

    def get(self, request):
        curso_id = request.query_params.get("curso")
        materia_id = request.query_params.get("materia")

        if not curso_id or not materia_id:
            return Response({"error": "curso y materia son requeridos"}, status=400)

        # Validar que el docente tiene esa asignación
        existe = CursoMateriaDocente.objects.filter(
            curso_id=curso_id,
            materia_id=materia_id,
            docente=request.user
        ).exists()

        if not existe:
            return Response({"error": "No tienes acceso a esta materia en ese curso"}, status=403)

        alumnos = Alumno.objects.filter(curso_id=curso_id)
        serializer = AlumnoSerializer(alumnos, many=True)

        return Response(serializer.data)


class CuadriculaNotasView(APIView):
    permission_classes = [IsAuthenticated, IsDocente]

    def get(self, request):
        curso_id = request.query_params.get("curso")
        materia_id = request.query_params.get("materia")
        trimestre = request.query_params.get("trimestre")  # opcional

        if not curso_id or not materia_id:
            return Response({"error": "curso y materia son requeridos"}, status=400)

        alumnos = CustomUser.objects.filter(rol="alumno", alumno__curso_id=curso_id)

        actividades = EvaluacionActividad.objects.filter(
            curso_id=curso_id,
            materia_id=materia_id,
            docente=request.user
        )
        if trimestre:
            actividades = actividades.filter(trimestre=trimestre)

        notas = NotaActividad.objects.filter(evaluacion__in=actividades)
        autoevals = Autoevaluacion.objects.filter(
            curso_id=curso_id,
            materia_id=materia_id,
            trimestre=trimestre,  # ← este es el fix
        )


        resultado = []
        for alumno in alumnos:
            alumno_data = {
                "alumno": alumno.id,
                "alumno_nombre": f"{alumno.nombre} {alumno.apellido}",
                "notas": {},
                "autoevaluacion": None,
            }

            for nota in notas.filter(alumno=alumno):
                alumno_data["notas"][str(nota.evaluacion.id)] = nota.nota

            auto = autoevals.filter(alumno=alumno).first()
            if auto:
                alumno_data["autoevaluacion"] = auto.nota

            resultado.append(alumno_data)

        return Response(resultado)




#  resumen de notas 
class ResumenNotasView(APIView):
    permission_classes = [IsAuthenticated, IsDocente]

    def get(self, request):
        curso_id = request.query_params.get("curso")
        materia_id = request.query_params.get("materia")
        trimestre = request.query_params.get("trimestre")

        if not all([curso_id, materia_id, trimestre]):
            return Response({"error": "Faltan parámetros: curso, materia y trimestre son obligatorios."}, status=400)

        alumnos = CustomUser.objects.filter(rol='alumno')
        dimensiones = {'ser': 5, 'saber': 45, 'hacer': 40, 'decidir': 5}
        resultados = []

        for alumno in alumnos:
            resumen = {"alumno": f"{alumno.nombre} {alumno.apellido}"}
            total = 0

            for dim, max_valor in dimensiones.items():
                actividades = EvaluacionActividad.objects.filter(
                    curso_id=curso_id, materia_id=materia_id,
                    docente=request.user, trimestre=trimestre,
                    dimension=dim
                )
                notas = NotaActividad.objects.filter(evaluacion__in=actividades, alumno=alumno)

                if notas.exists():
                    promedio = sum(n.nota for n in notas) / notas.count()
                else:
                    promedio = 0

                resumen[dim] = round(promedio, 1)
                total += promedio

            # Autoevaluación
            autoeval = Autoevaluacion.objects.filter(
                curso_id=curso_id, materia_id=materia_id,
                alumno=alumno, trimestre=trimestre
            ).first()
            autoeval_nota = autoeval.nota if autoeval else 0
            resumen["autoevaluacion"] = autoeval_nota
            total += autoeval_nota

            resumen["total"] = round(total, 1)

            # Clasificación
            if total <= 50:
                resumen["clasificacion"] = "Aplazado"
            elif total <= 60:
                resumen["clasificacion"] = "Aprobado"
            elif total <= 70:
                resumen["clasificacion"] = "Bueno"
            elif total <= 89:
                resumen["clasificacion"] = "Muy Bueno"
            else:
                resumen["clasificacion"] = "Excelente"

            resultados.append(resumen)

        return Response(resultados)
