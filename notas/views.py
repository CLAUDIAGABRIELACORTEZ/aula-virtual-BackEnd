from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsDocente
from .models import EvaluacionActividad, NotaActividad, Autoevaluacion, Materia
from .serializers import EvaluacionActividadSerializer, NotaActividadSerializer, AutoevaluacionSerializer,  PrediccionInputSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import CustomUser
from students.models import Alumno 
from students.serializers import AlumnoSerializer
from core.models import CursoMateriaDocente
from rest_framework import permissions
from rest_framework import status

from .services import get_model
from .utils import nota_trimestre

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


class AutoevaluacionViewSet(viewsets.ModelViewSet):
    queryset = Autoevaluacion.objects.all()
    serializer_class = AutoevaluacionSerializer
    permission_classes = [IsAuthenticated, IsDocente]

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

# nuevo enpoint para la parte de prediccion de notas


UMBRAL = 51  # ajusta según tu escala

class PrediccionTrim3View(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PrediccionInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        alumno_id  = serializer.validated_data["alumno"]   # ahora interpreta que es Alumno.id
        # curso_id   = serializer.validated_data["curso"]
        materia_id = serializer.validated_data["materia"]

        # 1. Intentamos obtener el registro de Alumno, no CustomUser
        try:
            alumno_instancia = Alumno.objects.select_related("user", "curso").get(id=alumno_id)
        except Alumno.DoesNotExist:
            return Response(
                {"error": f"El alumno con id={alumno_id} no existe como instancia Alumno."},
                status=400
            )

        # 2. Ahora, del modelo Alumno sacamos el CustomUser y el Curso
        usuario = alumno_instancia.user      # CustomUser asociado (debe tener rol="alumno")
        curso   = alumno_instancia.curso     # Curso asociado al Alumno

        # 3. Verificamos que exista la Materia
        try:
            materia = Materia.objects.get(id=materia_id)
        except Materia.DoesNotExist:
            return Response(
                {"error": f"La materia con id={materia_id} no existe."},
                status=400
            )

        # 4. Calculamos notas T1 y T2 con la función utilitaria
        #    nota_trimestre espera (usuario=CustomUser, curso=Curso, materia=Materia, trimestre="1er"/"2do"/"3er")
        n1 = nota_trimestre(usuario, curso, materia, "1er Trimestre")
        n2 = nota_trimestre(usuario, curso, materia, "2do Trimestre")

        # 5. Cargamos el modelo entrenado
        try:
            model = get_model()
        except FileNotFoundError:
            return Response(
                {"error": "El modelo predictivo no está disponible. Ejecuta retrain_trim3 primero."},
                status=503
            )

        # 6. Hacemos la predicción del 3er trimestre
        pred = model.predict([[n1, n2]])[0]
        nota_trim3 = round(float(pred), 2)

        # 7. Cálculo del promedio final
        promedio_final = round((n1 + n2 + nota_trim3) / 3, 2)

        # 8. Evaluaciones
        pasa_materia = promedio_final >= UMBRAL
        aplazo_trim3 = nota_trim3 < UMBRAL

        # 9. Devolvemos la respuesta
        return Response({
            "nota_trim1":            n1,
            "nota_trim2":            n2,
            "nota_predicha_trim3":   nota_trim3,
            "promedio_final":        promedio_final,
            "pasa":                  pasa_materia,
            "aplazo_trim3":          aplazo_trim3
        })

