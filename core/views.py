from rest_framework import viewsets

from accounts import serializers
from .models import Curso, Materia, CursoMateria
from .serializers import CursoSerializer, MateriaSerializer, CursoMateriaSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsDocente
from .models import CursoMateriaDocente
from .serializers import CursoMateriaDocenteSerializer,CursoMateriaDocenteDetailSerializer
from rest_framework import viewsets
from accounts.permissions import IsDirector  # solo director puede asignar
from core.serializers import CursoMateriaDetailSerializer
from .serializers import AsignacionDocenteSerializer

class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

class MateriaViewSet(viewsets.ModelViewSet):
    queryset = Materia.objects.all()
    serializer_class = MateriaSerializer

class CursoMateriaViewSet(viewsets.ModelViewSet):
    queryset = CursoMateria.objects.all()
    serializer_class = CursoMateriaSerializer

class VistaSoloDocente(APIView):
    permission_classes = [IsAuthenticated, IsDocente]

    def get(self, request):
        from teachers.models import Docente

        try:
            docente = Docente.objects.get(user=request.user)
        except Docente.DoesNotExist:
            return Response({"error": "No es un docente válido"}, status=403)

        curso_materias = CursoMateria.objects.filter(materia__in=docente.materias.all()).select_related("curso", "materia")
        serializer = CursoMateriaDetailSerializer(curso_materias, many=True)

        return Response({
            "docente": request.user.nombre,
            "asignaciones": serializer.data
        })

class CursoMateriaDocenteViewSet(viewsets.ModelViewSet):
    queryset = CursoMateriaDocente.objects.all()
    permission_classes = [IsAuthenticated, IsDirector]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CursoMateriaDocenteDetailSerializer
        return CursoMateriaDocenteSerializer

    def perform_create(self, serializer):
        curso = serializer.validated_data['curso']
        materia = serializer.validated_data['materia']

        if CursoMateriaDocente.objects.filter(curso=curso, materia=materia).exists():
            raise ValidationError("Ya hay un docente asignado a esta materia en este curso.")
        serializer.save()
    
# par la vista del docente
class VistaAsignacionesDocente(APIView):
    permission_classes = [IsAuthenticated, IsDocente]

    def get(self, request):
        asignaciones = CursoMateriaDocente.objects.filter(docente=request.user).select_related("curso", "materia")
        serializer = AsignacionDocenteSerializer(asignaciones, many=True)

        return Response({
            "docente": request.user.nombre,
            "asignaciones": serializer.data
        })
